#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
네이밍 모듈
"""

import re
import os
import json

# 모듈 임포트
from .namingConfig import NamingConfig
from .namePart import NamePart


class Naming:
    """
    3ds Max 노드 이름을 관리하기 위한 클래스.
    MAXScript의 _Name 구조체와 _String 구조체를 통합하여 Python으로 재구현.
    namingConfig.py와 연동하여 JSON 설정 파일을 통한 설정 관리 지원.
    """
    
    def __init__(self, configPath=None):
        """
        클래스 초기화 및 기본 설정값 정의
        
        Args:
            configPath: 설정 파일 경로 (기본값: None)
                        설정 파일이 제공되면 해당 파일에서 설정을 로드함
        """
        # 기본 설정값
        self._paddingNum = 2
        self._configPath = configPath
        
        # 기본 namePart 초기화 (각 부분에 사전 정의 값 직접 설정)
        self._nameParts = []
        
        # Base 부분 - "b"는 기본값으로 더 높은 가중치 부여
        basePart = NamePart("Base", ["b", "Bip001"], {"b": 5, "Bip001": 10})
        
        # Type 부분 - 각 유형에 가중치 부여
        typePart = NamePart("Type", ["P", "Dum", "Exp", "IK", "T"], 
                          {"P": 5, "Dum": 10, "Exp": 15, "IK": 20, "T": 25})
        
        # Side 부분 - 의미론적 매핑 및 가중치
        sidePart = NamePart("Side", ["L", "R"], {"L": 5, "R": 10})
        
        # FrontBack 부분 - 의미론적 매핑 및 가중치
        frontBackPart = NamePart("FrontBack", ["F", "B"], {"F": 5, "B": 10})
        
        realNamePart = NamePart("RealName")
        indexPart = NamePart("Index")
        nubPart = NamePart("Nub", ["Nub"], {"Nub": 5})
        
        # 기본 순서대로 설정
        self._nameParts = [basePart, typePart, sidePart, frontBackPart, realNamePart, indexPart, nubPart]
        
        # 설정 파일이 제공된 경우 로드
        if configPath:
            self.load_from_config_file(configPath)
        else:
            # 기본 JSON 설정 파일 로드 시도
            self.load_default_config()

    # ---- String 관련 메소드들 (내부 사용 헬퍼 메소드) ----
    
    def _split_into_string_and_digit(self, inStr):
        """
        문자열을 문자부분과 숫자부분으로 분리
        
        Args:
            inStr: 분리할 문자열
            
        Returns:
            튜플 (문자부분, 숫자부분)
        """
        match = re.match(r'^(.*?)(\d*)$', inStr)
        if match:
            return match.group(1), match.group(2)
        return inStr, ""

    def _compare_string(self, inStr1, inStr2):
        """
        대소문자 구분 없이 문자열 비교
        
        Args:
            inStr1: 첫 번째 문자열
            inStr2: 두 번째 문자열
            
        Returns:
            비교 결과 (inStr1 < inStr2: 음수, inStr1 == inStr2: 0, inStr1 > inStr2: 양수)
        """
        # Python에서는 대소문자 구분 없는 비교를 위해 lower() 메서드 사용
        if inStr1.lower() < inStr2.lower():
            return -1
        elif inStr1.lower() > inStr2.lower():
            return 1
        return 0

    def _sort_by_alphabet(self, inArray):
        """
        배열 내 문자열을 알파벳 순으로 정렬
        
        Args:
            inArray: 정렬할 배열
            
        Returns:
            정렬된 배열
        """
        # Python의 sorted 함수와 lambda를 사용하여 대소문자 구분 없이 정렬
        return sorted(inArray, key=lambda x: x.lower())

    def _get_filtering_char(self, inStr):
        """
        문자열에서 사용된 구분자 문자 찾기
        
        Args:
            inStr: 확인할 문자열
            
        Returns:
            구분자 문자 (' ' 또는 '_' 또는 '')
        """
        if ' ' in inStr:
            return ' '
        if '_' in inStr:
            return '_'
        return ''

    def _filter_by_filtering_char(self, inStr):
        """
        구분자 문자로 문자열 분할
        
        Args:
            inStr: 분할할 문자열
            
        Returns:
            분할된 문자열 리스트
        """
        filChar = self._get_filtering_char(inStr)
        
        if not filChar:
            return [inStr]
            
        # 빈 문자열 제거하며 분할
        return [part for part in inStr.split(filChar) if part]

    def _filter_by_upper_case(self, inStr):
        """
        대문자로 시작하는 부분을 기준으로 문자열 분할
        
        Args:
            inStr: 분할할 문자열
            
        Returns:
            분할된 문자열 리스트
        """
        if not inStr:
            return []
            
        result = []
        currentPart = inStr[0]
        
        for i in range(1, len(inStr)):
            if inStr[i].isupper():
                result.append(currentPart)
                currentPart = inStr[i]
            else:
                currentPart += inStr[i]
                
        if currentPart:
            result.append(currentPart)
            
        return result

    def _has_digit(self, inStr):
        """
        문자열에 숫자가 포함되어 있는지 확인
        
        Args:
            inStr: 확인할 문자열
            
        Returns:
            숫자가 포함되어 있으면 True, 아니면 False
        """
        return bool(re.search(r'\d', inStr))

    def _is_digit(self, inStr):
        """
        문자열이 숫자로만 이루어져 있는지 확인
        
        Args:
            inStr: 확인할 문자열
            
        Returns:
            숫자로만 이루어져 있으면 True, 아니면 False
        """
        return bool(re.match(r'^\d+$', inStr))

    def _split_to_array(self, inStr):
        """
        문자열을 구분자 또는 대문자로 분할하고 숫자 부분도 분리
        
        Args:
            inStr: 분할할 문자열
            
        Returns:
            분할된 문자열 리스트
        """
        filChar = self._get_filtering_char(inStr)
        
        if not filChar:
            # 구분자가 없을 경우 대문자로 분할
            resultArray = self._filter_by_upper_case(inStr)
            tempArray = []
            
            for item in resultArray:
                if self._has_digit(item):
                    stringPart, digitPart = self._split_into_string_and_digit(item)
                    if stringPart:
                        tempArray.append(stringPart)
                    if digitPart:
                        tempArray.append(digitPart)
                else:
                    tempArray.append(item)
                    
            return tempArray
        else:
            # 구분자가 있을 경우 구분자로 분할
            return self._filter_by_filtering_char(inStr)

    def _remove_empty_string_in_array(self, inArray):
        """
        배열에서 빈 문자열 제거
        
        Args:
            inArray: 처리할 배열
            
        Returns:
            빈 문자열이 제거된 배열
        """
        return [item for item in inArray if item]

    def _combine(self, inArray, inFilChar=" "):
        """
        문자열 배열을 하나의 문자열로 결합
        
        Args:
            inArray: 결합할 문자열 배열
            filChar: 구분자 (기본값: 공백)
            
        Returns:
            결합된 문자열
        """
        refinedArray = self._remove_empty_string_in_array(inArray)
        
        if not refinedArray:
            return ""
            
        if len(refinedArray) == 1:
            return refinedArray[0]
            
        return inFilChar.join(refinedArray)

    def _find_and_replace(self, inStr, inTargetStr, inNewStr):
        """
        문자열 내 특정 부분을 다른 문자열로 대체
        
        Args:
            inStr: 원본 문자열
            inTargetStr: 대체할 대상 문자열
            inNewStr: 새 문자열
            
        Returns:
            대체된 문자열
        """
        return inStr.replace(inTargetStr, inNewStr)

    # ---- Name 관련 메서드들 ----
    
    # 사전 정의 값 편집 메서드 제거 (namingConfig를 통해서만 변경 가능)

    def get_padding_num(self):
        """
        패딩 숫자 가져오기
        
        Returns:
            패딩 숫자
        """
        return self._paddingNum

    def get_name_part(self, inNamePart):
        """
        namePart 이름으로 NamePart 객체 가져오기
        
        Args:
            namePart: 가져올 NamePart의 이름 ("Base", "Type", "Side" 등)
            
        Returns:
            해당 NamePart 객체, 존재하지 않으면 None
        """
        for part in self._nameParts:
            if part.get_name() == inNamePart:
                return part
        return None
        
    def get_name_part_index(self, inNamePart):
        """
        namePart 이름으로 인덱스 가져오기
        
        Args:
            namePart: 가져올 NamePart의 이름 ("Base", "Type", "Side" 등)
            
        Returns:
            해당 NamePart의 인덱스, 존재하지 않으면 -1
        """
        for i, part in enumerate(self._nameParts):
            if part.get_name() == inNamePart:
                return i
        return -1
    
    def get_nub_str(self):
        """
        넙 문자열 가져오기
        
        Returns:
            넙 문자열
        """
        nubPart = self.get_name_part("Nub")
        if nubPart:
            values = nubPart.get_predefined_values()
            if values and len(values) > 0:
                return values[0]
        return ""

    def get_left_str(self):
        """
        왼쪽 구분자 가져오기
        
        Returns:
            왼쪽 구분자
        """
        sidePart = self.get_name_part("Side")
        if sidePart:
            return sidePart.get_value_by_weight(inRank=5)
        return ""

    def get_right_str(self):
        """
        오른쪽 구분자 가져오기
        
        Returns:
            오른쪽 구분자
        """
        sidePart = self.get_name_part("Side")
        if sidePart:
            return sidePart.get_value_by_weight(inRank=10)
        return ""

    def get_front_str(self):
        """
        앞 구분자 가져오기
        
        Returns:
            앞 구분자
        """
        frontBackPart = self.get_name_part("FrontBack")
        if frontBackPart:
            return frontBackPart.get_value_by_weight(inRank=5)
        return ""

    def get_back_str(self):
        """
        뒤 구분자 가져오기
        
        Returns:
            뒤 구분자
        """
        frontBackPart = self.get_name_part("FrontBack")
        if frontBackPart:
            return frontBackPart.get_value_by_weight(inRank=10)
        return ""

    def get_base_part_index(self):
        """
        기본 부분 인덱스 가져오기
        
        Returns:
            기본 부분 인덱스
        """
        return self.get_name_part_index("Base")

    def get_type_part_index(self):
        """
        유형 부분 인덱스 가져오기
        
        Returns:
            유형 부분 인덱스
        """
        return self.get_name_part_index("Type")

    def get_side_part_index(self):
        """
        측면 부분 인덱스 가져오기
        
        Returns:
            측면 부분 인덱스
        """
        return self.get_name_part_index("Side")

    def get_front_back_part_index(self):
        """
        앞/뒤 부분 인덱스 가져오기
        
        Returns:
            앞/뒤 부분 인덱스
        """
        return self.get_name_part_index("FrontBack")

    def get_real_name_part_index(self):
        """
        실제 이름 부분 인덱스 가져오기
        
        Returns:
            실제 이름 부분 인덱스
        """
        return self.get_name_part_index("RealName")

    def get_index_part_index(self):
        """
        인덱스 부분 인덱스 가져오기
        
        Returns:
            인덱스 부분 인덱스
        """
        return self.get_name_part_index("Index")
    
    def get_nub_part_index(self):
        """
        넙(Nub) 부분 인덱스 가져오기
        
        Returns:
            넙 부분 인덱스
        """
        return self.get_name_part_index("Nub")

    def is_side_char(self, inChar):
        """
        문자가 측면 문자인지 확인
        
        Args:
            inChar: 확인할 문자
            
        Returns:
            측면 문자이면 True, 아니면 False
        """
        sidePart = self.get_name_part("Side")
        if sidePart:
            return inChar in sidePart.get_predefined_values()
        return False

    def is_front_back_char(self, inChar):
        """
        문자가 앞/뒤 문자인지 확인
        
        Args:
            inChar: 확인할 문자
            
        Returns:
            앞/뒤 문자이면 True, 아니면 False
        """
        frontBackPart = self.get_name_part("FrontBack")
        if frontBackPart:
            return inChar in frontBackPart.get_predefined_values()
        return False

    def is_type_char(self, inChar):
        """
        문자가 유형 문자인지 확인
        
        Args:
            inChar: 확인할 문자
            
        Returns:
            유형 문자이면 True, 아니면 False
        """
        typePart = self.get_name_part("Type")
        if typePart:
            return inChar in typePart.get_predefined_values()
        return False

    def is_base_char(self, inChar):
        """
        문자가 기본 문자인지 확인
        
        Args:
            inChar: 확인할 문자
            
        Returns:
            기본 문자이면 True, 아니면 False
        """
        basePart = self.get_name_part("Base")
        if basePart:
            return inChar in basePart.get_predefined_values()
        return False

    def is_index_char(self, inChar):
        """
        문자가 인덱스 문자인지 확인
        
        Args:
            inChar: 확인할 문자
            
        Returns:
            인덱스 문자이면 True, 아니면 False
        """
        return self._is_digit(inChar)
        
    def is_nub_char(self, inChar):
        """
        문자가 넙 문자인지 확인
        
        Args:
            inChar: 확인할 문자
            
        Returns:
            넙 문자이면 True, 아니면 False
        """
        nubPart = self.get_name_part("Nub")
        if nubPart:
            return inChar in nubPart.get_predefined_values()
        return False

    def get_char_type(self, inChar):
        """
        문자의 유형 가져오기
        
        Args:
            inChar: 확인할 문자
            
        Returns:
            문자 유형 ("Index", "Nub", "Side", "FrontBack", "Type", "Base" 중 하나)
        """
        # 인덱스 문자는 특별하게 처리 (숫자 여부 확인)
        if self.is_index_char(inChar):
            return "Index"
            
        # _nameParts에서 문자 유형 찾기
        for part in self._nameParts:
            partName = part.get_name()
            if partName != "Index" and partName != "RealName":  # Index는 이미 처리
                if inChar in part.get_predefined_values():
                    return partName
        
        return None

    def get_side(self, inStr):
        """
        문자열에서 측면 부분 추출
        
        Args:
            inStr: 처리할 문자열
            
        Returns:
            측면 부분 문자열
        """
        return self.get_name("Side", inStr)

    def get_base(self, inStr):
        """
        문자열에서 기본 부분 추출
        
        Args:
            inStr: 처리할 문자열
            
        Returns:
            기본 부분 문자열
        """
        return self.get_name("Base", inStr)

    def get_type(self, inStr):
        """
        문자열에서 유형 부분 추출
        
        Args:
            inStr: 처리할 문자열
            
        Returns:
            유형 부분 문자열
        """
        return self.get_name("Type", inStr)

    def get_front_back(self, inStr):
        """
        문자열에서 앞/뒤 부분 추출
        
        Args:
            inStr: 처리할 문자열
            
        Returns:
            앞/뒤 부분 문자열
        """
        return self.get_name("FrontBack", inStr)
        
    def get_name(self, inNamePart, inStr):
        """
        지정된 namePart에 해당하는 부분을 문자열에서 추출
        
        Args:
            namePart: 추출할 namePart 이름 ("Base", "Type", "Side" 등)
            inStr: 처리할 문자열
            
        Returns:
            지정된 namePart에 해당하는 문자열
        """
        nameArray = self._split_to_array(inStr)
        returnStr = ""
        
        # namePart 인덱스와 RealName 인덱스 가져오기
        partIndex = self.get_name_part_index(inNamePart)
        realNameIndex = self.get_real_name_part_index()
        
        # namePart가 유효하지 않으면 빈 문자열 반환
        if partIndex < 0:
            return returnStr
        
        # namePart 문자열 목록 가져오기
        partObj = self.get_name_part(inNamePart)
        partValues = partObj.get_predefined_values() if partObj else []
                
        # namePart 문자열이 있는지 확인
        found = False
        for item in nameArray:
            if item in partValues:
                found = True
                break
                
        if found:
            if partIndex < realNameIndex:
                # namePart가 실제 이름 앞에 있는 경우 - 앞에서부터 검색
                for i in range(len(nameArray)):
                    if nameArray[i] in partValues:
                        returnStr = nameArray[i]
                        break
            else:
                # namePart가 실제 이름 뒤에 있는 경우 - 뒤에서부터 검색
                for i in range(len(nameArray) - 1, -1, -1):
                    if nameArray[i] in partValues:
                        returnStr = nameArray[i]
                        break
        
        return returnStr

    def get_index(self, inStr):
        """
        문자열에서 인덱스 부분 추출
        
        Args:
            inStr: 처리할 문자열
            
        Returns:
            인덱스 부분 문자열
        """
        return self.get_name("Index", inStr)

    def get_nub(self, inStr):
        """
        문자열에서 넙 부분 추출
        
        Args:
            inStr: 처리할 문자열
            
        Returns:
            넙 부분 문자열
        """
        return self.get_name("Nub", inStr)

    def get_real_name(self, inStr):
        """
        문자열에서 실제 이름 부분 추출
        
        Args:
            inStr: 처리할 문자열
            
        Returns:
            실제 이름 부분 문자열
        """
        filChar = self._get_filtering_char(inStr)
        nameArray = self._split_to_array(inStr)
        realNameArray = []
        
        # 모든 nameParts 중 RealName이 아닌 것들의 값을 수집
        nonRealNameArray = []
        for part in self._nameParts:
            partName = part.get_name()
            if partName != "RealName":
                foundName = self.get_name(partName, inStr)
                nonRealNameArray.append(foundName)
        
        # 이름 배열에서 실제 이름이 아닌 부분 제외
        for item in nameArray:
            if item not in nonRealNameArray:
                realNameArray.append(item)
                
        # 구분자로 결합
        return self._combine(realNameArray, filChar)

    def convert_name_to_array(self, inStr):
        """
        문자열 이름을 이름 부분 배열로 변환
        
        Args:
            inStr: 변환할 이름 문자열
            
        Returns:
            이름 부분 배열 (Base, Type, Side, FrontBack, RealName, Index, Nub 등)
        """
        returnArray = [""] * len(self._nameParts)
        
        # 각 namePart에 대해 처리
        for i, part in enumerate(self._nameParts):
            partName = part.get_name()
            
            # 특수 케이스인 RealName은 마지막에 처리하기 위해 저장
            if partName == "RealName":
                realNameIndex = i
                continue
                
            # get_name 메소드를 사용하여 해당 부분 추출
            partValue = self.get_name(partName, inStr)
            returnArray[i] = partValue
        
        # 마지막으로 RealName 처리 (다른 모든 부분을 찾은 후에 수행해야 함)
        if 'realNameIndex' in locals():
            realNameStr = self.get_real_name(inStr)
            returnArray[realNameIndex] = realNameStr
        
        return returnArray
        
    def convert_to_dictionary(self, inStr):
        """
        문자열 이름을 이름 부분 딕셔너리로 변환
        
        Args:
            inStr: 변환할 이름 문자열
            
        Returns:
            이름 부분 딕셔너리 (키: namePart 이름, 값: 추출된 값)
            예: {"Base": "b", "Type": "P", "Side": "L", "RealName": "Arm", ...}
        """
        returnDict = {}
        
        # 각 namePart에 대해 처리
        for part in self._nameParts:
            partName = part.get_name()
            
            # 특수 케이스인 RealName은 마지막에 처리하기 위해 저장
            if partName == "RealName":
                continue
                
            # get_name 메소드를 사용하여 해당 부분 추출
            partValue = self.get_name(partName, inStr)
            returnDict[partName] = partValue
        
        # 마지막으로 RealName 처리 (다른 모든 부분을 찾은 후에 수행해야 함)
        realNameStr = self.get_real_name(inStr)
        returnDict["RealName"] = realNameStr
        
        return returnDict

    def is_nub(self, inStr):
        """
        이름에 넙(Nub) 부분이 있는지 확인
        
        Args:
            inStr: 확인할 이름 문자열
            
        Returns:
            넙이 있으면 True, 아니면 False
        """
        return bool(self.get_nub(inStr))

    def get_index_as_digit(self, inStr):
        """
        이름의 인덱스를 숫자로 변환
        
        Args:
            inStr: 변환할 이름 문자열
            
        Returns:
            숫자로 변환된 인덱스 (넙이 있으면 -1, 인덱스가 없으면 False)
        """
        if self.is_nub(inStr):
            return -1
            
        indexStr = self.get_index(inStr)
            
        if indexStr:
            try:
                return int(indexStr)
            except ValueError:
                pass
                
        return False

    def get_string(self, inStr):
        """
        인덱스 부분을 제외한 이름 문자열 가져오기
        
        Args:
            inStr: 처리할 이름 문자열
            
        Returns:
            인덱스가 제외된 이름 문자열
        """
        filChar = self._get_filtering_char(inStr)
        nameArray = self.convert_name_to_array(inStr)
        indexOrder = self.get_index_part_index()
        
        # 인덱스 부분 제거
        returnNameArray = nameArray.copy()
        returnNameArray[indexOrder] = ""
        
        return self._combine(returnNameArray, filChar)

    def set_index_as_nub(self, inStr):
        """
        이름에 넙(Nub) 부분을 추가하고 인덱스를 제거
        
        Args:
            inStr: 처리할 이름 문자열
            
        Returns:
            넙이 추가되고 인덱스가 제거된 이름 문자열
        """
        filChar = self._get_filtering_char(inStr)
        nameArray = self.convert_name_to_array(inStr)
        nubOrder = self.get_nub_part_index()
        indexOrder = self.get_index_part_index()
        
        # 인덱스 제거하고 넙 추

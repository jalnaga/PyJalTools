#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Naming 모듈 - 이름 규칙 관리 및 적용 기능 제공
NamePart 객체를 기반으로 조직화된 이름 생성 및 분석 기능 구현
"""

import os
import re
from typing import List, Dict, Any, Optional, Union, Tuple

# NamePart와 NamingConfig 임포트
from JalLib.namePart import NamePart, NamePartType
from JalLib.namingConfig import NamingConfig

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
        basePart = NamePart("Base", ["b", "Bip001"], {"b": 5, "Bip001": 10}, NamePartType.PREFIX)
        
        # Type 부분 - 각 유형에 가중치 부여
        typePart = NamePart("Type", ["P", "Dum", "Exp", "IK", "T"], 
                          {"P": 5, "Dum": 10, "Exp": 15, "IK": 20, "T": 25}, NamePartType.PREFIX)
        
        # Side 부분 - 의미론적 매핑 및 가중치
        sidePart = NamePart("Side", ["L", "R"], {"L": 5, "R": 10}, NamePartType.PREFIX)
        
        # FrontBack 부분 - 의미론적 매핑 및 가중치
        frontBackPart = NamePart("FrontBack", ["F", "B"], {"F": 5, "B": 10}, NamePartType.PREFIX)
        
        # RealName 부분 (REALNAME 타입)
        realNamePart = NamePart("RealName", [], {}, NamePartType.REALNAME)
        
        # Index 부분 (INDEX 타입)
        indexPart = NamePart("Index", [], {}, NamePartType.INDEX)
        
        # Nub 부분 (SUFFIX 타입)
        nubPart = NamePart("Nub", ["Nub"], {"Nub": 5}, NamePartType.SUFFIX)
        
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
        return any(char.isdigit() for char in inStr)

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
            return sidePart.get_value_by_min_weight()
        return ""

    def get_right_str(self):
        """
        오른쪽 구분자 가져오기
        
        Returns:
            오른쪽 구분자
        """
        sidePart = self.get_name_part("Side")
        if sidePart:
            return sidePart.get_value_by_max_weight()
        return ""

    def get_front_str(self):
        """
        앞 구분자 가져오기
        
        Returns:
            앞 구분자
        """
        frontBackPart = self.get_name_part("FrontBack")
        if frontBackPart:
            return frontBackPart.get_value_by_min_weight()
        return ""

    def get_back_str(self):
        """
        뒤 구분자 가져오기
        
        Returns:
            뒤 구분자
        """
        frontBackPart = self.get_name_part("FrontBack")
        if frontBackPart:
            return frontBackPart.get_value_by_max_weight()
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
        return inChar.isdigit()
        
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
    
    def pick_name(self, inNamePart, inStr):
        nameArray = self._split_to_array(inStr)
        returnStr = ""
        
        # namePart 문자열 목록 가져오기
        partObj = self.get_name_part(inNamePart)
        if not partObj:
            return returnStr
        
        partType = partObj.get_type()
        if not partType:
            return returnStr
            
        partValues = partObj.get_predefined_values()
        if partType != NamePartType.INDEX and partType != NamePartType.REALNAME and not partValues:
            return returnStr
        
        if partType == NamePartType.PREFIX:
            for item in nameArray:
                if item in partValues:
                    returnStr = item
                    break
        
        if partType == NamePartType.SUFFIX:
            for i in range(len(nameArray) - 1, -1, -1):
                if nameArray[i] in partValues:
                    returnStr = nameArray[i]
                    break
                
        if partType == NamePartType.INDEX:
            if self.get_index_part_index() > self.get_real_name_part_index():
                for i in range(len(nameArray) - 1, -1, -1):
                    if self.is_index_char(nameArray[i]):
                        returnStr = nameArray[i]
                        break
            else:
                for item in nameArray:
                    if self.is_index_char(item):
                        returnStr = item
                        break
        
        return returnStr
        
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
        
        partType = self.get_name_part(inNamePart).get_type()
        
        foundName = self.pick_name(inNamePart, inStr)
        if foundName == "":
            return returnStr
        foundIndex = nameArray.index(foundName)
        
        if partType == NamePartType.PREFIX:
            if foundIndex >= 0:
                prevNameParts = self._nameParts[:foundIndex]
                prevNames = [self.pick_name(part.get_name(), inStr) for part in prevNameParts]
                prevNamesInNameArray = nameArray[:foundIndex]
                for prevName in prevNames:
                    if prevName in prevNamesInNameArray:
                        prevNamesInNameArray.remove(prevName)
                if len(prevNamesInNameArray) == 0 :
                    returnStr = foundName
        
        if partType == NamePartType.SUFFIX:
            if foundIndex >= 0:
                nextNameParts = self._nameParts[foundIndex + 1:]
                nextNames = [self.pick_name(part.get_name(), inStr) for part in nextNameParts]
                nextNamesInNameArray = nameArray[foundIndex + 1:]
                for nextName in nextNames:
                    if nextName in nextNamesInNameArray:
                        nextNamesInNameArray.remove(nextName)
                if len(nextNamesInNameArray) == 0 :
                    returnStr = foundName
        
        if partType == NamePartType.INDEX:
            returnStr = self.pick_name(inNamePart, inStr)
                
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

    def load_from_config_file(self, configPath=None):
        """
        설정 파일에서 설정 로드
        
        Args:
            configPath: 설정 파일 경로 (기본값: self._configPath)
            
        Returns:
            로드 성공 여부 (True/False)
        """
        # 경로가 없으면 인스턴스 생성 시 설정된 경로 사용
        if not configPath:
            configPath = self._configPath
            
        if not configPath:
            print("설정 파일 경로가 제공되지 않았습니다.")
            return False
            
        # NamingConfig 인스턴스 생성 및 설정 로드
        config = NamingConfig()
        if config.load(configPath):
            # 설정을 Naming 인스턴스에 적용
            result = config.apply_to_naming(self)
            if result:
                self._configPath = configPath  # 성공적으로 로드한 경로 저장
            return result
        else:
            print(f"설정 파일 로드 실패: {configPath}")
            return False
    
    def load_default_config(self):
        """
        기본 설정 로드 (현재는 아무 작업도 수행하지 않음)
        
        Returns:
            항상 True 반환 (기본 설정은 __init__에서 이미 설정됨)
        """
        # 이 메소드는 현재 __init__에서 설정한 기본값을 그대로 사용하므로
        # 아무 작업도 수행하지 않습니다.
        return True
    
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
        
        # 인덱스 제거하고 넙 추가
        nameArray[indexOrder] = ""
        nameArray[nubOrder] = self.get_nub_str()
        
        return self._combine(nameArray, filChar)

    def is_left(self, inStr):
        """
        이름이 왼쪽(L) 측면인지 확인
        
        Args:
            inStr: 확인할 이름 문자열
            
        Returns:
            왼쪽이면 True, 아니면 False
        """
        sideChar = self.get_side(inStr)
        return sideChar and sideChar == self.get_left_str()

    def is_right(self, inStr):
        """
        이름이 오른쪽(R) 측면인지 확인
        
        Args:
            inStr: 확인할 이름 문자열
            
        Returns:
            오른쪽이면 True, 아니면 False
        """
        sideChar = self.get_side(inStr)
        return sideChar and sideChar == self.get_right_str()

    def is_front(self, inStr):
        """
        이름이 앞쪽(F)인지 확인
        
        Args:
            inStr: 확인할 이름 문자열
            
        Returns:
            앞쪽이면 True, 아니면 False
        """
        frontBackChar = self.get_front_back(inStr)
        return frontBackChar and frontBackChar == self.get_front_str()

    def is_back(self, inStr):
        """
        이름이 뒤쪽(B)인지 확인
        
        Args:
            inStr: 확인할 이름 문자열
            
        Returns:
            뒤쪽이면 True, 아니면 False
        """
        frontBackChar = self.get_front_back(inStr)
        return frontBackChar and frontBackChar == self.get_back_str()

    def has_side(self, inStr):
        """
        이름에 측면(L/R) 정보가 있는지 확인
        
        Args:
            inStr: 확인할 이름 문자열
            
        Returns:
            측면 정보가 있으면 True, 아니면 False
        """
        return self.is_left(inStr) or self.is_right(inStr)

    def has_front_back(self, inStr):
        """
        이름에 앞/뒤(F/B) 정보가 있는지 확인
        
        Args:
            inStr: 확인할 이름 문자열
            
        Returns:
            앞/뒤 정보가 있으면 True, 아니면 False
        """
        return self.is_front(inStr) or self.is_back(inStr)

    def get_non_real_name(self, inStr):
        """
        실제 이름 부분을 제외한 이름 가져오기
        
        Args:
            inStr: 처리할 이름 문자열
            
        Returns:
            실제 이름이 제외된 이름 문자열
        """
        filChar = self._get_filtering_char(inStr)
        nameArray = self.convert_name_to_array(inStr)
        realNameIndex = self.get_real_name_part_index()
        
        nameArray[realNameIndex] = ""
        return self._combine(nameArray, filChar)

    def combine(self, inPartsDict={}, inFilChar=" "):
        """
        namingConfig에서 정의된 nameParts와 그 순서에 따라 이름 부분들을 조합하여 완전한 이름 생성
        
        Args:
            parts_dict: namePart 이름과 값의 딕셔너리 (예: {"Base": "b", "Type": "P", "Side": "L"})
            inFilChar: 구분자 문자 (기본값: " ")
            
        Returns:
            조합된 이름 문자열
        """
        # 결과 배열 초기화 (빈 문자열로)
        combinedNameArray = [""] * len(self._nameParts)
        
        # 각 namePart에 대해
        for i, part in enumerate(self._nameParts):
            partName = part.get_name()
            # 딕셔너리에서 해당 부분의 값 가져오기 (없으면 빈 문자열 사용)
            if partName in inPartsDict:
                combinedNameArray[i] = inPartsDict[partName]
                
        # 배열을 문자열로 결합
        return self._combine(combinedNameArray, inFilChar)

    def add_fix(self, inStr, inPart, inFix, inPos="prefix"):
        """
        이름의 특정 부분에 접두사 또는 접미사 추가
        
        Args:
            inStr: 처리할 이름 문자열
            inPart: 수정할 부분 ("Base", "Type", "Side", "FrontBack", "RealName", "Index")
            inFix: 추가할 접두사/접미사
            pos: 위치 ("prefix" 또는 "suffix")
            
        Returns:
            수정된 이름 문자열
        """
        returnStr = inStr
        
        if inFix:
            filChar = self._get_filtering_char(inStr)
            nameArray = self.convert_name_to_array(inStr)
            partIndex = self.get_name_part_index(inPart)
                
            if partIndex >= 0:
                if inPos == "prefix":
                    nameArray[partIndex] = inFix + nameArray[partIndex]
                elif inPos == "suffix":
                    nameArray[partIndex] = nameArray[partIndex] + inFix
                    
                returnStr = self._combine(nameArray, filChar)
                
        return returnStr

    def add_prefix_to_real_name(self, inStr, inPrefix):
        """
        실제 이름 부분에 접두사 추가
        
        Args:
            inStr: 처리할 이름 문자열
            inPrefix: 추가할 접두사
            
        Returns:
            수정된 이름 문자열
        """
        return self.add_fix(inStr, "RealName", inPrefix, "prefix")

    def add_suffix_to_real_name(self, inStr, inSuffix):
        """
        실제 이름 부분에 접미사 추가
        
        Args:
            inStr: 처리할 이름 문자열
            inSuffix: 추가할 접미사
            
        Returns:
            수정된 이름 문자열
        """
        return self.add_fix(inStr, "RealName", inSuffix, "suffix")

    def convert_digit_into_padding_string(self, inDigit, inPaddingNum=None):
        """
        숫자를 패딩된 문자열로 변환
        
        Args:
            inDigit: 변환할 숫자 또는 숫자 문자열
            inPaddingNum: 패딩 자릿수 (기본값: 클래스의 _paddingNum)
            
        Returns:
            패딩된 문자열
        """
        if inPaddingNum is None:
            inPaddingNum = self._paddingNum
            
        digitNum = 0
        
        if isinstance(inDigit, int):
            digitNum = inDigit
        elif isinstance(inDigit, str):
            if inDigit.isdigit():
                digitNum = int(inDigit)
                
        # Python의 문자열 포맷팅을 사용하여 패딩
        return f"{digitNum:0{inPaddingNum}d}"

    def set_index_padding_num(self, inStr, inPaddingNum=None):
        """
        이름의 인덱스 부분 패딩 설정
        
        Args:
            inStr: 처리할 이름 문자열
            inPaddingNum: 설정할 패딩 자릿수 (기본값: 클래스의 _paddingNum)
            
        Returns:
            패딩이 적용된 이름 문자열
        """
        if inPaddingNum is None:
            inPaddingNum = self._paddingNum
            
        filChar = self._get_filtering_char(inStr)
        nameArray = self.convert_name_to_array(inStr)
        indexIndex = self.get_index_part_index()
        indexStr = self.get_index(inStr)
        
        if indexStr and not self.is_nub(inStr):
            indexStr = self.convert_digit_into_padding_string(indexStr, inPaddingNum)
            nameArray[indexIndex] = indexStr
            
        return self._combine(nameArray, filChar)

    def get_index_padding_num(self, inStr):
        """
        이름의 인덱스 부분 패딩 자릿수 가져오기
        
        Args:
            inStr: 처리할 이름 문자열
            
        Returns:
            인덱스 패딩 자릿수
        """
        indexVal = self.get_index(inStr)
        
        if not self.is_nub(inStr) and indexVal:
            return len(indexVal)
            
        return 1

    def increase_index(self, inStr, inAmount):
        """
        이름의 인덱스 부분 값 증가
        
        Args:
            inStr: 처리할 이름 문자열
            inAmount: 증가시킬 값
            
        Returns:
            인덱스가 증가된 이름 문자열
        """
        newName = inStr
        filChar = self._get_filtering_char(inStr)
        nameArray = self.convert_name_to_array(inStr)
        indexIndex = self.get_index_part_index()
        nubIndex = self.get_nub_part_index()
        
        if indexIndex >= 0:
            indexStr = ""
            indexPaddingNum = self._paddingNum
            indexNum = -9999
            
            if not nameArray[indexIndex]:
                indexNum = -1
            elif self.is_nub(inStr):
                indexNum = -9999999
            else:
                try:
                    indexNum = int(nameArray[indexIndex])
                    indexPaddingNum = len(nameArray[indexIndex])
                except ValueError:
                    pass
            
            indexNum += inAmount
            
            if indexNum > -1:
                # Python의 문자열 포맷팅을 사용하여 패딩
                indexStr = f"{indexNum:0{indexPaddingNum}d}"
                nameArray[indexIndex] = indexStr
                nameArray[nubIndex] = ""
            else:
                nameArray[indexIndex] = ""
                nameArray[nubIndex] = self.get_nub_str()
                
            nameArray[indexIndex] = indexStr
            newName = self._combine(nameArray, filChar)
            
        return newName

    def replace_filtering_char(self, inStr, inNewFilChar):
        """
        이름의 구분자 문자 변경
        
        Args:
            inStr: 처리할 이름 문자열
            inNewFilChar: 새 구분자 문자
            
        Returns:
            구분자가 변경된 이름 문자열
        """
        nameArray = self.convert_name_to_array(inStr)
        return self._combine(nameArray, inNewFilChar)

    def replace_base(self, inStr, inNewBase):
        """
        이름의 기본 부분 교체
        
        Args:
            inStr: 처리할 이름 문자열
            inNewBase: 새 기본 부분
            
        Returns:
            기본 부분이 교체된 이름 문자열
        """
        returnVal = inStr
        filChar = self._get_filtering_char(inStr)
        nameArray = self.convert_name_to_array(inStr)
        baseIndex = self.get_base_part_index()
        
        if baseIndex >= 0:
            nameArray[baseIndex] = inNewBase
            returnVal = self._combine(nameArray, filChar)
            
        return returnVal

    def replace_type(self, inStr, inNewType):
        """
        이름의 유형 부분 교체
        
        Args:
            inStr: 처리할 이름 문자열
            inNewType: 새 유형 부분
            
        Returns:
            유형 부분이 교체된 이름 문자열
        """
        returnVal = inStr
        filChar = self._get_filtering_char(inStr)
        nameArray = self.convert_name_to_array(inStr)
        typeIndex = self.get_type_part_index()
        
        if typeIndex >= 0:
            nameArray[typeIndex] = inNewType
            returnVal = self._combine(nameArray, filChar)
            
        return returnVal

    def replace_side(self, inStr, inNewSide):
        """
        이름의 측면 부분 교체
        
        Args:
            inStr: 처리할 이름 문자열
            inNewSide: 새 측면 부분
            
        Returns:
            측면 부분이 교체된 이름 문자열
        """
        returnVal = inStr
        filChar = self._get_filtering_char(inStr)
        nameArray = self.convert_name_to_array(inStr)
        sideIndex = self.get_side_part_index()
        
        if sideIndex >= 0:
            nameArray[sideIndex] = inNewSide
            returnVal = self._combine(nameArray, filChar)
            
        return returnVal

    def replace_front_back(self, inStr, inNewFrontBack):
        """
        이름의 앞/뒤 부분 교체
        
        Args:
            inStr: 처리할 이름 문자열
            inNewFrontBack: 새 앞/뒤 부분
            
        Returns:
            앞/뒤 부분이 교체된 이름 문자열
        """
        returnVal = inStr
        filChar = self._get_filtering_char(inStr)
        nameArray = self.convert_name_to_array(inStr)
        frontBackIndex = self.get_front_back_part_index()
        
        if frontBackIndex >= 0:
            nameArray[frontBackIndex] = inNewFrontBack
            returnVal = self._combine(nameArray, filChar)
            
        return returnVal

    def replace_index(self, inStr, inNewIndex, inKeepPadding=True):
        """
        이름의 인덱스 부분 교체
        
        Args:
            inStr: 처리할 이름 문자열
            inNewIndex: 새 인덱스 부분
            keepPadding: 패딩 유지 여부 (기본값: True)
            
        Returns:
            인덱스 부분이 교체된 이름 문자열
        """
        returnVal = inStr
        filChar = self._get_filtering_char(inStr)
        nameArray = self.convert_name_to_array(inStr)
        indexIndex = self.get_index_part_index()
        
        if indexIndex >= 0:
            nameArray[indexIndex] = inNewIndex
            returnVal = self._combine(nameArray, filChar)
            
            if inKeepPadding:
                indexPaddingNum = self.get_index_padding_num(inStr)
                returnVal = self.set_index_padding_num(returnVal, indexPaddingNum)
                
        return returnVal

    def replace_real_name(self, inStr, inNewRealName):
        """
        이름의 실제 이름 부분 교체
        
        Args:
            inStr: 처리할 이름 문자열
            inNewRealName: 새 실제 이름 부분
            
        Returns:
            실제 이름 부분이 교체된 이름 문자열
        """
        returnVal = inStr
        filChar = self._get_filtering_char(inStr)
        nameArray = self.convert_name_to_array(inStr)
        realNameIndex = self.get_real_name_part_index()
        
        if realNameIndex >= 0:
            nameArray[realNameIndex] = inNewRealName
            returnVal = self._combine(nameArray, filChar)
            
        return returnVal

    def remove_type(self, inStr):
        """
        이름에서 유형 부분 제거
        
        Args:
            inStr: 처리할 이름 문자열
            
        Returns:
            유형 부분이 제거된 이름 문자열
        """
        return self.replace_type(inStr, "")

    def remove_side(self, inStr):
        """
        이름에서 측면 부분 제거
        
        Args:
            inStr: 처리할 이름 문자열
            
        Returns:
            측면 부분이 제거된 이름 문자열
        """
        return self.replace_side(inStr, "")

    def remove_index(self, inStr):
        """
        이름에서 인덱스 부분 제거
        
        Args:
            inStr: 처리할 이름 문자열
            
        Returns:
            인덱스 부분이 제거된 이름 문자열
        """
        return self.replace_index(inStr, "")

    def remove_base(self, inStr):
        """
        이름에서 기본 부분 제거
        
        Args:
            inStr: 처리할 이름 문자열
            
        Returns:
            기본 부분이 제거된 이름 문자열
        """
        return self.replace_base(inStr, "")

    def gen_mirroring_name(self, inStr):
        """
        미러링된 이름 생성 (측면 또는 앞/뒤 변경)
        
        이름에서 Side와 FrontBack namePart를 자동으로 검색하고,
        발견된 값의 semanticmapping weight와 가장 차이가 큰 값으로 교체합니다.
        
        Args:
            inStr: 처리할 이름 문자열
            
        Returns:
            미러링된 이름 문자열
        """
        returnName = inStr
        
        # Side 부분 처리
        if self.has_side(inStr):
            sidePart = self.get_name_part("Side")
            currentSide = self.get_side(inStr)
            
            # 가중치 차이가 가장 큰 값 찾기
            oppositeSide = sidePart.get_most_different_weight_value(currentSide)
            
            if oppositeSide:
                # 값 교체
                returnName = self.replace_side(returnName, oppositeSide)
        
        # FrontBack 부분 처리
        if self.has_front_back(inStr):
            frontbackPart = self.get_name_part("FrontBack")
            currentFb = self.get_front_back(inStr)
            
            # 가중치 차이가 가장 큰 값 찾기
            oppositeFb = frontbackPart.get_most_different_weight_value(currentFb)
            
            if oppositeFb:
                # 값 교체
                returnName = self.replace_front_back(returnName, oppositeFb)
        
        return returnName

    def sort_by_index(self, inNameArray):
        """
        이름 배열을 인덱스 기준으로 정렬
        
        Args:
            inNameArray: 정렬할 이름 배열
            
        Returns:
            인덱스 기준으로 정렬된 이름 배열
        """
        if not inNameArray:
            return []
            
        # 정렬을 위한 보조 클래스 정의
        class IndexSorting:
            def __init__(self, inOriIndex, inNewIndex):
                self.oriIndex = inOriIndex
                self.newIndex = inNewIndex
                
        # 각 이름의 인덱스를 추출하여 정렬 정보 생성
        structArray = []
        
        for i, name in enumerate(inNameArray):
            tempIndex = self.get_index_as_digit(name)
            
            if tempIndex is False:
                structArray.append(IndexSorting(i, 0))
            else:
                structArray.append(IndexSorting(i, tempIndex))
                
        # 인덱스 기준으로 정렬
        structArray.sort(key=lambda x: x.newIndex)
        
        # 정렬된 순서로 결과 배열 생성
        sortedNameArray = []
        for struct in structArray:
            sortedNameArray.append(inNameArray[struct.oriIndex])
            
        return sortedNameArray

    def get_config_path(self):
        """
        현재 설정 파일 경로 가져오기
        
        Returns:
            설정 파일 경로 (없으면 빈 문자열)
        """
        return self._configPath or ""

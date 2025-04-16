#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
3ds Max용 이름 처리 모듈
3ds Max에 특화된 네이밍 기능 (pymxs 의존)
"""

from pymxs import runtime as rt
from JalLib.naming import Naming
from JalLib.namePart import NamePart, NamePartType

class Name(Naming):
    """
    3ds Max 노드 이름 관리를 위한 클래스
    Naming 클래스를 상속받으며, Max 특화 기능 제공
    """
    
    def __init__(self, configPath=None):
        """
        클래스 초기화
        
        Args:
            configPath: 설정 파일 경로 (기본값: None)
                        설정 파일이 제공되면 해당 파일에서 설정을 로드함
        """
        # 기본 설정값
        self._paddingNum = 2
        self._configPath = configPath
        
        # 기본 namePart 초기화 (각 부분에 사전 정의 값 직접 설정)
        self._nameParts = []
        
        if configPath:
            # 사용자가 지정한 설정 파일 사용
            self.load_from_config_file(configPath=configPath)
        else:
            # 설정 파일이 없는 경우, 기본 설정값으로 초기화
            # Base 부분 (PREFIX 타입)
            basePart = NamePart("Base", NamePartType.PREFIX, 
                             ["b", "Bip001"], 
                             ["SkinBone", "Biped"])
            # Type 부분 (PREFIX 타입)
            typePart = NamePart("Type", NamePartType.PREFIX, 
                             ["P", "Dum", "Exp", "IK", "T"], 
                             ["Parent", "Dummy", "ExposeTM", "IK", "Target"])
            # Side 부분 (PREFIX 타입)
            sidePart = NamePart("Side", NamePartType.PREFIX,
                             ["L", "R"], 
                             ["Left", "Right"])
            # FrontBack 부분 (PREFIX 타입)
            frontBackPart = NamePart("FrontBack", NamePartType.PREFIX,
                                 ["F", "B"], 
                                 ["Front", "Back"])
            # RealName 부분 (REALNAME 타입)
            realNamePart = NamePart("RealName", NamePartType.REALNAME, [], [])
            # Index 부분 (INDEX 타입)
            indexPart = NamePart("Index", NamePartType.INDEX, [], [])
            # Nub 부분 (SUFFIX 타입)
            nubPart = NamePart("Nub", NamePartType.SUFFIX,
                             ["Nub"], 
                             ["Nub"])
            # 기본 순서대로 설정
            self._nameParts = [basePart, typePart, sidePart, frontBackPart, realNamePart, indexPart, nubPart]
    
    # NamePart 직접 액세스 메소드들
    
    def get_Base_str(self):
        """
        Base 이름 문자열 반환
        
        Returns:
            Base 이름 문자열, 없으면 빈 문자열
        """
        basePart = self.get_name_part("Base")
        if basePart:
            return basePart.get_value_by_min_weight()
        return ""
    
    def get_Base_values(self):
        """
        Base 이름 부분의 모든 사전 정의 값 반환
        
        Returns:
            Base 값 목록, 없으면 빈 리스트
        """
        basePart = self.get_name_part("Base")
        if basePart:
            return basePart.get_predefined_values()
        return []
    
    def is_Base_char(self, inChar):
        """
        문자가 Base 값인지 확인
        
        Args:
            inChar: 확인할 문자
            
        Returns:
            Base 값이면 True, 아니면 False
        """
        basePart = self.get_name_part("Base")
        if basePart:
            return inChar in basePart.get_predefined_values()
        return False
    
    def get_Type_str(self):
        """
        Type 이름 문자열 반환
        
        Returns:
            Type 이름 문자열, 없으면 빈 문자열
        """
        typePart = self.get_name_part("Type")
        if typePart:
            return typePart.get_value_by_min_weight()
        return ""
    
    def get_Type_values(self):
        """
        Type 이름 부분의 모든 사전 정의 값 반환
        
        Returns:
            Type 값 목록, 없으면 빈 리스트
        """
        typePart = self.get_name_part("Type")
        if typePart:
            return typePart.get_predefined_values()
        return []
    
    def is_Type_char(self, inChar):
        """
        문자가 Type 값인지 확인
        
        Args:
            inChar: 확인할 문자
            
        Returns:
            Type 값이면 True, 아니면 False
        """
        typePart = self.get_name_part("Type")
        if typePart:
            return inChar in typePart.get_predefined_values()
        return False
    
    def get_Side_str(self):
        """
        Side 이름 문자열 반환
        
        Returns:
            Side 이름 문자열, 없으면 빈 문자열
        """
        sidePart = self.get_name_part("Side")
        if sidePart:
            return sidePart.get_value_by_min_weight()
        return ""
    
    def get_Side_values(self):
        """
        Side 이름 부분의 모든 사전 정의 값 반환
        
        Returns:
            Side 값 목록, 없으면 빈 리스트
        """
        sidePart = self.get_name_part("Side")
        if sidePart:
            return sidePart.get_predefined_values()
        return []
    
    def is_Side_char(self, inChar):
        """
        문자가 Side 값인지 확인
        
        Args:
            inChar: 확인할 문자
            
        Returns:
            Side 값이면 True, 아니면 False
        """
        sidePart = self.get_name_part("Side")
        if sidePart:
            return inChar in sidePart.get_predefined_values()
        return False
    
    def get_FrontBack_str(self):
        """
        FrontBack 이름 문자열 반환
        
        Returns:
            FrontBack 이름 문자열, 없으면 빈 문자열
        """
        frontBackPart = self.get_name_part("FrontBack")
        if frontBackPart:
            return frontBackPart.get_value_by_min_weight()
        return ""
    
    def get_FrontBack_values(self):
        """
        FrontBack 이름 부분의 모든 사전 정의 값 반환
        
        Returns:
            FrontBack 값 목록, 없으면 빈 리스트
        """
        frontBackPart = self.get_name_part("FrontBack")
        if frontBackPart:
            return frontBackPart.get_predefined_values()
        return []
    
    def is_FrontBack_char(self, inChar):
        """
        문자가 FrontBack 값인지 확인
        
        Args:
            inChar: 확인할 문자
            
        Returns:
            FrontBack 값이면 True, 아니면 False
        """
        frontBackPart = self.get_name_part("FrontBack")
        if frontBackPart:
            return inChar in frontBackPart.get_predefined_values()
        return False
    
    def get_RealName_str(self, inStr):
        """
        문자열에서 RealName 부분 추출
        
        Args:
            inStr: 처리할 문자열
            
        Returns:
            RealName 부분 문자열
        """
        return self.get_name("RealName", inStr)
    
    def get_Index_str(self, inStr):
        """
        문자열에서 Index 부분 추출
        
        Args:
            inStr: 처리할 문자열
            
        Returns:
            Index 부분 문자열
        """
        return self.get_name("Index", inStr)
    
    def is_Index_char(self, inChar):
        """
        문자가 Index 값인지 확인
        
        Args:
            inChar: 확인할 문자
            
        Returns:
            숫자로만 구성되어 있으면 True, 아니면 False
        """
        return inChar.isdigit()
    
    def get_Nub_str(self):
        """
        Nub 이름 문자열 반환
        
        Returns:
            Nub 이름 문자열, 없으면 빈 문자열
        """
        nubPart = self.get_name_part("Nub")
        if nubPart:
            return nubPart.get_value_by_min_weight()
        return ""
    
    def get_Nub_values(self):
        """
        Nub 이름 부분의 모든 사전 정의 값 반환
        
        Returns:
            Nub 값 목록, 없으면 빈 리스트
        """
        nubPart = self.get_name_part("Nub")
        if nubPart:
            return nubPart.get_predefined_values()
        return []
    
    def is_Nub(self, inStr):
        """
        문자열이 Nub 값인지 확인
        
        Args:
            inStr: 확인할 문자열
            
        Returns:
            Nub 값이면 True, 아니면 False
        """
        nubPart = self.get_name_part("Nub")
        if nubPart:
            nubValues = nubPart.get_predefined_values()
            return self.get_nub(inStr) in nubValues
        return False
    
    # 기존 특화 메소드들
    
    # pymxs 의존적인 메소드 구현
    
    def gen_unique_name(self, inStr):
        """
        고유한 이름 생성
        
        Args:
            inStr: 기준 이름 문자열
            
        Returns:
            고유한 이름 문자열
        """
        pattern_str = self.replace_index(inStr, "*")
        
        # pymxs를 사용하여 객체 이름을 패턴과 매칭하여 검색
        matched_objects = []
        
        # 모든 객체 중에서 패턴과 일치하는 이름 찾기
        for obj in rt.objects:
            if rt.matchPattern(obj.name, pattern=pattern_str):
                matched_objects.append(obj)
                
        return self.replace_index(inStr, str(len(matched_objects) + 1))
    
    def compare_name(self, inObjA, inObjB):
        """
        두 객체의 이름 비교 (정렬용)
        
        Args:
            inObjA: 첫 번째 객체
            inObjB: 두 번째 객체
            
        Returns:
            비교 결과 (inObjA.name < inObjB.name: 음수, inObjA.name == inObjB.name: 0, inObjA.name > inObjB.name: 양수)
        """
        # Python에서는 대소문자 구분 없는 비교를 위해 lower() 사용
        return 1 if inObjA.name.lower() > inObjB.name.lower() else -1 if inObjA.name.lower() < inObjB.name.lower() else 0
    
    def sort_by_name(self, inArray):
        """
        객체 배열을 이름 기준으로 정렬
        
        Args:
            inArray: 정렬할 객체 배열
            
        Returns:
            이름 기준으로 정렬된 객체 배열
        """
        # Python의 sorted 함수와 key를 사용하여 이름 기준 정렬
        return sorted(inArray, key=lambda obj: obj.name.lower())
        
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
        return_name = super().gen_mirroring_name(inStr)
        
        # 이름이 변경되지 않았다면 고유한 이름 생성
        if return_name == inStr:
            return_name = self.gen_unique_name(inStr)
            
        return return_name
    
    def get_parent_str(self):
        """
        부모 이름 문자열 반환
        
        Returns:
            부모 이름 문자열
        """
        return self.get_name_part("Type").get_value_by_weight(inRank=5)
    
    def get_dummy_str(self):
        """
        더미 이름 문자열 반환
        
        Returns:
            더미 이름 문자열
        """
        return self.get_name_part("Type").get_value_by_weight(inRank=10)
    
    def get_exposeTm_str(self):
        """
        ExposeTm 이름 문자열 반환
        
        Returns:
            ExposeTm 이름 문자열
        """
        return self.get_name_part("Type").get_value_by_weight(inRank=15)
    
    def get_ik_str(self):
        """
        IK 이름 문자열 반환
        
        Returns:
            IK 이름 문자열
        """
        return self.get_name_part("Type").get_value_by_weight(inRank=20)
    
    def get_target_str(self):
        """
        타겟 이름 문자열 반환
        
        Returns:
            타겟 이름 문자열
        """
        return self.get_name_part("Type").get_value_by_weight(inRank=25)
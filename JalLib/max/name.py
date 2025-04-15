#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
3ds Max용 이름 처리 모듈
3ds Max에 특화된 네이밍 기능 (pymxs 의존)
"""

from pymxs import runtime as rt
from JalLib.naming import Naming

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
        # 부모 클래스 초기화
        super().__init__(configPath)
    
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
        return_name = self.gen_mirroring_name(inStr)
        
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
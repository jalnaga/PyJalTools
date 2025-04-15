#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
namePart 모듈 - 이름의 각 부분을 표현하는 기능 제공
이름 부분의 사전 정의된 값과 의미론적 매핑을 관리하는 클래스 구현
"""

from typing import List, Dict, Any, Optional, Union
from enum import Enum, auto

class NamePartType(Enum):
    """
    이름 부분(name part)의 유형을 정의하는 열거형 클래스.
    
    - PREFIX: RealName 앞에 오는 부분, 사전 정의 값 필수
    - SUFFIX: RealName 뒤에 오는 부분, 사전 정의 값 필수
    - REALNAME: 실제 이름 부분, 자유 텍스트 가능
    - INDEX: 숫자만 허용되는 부분
    - UNDEFINED: 정의되지 않은 타입 (기본값)
    """
    PREFIX = auto()
    SUFFIX = auto()
    REALNAME = auto()
    INDEX = auto()
    UNDEFINED = auto()

class NamePart:
    """
    이름 부분(name part)을 관리하기 위한 클래스.
    이름과 해당 부분에 대한 사전 선언된 값들을 관리합니다.
    """
    
    def __init__(self, inName="", inPredefinedValues=None, inSemanticMapping=None, inType=NamePartType.UNDEFINED):
        """
        NamePart 클래스 초기화
        
        Args:
            inName: 이름 부분의 이름 (예: "Base", "Type", "Side" 등)
            inPredefinedValues: 사전 선언된 값 목록 (기본값: None, 빈 리스트로 초기화)
            inSemanticMapping: 의미론적 매핑 또는 가중치 딕셔너리
                           (예: {"L": "left", "R": "right"}, {"P": 10, "Dum": 5})
            inType: NamePart의 타입 (NamePartType 열거형 값)
        """
        self._name = inName
        self._predefinedValues = inPredefinedValues if inPredefinedValues is not None else []
        self._semanticMappings = inSemanticMapping if inSemanticMapping is not None else {}
        self._type = inType
        
        # 타입에 따른 기본 값 설정
        self._initialize_type_defaults()
    
    def _initialize_type_defaults(self):
        """타입에 따른 기본 설정을 초기화합니다."""
        if self._type == NamePartType.INDEX:
            # Index 타입은 숫자만 처리하므로 predefined values는 사용하지 않음
            self._predefinedValues = []
        elif self._type == NamePartType.REALNAME:
            # RealName 타입은 predefined values를 사용하지 않음
            self._predefinedValues = []
    
    def set_name(self, inName):
        """
        이름 부분의 이름을 설정합니다.
        
        Args:
            inName: 설정할 이름
        """
        self._name = inName
    
    def get_name(self):
        """
        이름 부분의 이름을 반환합니다.
        
        Returns:
            이름 부분의 이름
        """
        return self._name
    
    def set_type(self, inType):
        """
        이름 부분의 타입을 설정합니다.
        
        Args:
            inType: 설정할 타입 (NamePartType 열거형 값)
        """
        self._type = inType
        self._initialize_type_defaults()
    
    def get_type(self):
        """
        이름 부분의 타입을 반환합니다.
        
        Returns:
            이름 부분의 타입 (NamePartType 열거형 값)
        """
        return self._type
    
    def is_prefix(self):
        """
        이름 부분이 PREFIX 타입인지 확인합니다.
        
        Returns:
            PREFIX 타입이면 True, 아니면 False
        """
        return self._type == NamePartType.PREFIX
    
    def is_suffix(self):
        """
        이름 부분이 SUFFIX 타입인지 확인합니다.
        
        Returns:
            SUFFIX 타입이면 True, 아니면 False
        """
        return self._type == NamePartType.SUFFIX
    
    def is_realname(self):
        """
        이름 부분이 REALNAME 타입인지 확인합니다.
        
        Returns:
            REALNAME 타입이면 True, 아니면 False
        """
        return self._type == NamePartType.REALNAME
    
    def is_index(self):
        """
        이름 부분이 INDEX 타입인지 확인합니다.
        
        Returns:
            INDEX 타입이면 True, 아니면 False
        """
        return self._type == NamePartType.INDEX
    
    def add_predefined_value(self, inValue):
        """
        사전 선언된 값 목록에 새 값을 추가합니다.
        
        Args:
            inValue: 추가할 값
            
        Returns:
            추가 성공 여부 (이미 존재하는 경우 False)
        """
        # REALNAME이나 INDEX 타입인 경우 predefined values를 사용하지 않음
        if self._type == NamePartType.REALNAME or self._type == NamePartType.INDEX:
            return False
            
        if inValue not in self._predefinedValues:
            self._predefinedValues.append(inValue)
            return True
        return False
    
    def remove_predefined_value(self, inValue):
        """
        사전 선언된 값 목록에서 값을 제거합니다.
        
        Args:
            inValue: 제거할 값
            
        Returns:
            제거 성공 여부 (존재하지 않는 경우 False)
        """
        if inValue in self._predefinedValues:
            self._predefinedValues.remove(inValue)
            return True
        return False
    
    def set_predefined_values(self, inValues):
        """
        사전 선언된 값 목록을 설정합니다.
        
        Args:
            inValues: 설정할 값 목록
        """
        # REALNAME이나 INDEX 타입인 경우 predefined values를 사용하지 않음
        if self._type == NamePartType.REALNAME or self._type == NamePartType.INDEX:
            return
            
        self._predefinedValues = inValues.copy() if inValues else []
    
    def get_predefined_values(self):
        """
        사전 선언된 값 목록을 반환합니다.
        
        Returns:
            사전 선언된 값 목록
        """
        return self._predefinedValues.copy()
    
    def contains_value(self, inValue):
        """
        특정 값이 사전 선언된 값 목록에 있는지 확인합니다.
        
        Args:
            inValue: 확인할 값
            
        Returns:
            값이 존재하면 True, 아니면 False
        """
        # INDEX 타입인 경우 숫자인지 확인
        if self._type == NamePartType.INDEX:
            return isinstance(inValue, str) and inValue.isdigit()
            
        return inValue in self._predefinedValues
    
    def get_value_at_index(self, inIndex):
        """
        지정된 인덱스의 사전 선언된 값을 반환합니다.
        
        Args:
            inIndex: 값의 인덱스
            
        Returns:
            값 (인덱스가 범위를 벗어나면 None)
        """
        if 0 <= inIndex < len(self._predefinedValues):
            return self._predefinedValues[inIndex]
        return None
    
    def get_value_count(self):
        """
        사전 선언된 값의 개수를 반환합니다.
        
        Returns:
            값 개수
        """
        return len(self._predefinedValues)
    
    def clear_predefined_values(self):
        """
        모든 사전 선언된 값을 제거합니다.
        """
        # REALNAME이나 INDEX 타입인 경우 아무것도 하지 않음
        if self._type == NamePartType.REALNAME or self._type == NamePartType.INDEX:
            return
            
        self._predefinedValues.clear()
    
    # 새로 추가된 메서드들 - 시맨틱 매핑 관련
    
    def set_semantic_mapping(self, inMapping):
        """
        의미론적 매핑 또는 가중치를 설정합니다.
        
        Args:
            inMapping: 의미 또는 가중치의 딕셔너리
                   (예: {"L": "left", "R": "right"} 또는 {"P": 10, "Dum": 5})
        """
        # REALNAME이나 INDEX 타입인 경우 semantic mapping을 사용하지 않음
        if self._type == NamePartType.REALNAME or self._type == NamePartType.INDEX:
            return
            
        self._semanticMappings = inMapping.copy() if inMapping else {}
    
    def get_semantic_mapping(self):
        """
        의미론적 매핑 또는 가중치를 반환합니다.
        
        Returns:
            의미론적 매핑 또는 가중치 딕셔너리
        """
        return self._semanticMappings.copy()
    
    def add_semantic_mapping(self, inKey, inValue):
        """
        의미론적 매핑 또는 가중치에 항목을 추가합니다.
        
        Args:
            inKey: 매핑할 값 또는 이름
            inValue: 의미 또는 가중치 값
            
        Returns:
            추가 성공 여부
        """
        # REALNAME이나 INDEX 타입인 경우 semantic mapping을 사용하지 않음
        if self._type == NamePartType.REALNAME or self._type == NamePartType.INDEX:
            return False
            
        if inKey:
            self._semanticMappings[inKey] = inValue
            return True
        return False
    
    def get_value_by_semantic(self, inSemantic):
        """
        특정 의미에 해당하는 값을 반환합니다.
        
        Args:
            inSemantic: 찾고자 하는 의미 (예: "left", "right", "primary")
            
        Returns:
            해당 의미에 매핑된 값, 없으면 빈 문자열
        """
        for key, value in self._semanticMappings.items():
            if value == inSemantic and key in self._predefinedValues:
                return key
        return ""
    
    def get_value_by_weight(self, inRank=0):
        """
        가중치 순위에 따른 값을 반환합니다.
        
        Args:
            inRank: 가중치 순위 (0: 가장 높은 가중치, 1: 두 번째 가중치, 등)
            
        Returns:
            해당 순위의 가중치를 가진 값, 없으면 빈 문자열
        """
        weightedValues = []
        
        # 가중치가 숫자인 항목만 처리
        for value in self._predefinedValues:
            if value in self._semanticMappings and isinstance(self._semanticMappings[value], (int, float)):
                weightedValues.append((value, self._semanticMappings[value]))
        
        # 가중치가 없는 값들에는 기본 가중치 0 할당
        for value in self._predefinedValues:
            if value not in self._semanticMappings or not isinstance(self._semanticMappings[value], (int, float)):
                weightedValues.append((value, 0))
        
        # 가중치 내림차순 정렬 (높은 값이 더 중요)
        weightedValues.sort(key=lambda x: x[1], reverse=True)
        
        if 0 <= inRank < len(weightedValues):
            return weightedValues[inRank][0]
        return ""
    
    def get_sorted_values_by_weight(self):
        """
        가중치에 따라 정렬된 값 목록을 반환합니다.
        
        Returns:
            가중치 내림차순으로 정렬된 값 목록
        """
        weightedValues = []
        
        # 가중치가 숫자인 항목만 처리
        for value in self._predefinedValues:
            if value in self._semanticMappings and isinstance(self._semanticMappings[value], (int, float)):
                weightedValues.append((value, self._semanticMappings[value]))
        
        # 가중치가 없는 값들에는 기본 가중치 0 할당
        for value in self._predefinedValues:
            if value not in self._semanticMappings or not isinstance(self._semanticMappings[value], (int, float)):
                weightedValues.append((value, 0))
        
        # 가중치 내림차순 정렬 (높은 값이 더 중요)
        weightedValues.sort(key=lambda x: x[1], reverse=True)
        
        # 값만 반환
        return [item[0] for item in weightedValues]
    
    def get_most_different_weight_value(self, inValue):
        """
        주어진 값의 가중치와 가장 차이가 큰 값을 반환합니다.
        
        Args:
            inValue: 기준이 되는 값
            
        Returns:
            가중치 차이가 가장 큰 값, 없으면 빈 문자열
        """
        if not self._predefinedValues or len(self._predefinedValues) <= 1:
            return ""
            
        if inValue not in self._predefinedValues:
            return ""
            
        # 값의 가중치 가져오기
        currentWeight = 0
        if inValue in self._semanticMappings and isinstance(self._semanticMappings[inValue], (int, float)):
            currentWeight = self._semanticMappings[inValue]
            
        maxDiff = -1
        maxDiffValue = ""
        
        # 가중치 차이가 가장 큰 값 찾기
        for predValue in self._predefinedValues:
            if predValue == inValue:
                continue
                
            predWeight = 0
            if predValue in self._semanticMappings and isinstance(self._semanticMappings[predValue], (int, float)):
                predWeight = self._semanticMappings[predValue]
                
            diff = abs(currentWeight - predWeight)
            if diff > maxDiff:
                maxDiff = diff
                maxDiffValue = predValue
                
        return maxDiffValue
    
    def get_value_by_min_weight(self):
        """
        가중치가 가장 낮은 값을 반환합니다.
        
        Returns:
            가중치가 가장 낮은 값, 없으면 빈 문자열
        """
        sorted_values = self.get_sorted_values_by_weight()
        if sorted_values:
            return sorted_values[-1]  # 마지막 값이 가중치가 가장 낮은 값
        return ""
    
    def get_value_by_max_weight(self):
        """
        가중치가 가장 높은 값을 반환합니다.
        
        Returns:
            가중치가 가장 높은 값, 없으면 빈 문자열
        """
        sorted_values = self.get_sorted_values_by_weight()
        if sorted_values:
            return sorted_values[0]  # 첫 번째 값이 가중치가 가장 높은 값
        return ""
    
    def validate_value(self, inValue):
        """
        값이 이 NamePart 타입에 유효한지 검증합니다.
        
        Args:
            inValue: 검증할 값
            
        Returns:
            유효하면 True, 아니면 False
        """
        # INDEX 타입은 숫자 문자열만 유효
        if self._type == NamePartType.INDEX:
            return isinstance(inValue, str) and inValue.isdigit()
            
        # PREFIX와 SUFFIX 타입은 predefined values 중 하나여야 함
        if (self._type == NamePartType.PREFIX or self._type == NamePartType.SUFFIX) and self._predefinedValues:
            return inValue in self._predefinedValues
            
        # REALNAME 타입은 모든 문자열 유효
        if self._type == NamePartType.REALNAME:
            return isinstance(inValue, str)
            
        # 정의되지 않은 타입이면 기존 동작대로 처리
        return True
    
    def to_dict(self):
        """
        NamePart 객체를 사전 형태로 변환합니다.
        
        Returns:
            사전 형태의 NamePart 정보
        """
        return {
            "name": self._name,
            "predefinedValues": self._predefinedValues.copy(),
            "semanticMapping": self._semanticMappings.copy(),
            "type": self._type.name if hasattr(self._type, 'name') else str(self._type)
        }
    
    @staticmethod
    def from_dict(inData):
        """
        사전 형태의 데이터로부터 NamePart 객체를 생성합니다.
        
        Args:
            inData: 사전 형태의 NamePart 정보
            
        Returns:
            NamePart 객체
        """
        if isinstance(inData, dict) and "name" in inData:
            # 타입 변환 (문자열 -> NamePartType 열거형)
            type_str = inData.get("type", "UNDEFINED")
            try:
                part_type = NamePartType[type_str] if isinstance(type_str, str) else NamePartType.UNDEFINED
            except KeyError:
                part_type = NamePartType.UNDEFINED
                
            return NamePart(
                inData["name"],
                inData.get("predefinedValues", []),
                inData.get("semanticMapping", {}),
                part_type
            )
        return NamePart()
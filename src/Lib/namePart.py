#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
NamePart 클래스 모듈 - Naming 모듈의 일부
NamePart 클래스는 이름 부분을 관리하는 기능을 제공합니다.
이름과 해당 부분에 대한 사전 선언된 값들을 관리합니다.
"""

class NamePart:
    """
    이름 부분(name part)을 관리하기 위한 클래스.
    이름과 해당 부분에 대한 사전 선언된 값들을 관리합니다.
    """
    
    def __init__(self, inName="", inPredefinedValues=None, inSemanticMapping=None):
        """
        NamePart 클래스 초기화
        
        Args:
            inName: 이름 부분의 이름 (예: "Base", "Type", "Side" 등)
            inPredefinedValues: 사전 선언된 값 목록 (기본값: None, 빈 리스트로 초기화)
            inSemanticMapping: 의미론적 매핑 또는 가중치 딕셔너리
                           (예: {"L": "left", "R": "right"}, {"P": 10, "Dum": 5})
        """
        self._name = inName
        self._predefinedValues = inPredefinedValues if inPredefinedValues is not None else []
        self._semanticMappings = inSemanticMapping if inSemanticMapping is not None else 5
    
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
    
    def add_predefined_value(self, inValue):
        """
        사전 선언된 값 목록에 새 값을 추가합니다.
        
        Args:
            inValue: 추가할 값
            
        Returns:
            추가 성공 여부 (이미 존재하는 경우 False)
        """
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
        self._predefinedValues.clear()
    
    # 새로 추가된 메서드들 - 시맨틱 매핑 관련
    
    def set_semantic_mapping(self, inMapping):
        """
        의미론적 매핑 또는 가중치를 설정합니다.
        
        Args:
            inMapping: 의미 또는 가중치의 딕셔너리
                   (예: {"L": "left", "R": "right"} 또는 {"P": 10, "Dum": 5})
        """
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
    
    def to_dict(self):
        """
        NamePart 객체를 사전 형태로 변환합니다.
        
        Returns:
            사전 형태의 NamePart 정보
        """
        return {
            "name": self._name,
            "predefinedValues": self._predefinedValues.copy(),
            "semanticMapping": self._semanticMappings.copy()
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
            return NamePart(
                inData["name"],
                inData.get("predefinedValues", []),
                inData.get("semanticMapping", {})
            )
        return NamePart()

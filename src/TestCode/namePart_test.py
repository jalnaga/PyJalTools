#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
NamePart 클래스를 위한 테스트 모듈
"""

import sys
import os
import unittest

# 부모 디렉토리를 시스템 경로에 추가
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from namePart import NamePart


class TestNamePart(unittest.TestCase):
    """NamePart 클래스 테스트 케이스"""

    def setUp(self):
        """각 테스트 케이스 전에 실행되는 설정"""
        # 기본 NamePart 객체 생성
        self.empty_part = NamePart()
        
        # 이름만 있는 NamePart 객체
        self.name_only_part = NamePart("Side")
        
        # 사전 정의된 값이 있는 NamePart 객체
        self.predefined_part = NamePart("Side", ["L", "R", "C"])
        
        # 시맨틱 매핑이 있는 NamePart 객체
        self.semantic_part = NamePart(
            "Side", 
            ["L", "R", "C"], 
            {"L": "left", "R": "right", "C": "center"}
        )
        
        # 가중치 매핑이 있는 NamePart 객체
        self.weighted_part = NamePart(
            "Type", 
            ["P", "S", "H", "C"],
            {"P": 10, "S": 5, "H": 3, "C": 1}
        )

    def test_initialization(self):
        """초기화 테스트"""
        # 기본 초기화
        self.assertEqual(self.empty_part.get_name(), "")
        self.assertEqual(self.empty_part.get_predefined_values(), [])
        
        # 이름만 초기화
        self.assertEqual(self.name_only_part.get_name(), "Side")
        self.assertEqual(self.name_only_part.get_predefined_values(), [])
        
        # 이름과 사전 정의된 값으로 초기화
        self.assertEqual(self.predefined_part.get_name(), "Side")
        self.assertEqual(self.predefined_part.get_predefined_values(), ["L", "R", "C"])
        
        # 이름, 사전 정의된 값, 시맨틱 매핑으로 초기화
        self.assertEqual(self.semantic_part.get_name(), "Side")
        self.assertEqual(self.semantic_part.get_predefined_values(), ["L", "R", "C"])
        expected_mapping = {"L": "left", "R": "right", "C": "center"}
        self.assertEqual(self.semantic_part.get_semantic_mapping(), expected_mapping)

    def test_name_operations(self):
        """이름 관련 메서드 테스트"""
        # 이름 설정
        self.empty_part.set_name("Direction")
        self.assertEqual(self.empty_part.get_name(), "Direction")
        
        # 이름 변경
        self.name_only_part.set_name("Position")
        self.assertEqual(self.name_only_part.get_name(), "Position")

    def test_predefined_values_operations(self):
        """사전 정의된 값 관련 메서드 테스트"""
        # 값 추가
        result = self.empty_part.add_predefined_value("Test")
        self.assertTrue(result)
        self.assertEqual(self.empty_part.get_predefined_values(), ["Test"])
        
        # 이미 존재하는 값 추가 시도
        result = self.predefined_part.add_predefined_value("L")
        self.assertFalse(result)
        self.assertEqual(self.predefined_part.get_predefined_values(), ["L", "R", "C"])
        
        # 새로운 값 추가
        result = self.predefined_part.add_predefined_value("M")
        self.assertTrue(result)
        self.assertEqual(self.predefined_part.get_predefined_values(), ["L", "R", "C", "M"])
        
        # 값 제거
        result = self.predefined_part.remove_predefined_value("M")
        self.assertTrue(result)
        self.assertEqual(self.predefined_part.get_predefined_values(), ["L", "R", "C"])
        
        # 존재하지 않는 값 제거 시도
        result = self.predefined_part.remove_predefined_value("X")
        self.assertFalse(result)
        
        # 값 목록 설정
        new_values = ["F", "B", "S"]
        self.predefined_part.set_predefined_values(new_values)
        self.assertEqual(self.predefined_part.get_predefined_values(), new_values)
        
        # 값 포함 여부 확인
        self.assertTrue(self.predefined_part.contains_value("F"))
        self.assertFalse(self.predefined_part.contains_value("L"))
        
        # 인덱스로 값 가져오기
        self.assertEqual(self.predefined_part.get_value_at_index(0), "F")
        self.assertEqual(self.predefined_part.get_value_at_index(2), "S")
        self.assertIsNone(self.predefined_part.get_value_at_index(5))
        
        # 값 개수 확인
        self.assertEqual(self.predefined_part.get_value_count(), 3)
        
        # 값 목록 초기화
        self.predefined_part.clear_predefined_values()
        self.assertEqual(self.predefined_part.get_predefined_values(), [])
        self.assertEqual(self.predefined_part.get_value_count(), 0)

    def test_semantic_mapping_operations(self):
        """시맨틱 매핑 관련 메서드 테스트"""
        # 매핑 설정
        new_mapping = {"A": "after", "B": "before"}
        self.empty_part.set_semantic_mapping(new_mapping)
        self.assertEqual(self.empty_part.get_semantic_mapping(), new_mapping)
        
        # 매핑 항목 추가
        self.semantic_part.add_semantic_mapping("M", "middle")
        expected_mapping = {"L": "left", "R": "right", "C": "center", "M": "middle"}
        self.assertEqual(self.semantic_part.get_semantic_mapping(), expected_mapping)
        
        # 의미에 대응하는 값 가져오기
        self.semantic_part.add_predefined_value("M")
        self.assertEqual(self.semantic_part.get_value_by_semantic("left"), "L")
        self.assertEqual(self.semantic_part.get_value_by_semantic("center"), "C")
        self.assertEqual(self.semantic_part.get_value_by_semantic("unknown"), "")

    def test_weight_operations(self):
        """가중치 관련 메서드 테스트"""
        # 가중치 순위에 따른 값 가져오기
        self.assertEqual(self.weighted_part.get_value_by_weight(0), "P")  # 최고 가중치
        self.assertEqual(self.weighted_part.get_value_by_weight(1), "S")  # 두 번째 가중치
        self.assertEqual(self.weighted_part.get_value_by_weight(3), "C")  # 가장 낮은 가중치
        self.assertEqual(self.weighted_part.get_value_by_weight(10), "")  # 범위 벗어남
        
        # 가중치 순으로 정렬된 값 목록 가져오기
        sorted_values = self.weighted_part.get_sorted_values_by_weight()
        self.assertEqual(sorted_values, ["P", "S", "H", "C"])
        
        # 가중치 없는 항목 추가 후 정렬 테스트
        self.weighted_part.add_predefined_value("N")  # 가중치 없음
        sorted_values = self.weighted_part.get_sorted_values_by_weight()
        self.assertEqual(sorted_values, ["P", "S", "H", "C", "N"])  # 가중치 없는 항목은 맨 뒤에 정렬

    def test_serialization(self):
        """직렬화 메서드 테스트"""
        # to_dict 테스트
        data = self.semantic_part.to_dict()
        expected = {
            "name": "Side",
            "predefinedValues": ["L", "R", "C"],
            "semanticMapping": {"L": "left", "R": "right", "C": "center"}
        }
        self.assertEqual(data, expected)
        
        # from_dict 테스트
        new_part = NamePart.from_dict(data)
        self.assertEqual(new_part.get_name(), "Side")
        self.assertEqual(new_part.get_predefined_values(), ["L", "R", "C"])
        self.assertEqual(new_part.get_semantic_mapping(), {"L": "left", "R": "right", "C": "center"})
        
        # 잘못된 데이터로 from_dict 테스트
        invalid_part = NamePart.from_dict(None)
        self.assertEqual(invalid_part.get_name(), "")
        self.assertEqual(invalid_part.get_predefined_values(), [])
        
        invalid_part = NamePart.from_dict({})
        self.assertEqual(invalid_part.get_name(), "")
        self.assertEqual(invalid_part.get_predefined_values(), [])


if __name__ == "__main__":
    unittest.main()

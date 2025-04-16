#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Naming 클래스를 위한 테스트 모듈
get_char_type부터 get_nub 메소드까지에 대한 테스트 케이스 포함
"""

import sys
import os
import math
import importlib
import unittest

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "JalLib", ".."))
print(f"JalLib root_dir: {root_dir}")
if root_dir not in sys.path:
    sys.path.append(root_dir)

import JalLib
import JalLib.max.header
import JalLib.max.name
importlib.reload(JalLib)
importlib.reload(JalLib.max.header)
importlib.reload(JalLib.max.name)
from JalLib.max.name import Name

# tests 디렉토리를 sys.path에 추가
tests_dir = os.path.dirname(os.path.abspath(__file__))
if tests_dir not in sys.path:
    sys.path.append(tests_dir)

from reload_modules import reload_jaltools_modules
reload_jaltools_modules()


class NamingTest(unittest.TestCase):
    """Naming 클래스 테스트를 위한 테스트 케이스 클래스"""

    def setUp(self):
        """각 테스트 케이스 실행 전 초기화"""
        # 각 테스트 케이스마다 모듈 다시 로드
        importlib.reload(JalLib.naming)
        
        self.name = Name()  # 설정 파일 없이 기본 설정으로 초기화
        
        # 테스트에 사용할 이름 샘플
        self.test_names = [
            "Bip001 L Forearm",      # 공백 구분
            "b_L_Thigh_00",          # 언더스코어 구분
            "Sphere01",              # 구분자 없음
            "Box 01",                # 공백 구분
            "b_Dum_R_F_R_Skirt_Nub", # 복합적인 케이스
            "b_P_F_L_Sleeve_00"      # 복합적인 케이스
        ]
        
    def test(self):
        self.assertEqual(self.name.convert_name_to_array("b_Dum_R_F_R_Skirt_Nub"), ["b", "Dum", "R", "F", "R_Skirt", "", "Nub"])
        self.assertEqual(self.name.get_RealName("b_Dum_R_F_R_Skirt_Nub"), "R_Skirt")
        namePart = self.name.get_name_part("Type")
        self.assertEqual(namePart.get_predefined_values(), ["P", "Dum", "Exp", "IK", "T"])
        self.assertEqual(namePart._weights, [5, 10, 15, 20, 25])
        self.assertEqual(namePart.get_value_by_description("Dummy"), "Dum")
        self.assertEqual(namePart.get_description_by_value("Dum"), "Dummy")
        self.assertEqual(namePart.get_value_by_max_weight(), "T")
        


if __name__ == "__main__":
    unittest.main()
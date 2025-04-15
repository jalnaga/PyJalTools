#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Naming 클래스를 위한 테스트 모듈
get_char_type부터 get_nub 메소드까지에 대한 테스트 케이스 포함
"""

import unittest
import importlib
import JalLib.naming
# 모듈 실행 시 JalLib.naming을 리로드
importlib.reload(JalLib.naming)
from JalLib.naming import Naming


class NamingTest(unittest.TestCase):
    """Naming 클래스 테스트를 위한 테스트 케이스 클래스"""

    def setUp(self):
        """각 테스트 케이스 실행 전 초기화"""
        # 각 테스트 케이스마다 모듈 다시 로드
        importlib.reload(JalLib.naming)
        
        self.naming = Naming()  # 설정 파일 없이 기본 설정으로 초기화
        
        # 테스트에 사용할 이름 샘플
        self.test_names = [
            "Bip001 L Forearm",      # 공백 구분
            "b_L_Thigh_00",          # 언더스코어 구분
            "Sphere01",              # 구분자 없음
            "Box 01",                # 공백 구분
            "b_Dum_R_F_R_Skirt_Nub", # 복합적인 케이스
            "b_P_F_L_Sleeve_00"      # 복합적인 케이스
        ]
        
    def test_get_char_type(self):
        self.assertEqual(self.naming.convert_name_to_array("b_Dum_R_F_R_Skirt_Nub"), ["b", "Dum", "R", "F", "R_Skirt", "", "Nub"])
        self.assertEqual(self.naming.get_real_name("b_Dum_R_F_R_Skirt_Nub"), "R_Skirt")
        namePart = self.naming.get_name_part("Type")
        self.assertEqual(namePart.get_predefined_values(), ["P", "Dum", "Exp", "IK", "T"])
        self.assertEqual(namePart.get_value_by_weight(1), "P")


if __name__ == "__main__":
    unittest.main()
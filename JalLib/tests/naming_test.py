#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Naming 클래스를 위한 테스트 모듈
get_char_type부터 get_nub 메소드까지에 대한 테스트 케이스 포함
"""

import unittest
import importlib
from JalLib.naming import Naming


class NamingTest(unittest.TestCase):
    """Naming 클래스 테스트를 위한 테스트 케이스 클래스"""

    def setUp(self):
        """각 테스트 케이스 실행 전 초기화"""
        # 모듈 다시 로드
        import JalLib.naming
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
        """get_char_type 메소드 테스트"""
        # 기본 문자 유형 테스트
        self.assertEqual(self.naming.get_char_type("L"), "Side")
        self.assertEqual(self.naming.get_char_type("R"), "Side")
        self.assertEqual(self.naming.get_char_type("F"), "FrontBack")
        self.assertEqual(self.naming.get_char_type("B"), "FrontBack")
        self.assertEqual(self.naming.get_char_type("P"), "Type")
        self.assertEqual(self.naming.get_char_type("Dum"), "Type")
        self.assertEqual(self.naming.get_char_type("b"), "Base")
        self.assertEqual(self.naming.get_char_type("Bip001"), "Base")
        self.assertEqual(self.naming.get_char_type("Nub"), "Nub")
        
        # 숫자(인덱스) 테스트
        self.assertEqual(self.naming.get_char_type("01"), "Index")
        self.assertEqual(self.naming.get_char_type("1"), "Index")
        self.assertEqual(self.naming.get_char_type("123"), "Index")
        
        # 유형이 아닌 문자 테스트
        self.assertIsNone(self.naming.get_char_type("Arm"))
        self.assertIsNone(self.naming.get_char_type("Forearm"))
        self.assertIsNone(self.naming.get_char_type(""))
        
        # 커스텀 정의 테스트
        custom_naming = Naming()
        side_part = custom_naming.get_name_part("Side")
        if side_part:
            side_part._predefinedValues = ["X", "Y"]
            
        self.assertEqual(custom_naming.get_char_type("X"), "Side")
        self.assertEqual(custom_naming.get_char_type("Y"), "Side")
        self.assertIsNone(custom_naming.get_char_type("L"))  # 더 이상 Side로 인식되지 않음

    def test_get_side(self):
        """get_side 메소드 테스트"""
        # 기본 이름 샘플에서의 Side 추출 테스트
        self.assertEqual(self.naming.get_side("Bip001 L Forearm"), "L")
        self.assertEqual(self.naming.get_side("b_L_Thigh_00"), "L")
        self.assertEqual(self.naming.get_side("b_Dum_R_F_R_Skirt_Nub"), "R")
        self.assertEqual(self.naming.get_side("b_P_F_L_Sleeve_00"), "L")
        
        # Side가 없는 이름 테스트
        self.assertEqual(self.naming.get_side("Sphere01"), "")
        self.assertEqual(self.naming.get_side("Box 01"), "")
        
        # 사용자 정의 Side 테스트
        custom_naming = Naming()
        side_part = custom_naming.get_name_part("Side")
        if side_part:
            side_part._predefinedValues = ["X", "Y"]
            
        self.assertEqual(custom_naming.get_side("Test_X_Name"), "X")
        self.assertEqual(custom_naming.get_side("Test Y Name"), "Y")
        self.assertEqual(custom_naming.get_side("b_L_Thigh_00"), "")  # L은 더 이상 Side로 인식되지 않음

    def test_get_base(self):
        """get_base 메소드 테스트"""
        # 기본 이름 샘플에서의 Base 추출 테스트
        self.assertEqual(self.naming.get_base("Bip001 L Forearm"), "Bip001")
        self.assertEqual(self.naming.get_base("b_L_Thigh_00"), "b")
        self.assertEqual(self.naming.get_base("b_Dum_R_F_R_Skirt_Nub"), "b")
        self.assertEqual(self.naming.get_base("b_P_F_L_Sleeve_00"), "b")
        
        # Base가 없는 이름 테스트
        self.assertEqual(self.naming.get_base("Sphere01"), "")
        self.assertEqual(self.naming.get_base("Box 01"), "")
        
        # 사용자 정의 Base 테스트
        custom_naming = Naming()
        base_part = custom_naming.get_name_part("Base")
        if base_part:
            base_part._predefinedValues = ["myBase", "custom"]
            
        self.assertEqual(custom_naming.get_base("myBase_Test_Name"), "myBase")
        self.assertEqual(custom_naming.get_base("custom Test Name"), "custom")
        self.assertEqual(custom_naming.get_base("b_L_Thigh_00"), "")  # b는 더 이상 Base로 인식되지 않음

    def test_get_type(self):
        """get_type 메소드 테스트"""
        # 기본 이름 샘플에서의 Type 추출 테스트
        self.assertEqual(self.naming.get_type("b_Dum_R_F_R_Skirt_Nub"), "Dum")
        self.assertEqual(self.naming.get_type("b_P_F_L_Sleeve_00"), "P")
        self.assertEqual(self.naming.get_type("b_IK_Arm_01"), "IK")
        
        # Type이 없는 이름 테스트
        self.assertEqual(self.naming.get_type("Bip001 L Forearm"), "")
        self.assertEqual(self.naming.get_type("b_L_Thigh_00"), "")
        self.assertEqual(self.naming.get_type("Sphere01"), "")
        
        # 사용자 정의 Type 테스트
        custom_naming = Naming()
        type_part = custom_naming.get_name_part("Type")
        if type_part:
            type_part._predefinedValues = ["MyType", "Custom"]
            
        self.assertEqual(custom_naming.get_type("b_MyType_Test_Name"), "MyType")
        self.assertEqual(custom_naming.get_type("b_Custom_Test_Name"), "Custom")
        self.assertEqual(custom_naming.get_type("b_P_F_L_Sleeve_00"), "")  # P는 더 이상 Type으로 인식되지 않음

    def test_get_front_back(self):
        """get_front_back 메소드 테스트"""
        # 기본 이름 샘플에서의 FrontBack 추출 테스트
        self.assertEqual(self.naming.get_front_back("b_Dum_R_F_R_Skirt_Nub"), "F")
        self.assertEqual(self.naming.get_front_back("b_P_F_L_Sleeve_00"), "F")
        self.assertEqual(self.naming.get_front_back("b_T_B_R_Arm_01"), "B")
        
        # FrontBack이 없는 이름 테스트
        self.assertEqual(self.naming.get_front_back("Bip001 L Forearm"), "")
        self.assertEqual(self.naming.get_front_back("b_L_Thigh_00"), "")
        self.assertEqual(self.naming.get_front_back("Sphere01"), "")
        
        # 사용자 정의 FrontBack 테스트
        custom_naming = Naming()
        fb_part = custom_naming.get_name_part("FrontBack")
        if fb_part:
            fb_part._predefinedValues = ["Front", "Back"]
            
        self.assertEqual(custom_naming.get_front_back("b_T_Front_L_Arm"), "Front")
        self.assertEqual(custom_naming.get_front_back("b_T_Back_R_Leg"), "Back")
        self.assertEqual(custom_naming.get_front_back("b_P_F_L_Sleeve_00"), "")  # F는 더 이상 FrontBack으로 인식되지 않음

    def test_get_name(self):
        """get_name 메소드 테스트"""
        # 다양한 namePart에 대한 get_name 메소드 테스트
        test_name = "b_Dum_R_F_R_Skirt_Nub"
        
        # 각 부분 추출 테스트
        self.assertEqual(self.naming.get_name("Base", test_name), "b")
        self.assertEqual(self.naming.get_name("Type", test_name), "Dum")
        self.assertEqual(self.naming.get_name("Side", test_name), "R")
        self.assertEqual(self.naming.get_name("FrontBack", test_name), "F")
        self.assertEqual(self.naming.get_name("Nub", test_name), "Nub")
        
        # 존재하지 않는 부분 요청 테스트
        self.assertEqual(self.naming.get_name("NonExistent", test_name), "")
        
        # 복잡한 이름 테스트 - 앞에서부터 vs 뒤에서부터 검색
        test_name2 = "b_R_P_R_F_Name_00"  # Side(R)가 여러 번 등장
        
        # namePart 인덱스와 real_name 인덱스에 따라 앞에서 또는 뒤에서 검색
        # Side는 RealName 앞에 있으므로 앞에서부터 검색 (첫 번째 "R" 반환)
        self.assertEqual(self.naming.get_name("Side", test_name2), "R")

    def test_get_index(self):
        """get_index 메소드 테스트"""
        # 기본 이름 샘플에서의 인덱스 추출 테스트 
        # 참고: get_index는 namePart에 정의된 인덱스를 찾는 것이지
        # 문자열에서 숫자를 찾는 것이 아님
        self.assertEqual(self.naming.get_index("b_L_Thigh_00"), "00")
        
        # 인덱스가 없는 이름 테스트
        self.assertEqual(self.naming.get_index("Arm"), "")
        self.assertEqual(self.naming.get_index("b_L_Arm"), "")
        
        # Nub가 있는 경우 테스트
        self.assertEqual(self.naming.get_index("b_Dum_R_F_R_Skirt_Nub"), "")  # Nub가 있으면 인덱스는 없음
        
        # 참고: Sphere01와 같은 이름은 구분자가 없는 경우 
        # _split_to_array 로직에 따라 다르게 처리될 수 있음

    def test_get_nub(self):
        """get_nub 메소드 테스트"""
        # 기본 이름 샘플에서의 Nub 추출 테스트
        self.assertEqual(self.naming.get_nub("b_Dum_R_F_R_Skirt_Nub"), "Nub")
        
        # Nub가 없는 이름 테스트
        self.assertEqual(self.naming.get_nub("Bip001 L Forearm"), "")
        self.assertEqual(self.naming.get_nub("b_L_Thigh_00"), "")
        self.assertEqual(self.naming.get_nub("Sphere01"), "")
        self.assertEqual(self.naming.get_nub("b_P_F_L_Sleeve_00"), "")
        
        # 사용자 정의 Nub 테스트
        custom_naming = Naming()
        nub_part = custom_naming.get_name_part("Nub")
        if nub_part:
            nub_part._predefinedValues = ["End", "Tip"]
            
        self.assertEqual(custom_naming.get_nub("b_T_L_Arm_End"), "End")
        self.assertEqual(custom_naming.get_nub("b_T_R_Leg_Tip"), "Tip")
        self.assertEqual(custom_naming.get_nub("b_Dum_R_F_R_Skirt_Nub"), "")  # Nub는 더 이상 인식되지 않음

    def test_complex_name_cases(self):
        """복잡한 이름 케이스에 대한 통합 테스트"""
        # 여러 측면(Side) 부분이 있는 복잡한 이름
        complex_name = "b_L_R_F_B_Complex_01"
        
        # nameParts의 순서와 우선순위에 따라 올바르게 파싱되는지 테스트
        self.assertEqual(self.naming.get_base(complex_name), "b")
        self.assertEqual(self.naming.get_side(complex_name), "L")  # 첫 번째 L이 Side로 인식
        self.assertEqual(self.naming.get_front_back(complex_name), "")
        self.assertEqual(self.naming.get_real_name(complex_name), "R_F_B_Complex")  # 나머지는 RealName으로 인식
        self.assertEqual(self.naming.get_index(complex_name), "01")
        
        # 실제 같은 요소가 여러 번 나타나는 복잡한 이름
        complex_name2 = "b_P_R_F_Right_Front_00"
        
        # nameParts의 순서와 우선순위에 따라 올바르게 파싱되는지 테스트
        self.assertEqual(self.naming.get_base(complex_name2), "b")
        self.assertEqual(self.naming.get_type(complex_name2), "P")
        self.assertEqual(self.naming.get_side(complex_name2), "R")  # 첫 번째 R만 Side로 인식
        self.assertEqual(self.naming.get_front_back(complex_name2), "F")  # 첫 번째 F만 FrontBack으로 인식
        self.assertEqual(self.naming.get_real_name(complex_name2), "Right_Front")  # Right, Front와 인덱스는 RealName으로 인식
        self.assertEqual(self.naming.get_index(complex_name2), "00")


if __name__ == "__main__":
    unittest.main()
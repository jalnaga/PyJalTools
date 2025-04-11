#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
naming.py 모듈을 테스트하는 코드
제공된 이름들을 사용하여 Naming 클래스의 다양한 기능 테스트
"""

import sys
import os
import importlib

# JalTools 패키지를 임포트할 수 있도록 경로 설정
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.append(root_dir)

# JalTools.Lib에서 필요한 클래스 임포트
from JalTools.Lib.naming import Naming
from JalTools.Lib.namePart import NamePart


# 테스트에 사용할 이름 목록 - 사용자가 수정하기 쉽도록 전역 변수로 정의
TEST_NAMES = [
    "b_P_L_R_SkirtA_02",
    "b_Exp_R_F_SkirtArmor_A",
    "b_L_F_Target_Nub"
]

def run_tests():
    """명명 규칙 테스트 실행"""
    print("===== Naming 모듈 테스트 시작 =====")
    
    # Naming 인스턴스 생성
    jalNaming = Naming()
    
    # 각 테스트 이름에 대한 테스트 실행
    for name in TEST_NAMES:
        print(f"Name: {name}")
        
        # 이름을 배열로 변환
        nameArray = jalNaming.convert_name_to_array(name)
        print(f"NameArray: {nameArray}")
        
        # 이름을 딕셔너리로 변환
        nameDict = jalNaming.convert_to_dictionary(name)
        
        # 구분자 찾기
        filChar = jalNaming._get_filtering_char(name)
        
        # 각 이름 부분의 유형 출력
        for namePart in nameArray:
            nameType = jalNaming.get_char_type(namePart)
            if nameType is None and namePart == jalNaming.get_real_name(name):
                nameType = "RealName"
            print(f"NamePart: {namePart} / NameType: {nameType}")
        
        # 딕셔너리 출력
        print(f"NameDict: {nameDict}")
        
        # 딕셔너리에서 이름 다시 조합
        combinedName = jalNaming.combine(nameDict, inFilChar=filChar)
        print(f"Combined Name: {combinedName}")
        
        # 테스트 분리선
        print("=====================")
    
    print("===== Naming 모듈 테스트 완료 =====")

# 이 파일이 직접 실행될 때만 테스트 실행
if __name__ == "__main__":
    run_tests()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
naming.py 모듈을 테스트하는 코드
제공된 이름들을 사용하여 Naming 클래스의 다양한 기능 테스트
"""

import sys
import os
import importlib

# 상위 디렉토리 경로 추가하여 naming 모듈 임포트 가능하게 설정
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 모듈 전체를 import하고 reload
import naming
import namePart
import namingConfig

# 모듈들을 항상 reload하여 최신 상태 유지
importlib.reload(naming)
importlib.reload(namePart)
importlib.reload(namingConfig)

# reload 후에 필요한 클래스 import
from naming import Naming
from namePart import NamePart


# 테스트에 사용할 이름 목록 - 사용자가 수정하기 쉽도록 전역 변수로 정의
TEST_NAMES = [
    "b_P_L_R_SkirtA_02",
    "b_Exp_R_F_SkirtArmor_A",
    "b_L_F_Target_Nub"
]

jalNaming = Naming()

for name in TEST_NAMES:
    print(f"Name: {name}")
    nameArray = jalNaming.convert_name_to_array(name)
    print(f"NameArray: {nameArray}")
    nameDict = jalNaming.convert_to_dictionary(name)
    filChar = jalNaming._get_filtering_char(name)
    for namePart in nameArray:
        nameType = jalNaming.get_char_type(namePart)
        if nameType is None and namePart == jalNaming.get_real_name(name):
            nameType = "RealName"
        print(f"NamePart: {namePart} / NameType: {nameType}")
    print(f"NameDict: {nameDict}")
    combinedName = jalNaming.combine(nameDict, inFilChar=filChar)
    print(f"Combined Name: {combinedName}")
    print("=====================")

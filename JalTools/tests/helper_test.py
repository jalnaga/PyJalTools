#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Helper 모듈 테스트 코드
3DS Max 내에서 직접 실행하기 위한 테스트 코드
"""

import sys
import os
import importlib
from pymxs import runtime as rt

# JalTools 패키지를 임포트할 수 있도록 경로 설정
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.append(root_dir)

# JalTools.Lib에서 Helper 클래스 임포트
from JalTools.Lib.helper import Helper

# Helper 인스턴스 생성
jalHelper = Helper()

# 테스트용 객체 리스트 초기화
testSpheres = [rt.getNodeByName("Sphere001"), rt.getNodeByName("Sphere002"), rt.getNodeByName("Sphere003")]
testHelpers = [rt.getNodeByName("Point001"), rt.getNodeByName("Point002"), rt.getNodeByName("Point003")]
testBones = [rt.getNodeByName("Bone001"), rt.getNodeByName("Bone002"), rt.getNodeByName("Bone003")]

# create_point 함수 테스트
def test_create_point():
    print("create_point 테스트 시작")
    try:
        point = jalHelper.create_point(
            "TestPoint",
            size=3,
            boxToggle=True,
            crossToggle=False,
            pointColor=(255, 0, 0),
            pos=(10, 10, 0)
        )
        print("생성된 포인트:", point)
        print("create_point 테스트 완료")
    except Exception as e:
        print("create_point 테스트 중 오류:", e)

# create_empty_point 함수 테스트
def test_create_empty_point():
    print("create_empty_point 테스트 시작")
    try:
        emptyPoint = jalHelper.create_empty_point("EmptyTestPoint")
        print("생성된 빈 포인트:", emptyPoint)
        print("create_empty_point 테스트 완료")
    except Exception as e:
        print("create_empty_point 테스트 중 오류:", e)

# create_helper 함수 테스트
def test_create_helper():
    # 먼저 테스트 구체를 선택
    if None not in testSpheres:
        print("create_helper 테스트 시작")
        try:
            rt.select(testSpheres)
            helpers = jalHelper.create_helper()
            print("생성된 헬퍼 개수:", len(helpers))
            print("create_helper 테스트 완료")
        except Exception as e:
            print("create_helper 테스트 중 오류:", e)
    else:
        print("create_helper 테스트를 위한 테스트 구체가 없습니다.")

# create_parent_helper 함수 테스트
def test_create_parent_helper():
    # 먼저 테스트 구체를 선택
    if None not in testSpheres:
        print("create_parent_helper 테스트 시작")
        try:
            rt.select(testSpheres)
            jalHelper.create_parent_helper()
            print("create_parent_helper 테스트 완료")
        except Exception as e:
            print("create_parent_helper 테스트 중 오류:", e)
    else:
        print("create_parent_helper 테스트를 위한 테스트 구체가 없습니다.")

# create_exp_tm 함수 테스트
def test_create_exp_tm():
    # 먼저 테스트 구체를 선택
    if None not in testSpheres:
        print("create_exp_tm 테스트 시작")
        try:
            rt.select(testSpheres)
            expTms = jalHelper.create_exp_tm()
            print("생성된 ExposeTM 개수:", len(expTms))
            print("create_exp_tm 테스트 완료")
        except Exception as e:
            print("create_exp_tm 테스트 중 오류:", e)
    else:
        print("create_exp_tm 테스트를 위한 테스트 구체가 없습니다.")

# 헬퍼 크기 관련 함수 테스트
def test_size_functions():
    # 테스트 헬퍼를 사용
    if None not in testHelpers:
        helper = testHelpers[0]
        print("set_size/add_size 테스트 시작")
        try:
            originalSize = helper.size
            print("원래 크기:", originalSize)
            
            # 크기 설정 테스트
            jalHelper.set_size(helper, 5.0)
            print("set_size 후 크기:", helper.size)
            
            # 크기 증가 테스트
            jalHelper.add_size(helper, 2.0)
            print("add_size 후 크기:", helper.size)
            
            # 원래 크기로 복원
            jalHelper.set_size(helper, originalSize)
            print("크기 복원 후:", helper.size)
            
            print("set_size/add_size 테스트 완료")
        except Exception as e:
            print("set_size/add_size 테스트 중 오류:", e)
    else:
        print("size 함수 테스트를 위한 테스트 헬퍼가 없습니다.")

# 형태 변경 테스트
def test_shape_functions():
    # 테스트 헬퍼를 사용
    if None not in testHelpers:
        helper = testHelpers[0]
        print("형태 변경 함수 테스트 시작")
        try:
            # 박스 형태로 설정
            jalHelper.set_shape_to_box(helper)
            print("set_shape_to_box 적용됨")
            
            # 십자 형태로 설정
            jalHelper.set_shape_to_cross(helper)
            print("set_shape_to_cross 적용됨")
            
            # 센터 형태로 설정
            jalHelper.set_shape_to_center(helper)
            print("set_shape_to_center 적용됨")
            
            # 축 형태로 설정
            jalHelper.set_shape_to_axis(helper)
            print("set_shape_to_axis 적용됨")
            
            print("형태 변경 테스트 완료")
        except Exception as e:
            print("형태 변경 테스트 중 오류:", e)
    else:
        print("형태 변경 테스트를 위한 테스트 헬퍼가 없습니다.")

# 테스트 실행 함수
def run_tests():
    print("===== Helper 모듈 테스트 시작 =====")
    test_create_point()
    test_create_empty_point()
    test_create_helper()
    test_create_parent_helper()
    test_create_exp_tm()
    test_size_functions()
    test_shape_functions()
    print("===== Helper 모듈 테스트 완료 =====")

# 이 파일이 직접 실행될 때만 테스트 실행
if __name__ == "__main__":
    run_tests()

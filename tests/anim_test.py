#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
anim.py 모듈 테스트 코드
3DS Max 내에서 실행 가능하도록 작성됨
"""

import os
import sys
import importlib
from pymxs import runtime as rt

# JalLib 패키지를 임포트할 수 있도록 경로 설정
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if root_dir not in sys.path:
    sys.path.append(root_dir)
    
import JalLib
import JalLib.max.anim
importlib.reload(JalLib)
importlib.reload(JalLib.max.anim)

# JalLib 모듈 리로드
from JalLib.tests import reload_jaltools_modules
reload_jaltools_modules()

from JalLib.max.anim import Anim

# Anim 인스턴스 생성
jalAnim = Anim()

# 테스트에 사용할 노드들 불러오기
testObj    = rt.getNodeByName("testObj")
teapot     = rt.getNodeByName("Teapot001")
targetObj1 = rt.getNodeByName("target01")
targetObj2 = rt.getNodeByName("target02")
targetObjs = (targetObj1, targetObj2, teapot)

# rotate_local 함수 테스트
def test_rotate_local():
    if testObj is None:
        print("testObj를 찾을 수 없습니다.")
        return
    print("rotate_local 테스트 시작")
    try:
        # X축을 기준으로 45도 회전 적용
        jalAnim.rotate_local(testObj, 45, 0, 0)
        print("rotate_local 적용 완료")
    except Exception as e:
        print("rotate_local 테스트 중 오류:", e)

# move_local 함수 테스트
def test_move_local():
    if testObj is None:
        print("testObj를 찾을 수 없습니다.")
        return
    print("move_local 테스트 시작")
    try:
        # X축으로 10 단위 이동 적용
        jalAnim.move_local(testObj, 10, 0, 0)
        print("move_local 적용 완료")
    except Exception as e:
        print("move_local 테스트 중 오류:", e)

# collape_anim_transform 함수 테스트
def test_collapse_anim_transform():
    if testObj is None:
        print("testObj를 찾을 수 없습니다.")
        return
    print("collape_anim_transform 테스트 시작")
    try:
        jalAnim.collape_anim_transform(testObj)
        print("collape_anim_transform 적용 완료")
    except Exception as e:
        print("collape_anim_transform 테스트 중 오류:", e)

# match_anim_transform 함수 테스트
def test_match_anim_transform():
    if testObj is None or targetObj1 is None:
        print("testObj 또는 targetObj1을 찾을 수 없습니다.")
        return
    print("match_anim_transform 테스트 시작")
    try:
        jalAnim.match_anim_transform(testObj, targetObj1)
        print("match_anim_transform 적용 완료")
    except Exception as e:
        print("match_anim_transform 테스트 중 오류:", e)

# create_average_pos_transform, create_average_rot_transform 테스트
def test_create_average_transforms():
    if not all(targetObjs):
        print("평균 변환 테스트를 위한 필요한 노드가 부족합니다.")
        return
    print("create_average_pos_transform 테스트 시작")
    try:
        avgPos = jalAnim.create_average_pos_transform(targetObjs)
        print("계산된 평균 위치 변환 행렬:", avgPos)
    except Exception as e:
        print("create_average_pos_transform 테스트 중 오류:", e)
    
    print("create_average_rot_transform 테스트 시작")
    try:
        avgRot = jalAnim.create_average_rot_transform(targetObjs)
        print("계산된 평균 회전 변환 행렬:", avgRot)
    except Exception as e:
        print("create_average_rot_transform 테스트 중 오류:", e)

# 키프레임 관련 함수들 테스트
def test_key_functions():
    if testObj is None:
        print("testObj를 찾을 수 없습니다.")
        return
    print("get_all_keys 테스트 시작")
    try:
        keys = jalAnim.get_all_keys(testObj)
        print("키프레임 개수:", len(keys))
    except Exception as e:
        print("get_all_keys 테스트 중 오류:", e)
    
    print("delete_all_keys 테스트 시작")
    try:
        jalAnim.delete_all_keys(testObj)
        print("delete_all_keys 실행 완료")
    except Exception as e:
        print("delete_all_keys 테스트 중 오류:", e)

# teapot의 재질 관련 테스트
def test_material():
    if teapot is None:
        print("teapot을 찾을 수 없습니다.")
        return
    print("teapot 재질 테스트 시작")
    try:
        print("teapot.material:", teapot.material)
        print("rt.getProperty(teapot, 'material'):", rt.getProperty(teapot, "material"))
    except Exception as e:
        print("teapot 재질 테스트 중 오류:", e)

# 테스트 실행 함수
def run_tests():
    print("===== Anim 모듈 테스트 시작 =====")
    test_rotate_local()
    test_move_local()
    test_collapse_anim_transform()
    test_match_anim_transform()
    test_create_average_transforms()
    test_key_functions()
    test_material()
    print("===== Anim 모듈 테스트 완료 =====")

# 이 파일이 직접 실행될 때만 테스트 실행
if __name__ == "__main__":
    run_tests()

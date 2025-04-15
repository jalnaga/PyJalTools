#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Align 클래스 테스트 - 3ds Max에서 객체 정렬 기능 테스트
"""

import sys
import os
import math
import importlib
from pymxs import runtime as rt

# JalLib 패키지를 임포트할 수 있도록 경로 설정
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..",))
if root_dir not in sys.path:
    sys.path.append(root_dir)

# 모듈 직접 리로드 - 매번 실행할 때마다 최신 코드 사용
import JalLib
import JalLib.max.align
importlib.reload(JalLib)
importlib.reload(JalLib.max.align)

# JalLib 모듈 리로드
from JalLib.tests import reload_jaltools_modules
reload_jaltools_modules()

from JalLib.max.align import Align

def create_test_objects():
    """테스트용 객체 생성 (Teapot, Sphere, Box, Pyramid)"""
    # 뷰포트 초기화 및 이전 객체 삭제
    rt.resetMaxFile(rt.name("noPrompt"))
    
    # 테스트 객체 생성
    teapot = rt.Teapot(radius=30, segments=8)
    teapot.pos = rt.Point3(0, 0, 0)
    teapot.rotation = rt.EulerAngles(0, 0, 0)
    teapot.wirecolor = rt.color(255, 0, 0)  # 빨간색
    teapot.name = "테스트_Teapot"
    
    sphere = rt.Sphere(radius=25, segments=16)
    sphere.pos = rt.Point3(100, 0, 0)
    sphere.rotation = rt.EulerAngles(0, 0, 45)
    sphere.wirecolor = rt.color(0, 255, 0)  # 녹색
    sphere.name = "테스트_Sphere"
    
    box = rt.Box(length=40, width=40, height=40)
    box.pos = rt.Point3(50, 80, 0)
    box.rotation = rt.EulerAngles(0, 45, 0)
    box.wirecolor = rt.color(0, 0, 255)  # 파란색
    box.name = "테스트_Box"
    
    pyramid = rt.Pyramid(width=50, depth=50, height=70)
    pyramid.pos = rt.Point3(0, 100, 0)
    pyramid.rotation = rt.EulerAngles(30, 0, 30)
    pyramid.wirecolor = rt.color(255, 255, 0)  # 노란색
    pyramid.name = "테스트_Pyramid"
    
    # 뷰포트 업데이트
    rt.redrawViews()
    
    return teapot, sphere, box, pyramid

def print_object_info(objects, message=""):
    """객체들의 위치 및 회전 정보 출력"""
    if message:
        print("\n" + "="*50)
        print(message)
        print("="*50)
    
    for obj in objects:
        pos = obj.pos
        rot = obj.rotation
        print(f"{obj.name} - 위치: ({pos.x:.1f}, {pos.y:.1f}, {pos.z:.1f}), " + 
              f"회전: ({math.degrees(rot.x):.1f}°, {math.degrees(rot.y):.1f}°, {math.degrees(rot.z):.1f}°)")

def run_test_align_to_last_sel_center(align):
    """마지막 선택된 객체의 중심점으로 정렬 테스트"""
    teapot, sphere, box, pyramid = create_test_objects()
    objects = [teapot, sphere, box, pyramid]
    
    # 객체 선택 - 마지막을 Pyramid로 설정
    rt.select(objects)
    
    # 테스트 전 정보 출력
    print_object_info(objects, "테스트 1: 마지막 선택된 객체(Pyramid)의 중심점으로 정렬 (align_to_last_sel_center)")
    
    # 정렬 메소드 실행
    align.align_to_last_sel_center()
    
    # 테스트 후 정보 출력
    print_object_info(objects, "테스트 1 결과: 마지막 선택된 객체(Pyramid)의 중심점으로 정렬 후")
    

def run_test_align_to_last_sel(align):
    """마지막 선택된 객체의 트랜스폼으로 정렬 테스트"""
    teapot, sphere, box, pyramid = create_test_objects()
    objects = [teapot, sphere, box, pyramid]
    
    # 객체 선택 - 마지막을 Pyramid로 설정
    rt.select(objects)
    
    # 테스트 전 정보 출력
    print_object_info(objects, "테스트 2: 마지막 선택된 객체(Pyramid)의 트랜스폼으로 정렬 (align_to_last_sel)")
    
    # 정렬 메소드 실행
    align.align_to_last_sel()
    
    # 테스트 후 정보 출력
    print_object_info(objects, "테스트 2 결과: 마지막 선택된 객체(Pyramid)의 트랜스폼으로 정렬 후")
    
    # 객체 다시 원래 위치로 복원
    create_test_objects()

def run_test_align_to_last_sel_pos(align):
    """마지막 선택된 객체의 위치로 정렬 (회전 유지) 테스트"""
    teapot, sphere, box, pyramid = create_test_objects()
    objects = [teapot, sphere, box, pyramid]
    
    # 객체 선택 - 마지막을 Pyramid로 설정
    rt.select(objects)
    
    # 테스트 전 정보 출력
    print_object_info(objects, "테스트 3: 마지막 선택된 객체(Pyramid)의 위치로 정렬 (회전 유지) (align_to_last_sel_pos)")
    
    # 정렬 메소드 실행
    align.align_to_last_sel_pos()
    
    # 테스트 후 정보 출력
    print_object_info(objects, "테스트 3 결과: 마지막 선택된 객체(Pyramid)의 위치로 정렬 (회전 유지) 후")
    
    # 객체 다시 원래 위치로 복원
    create_test_objects()

def run_test_align_to_last_sel_rot(align):
    """마지막 선택된 객체의 회전으로 정렬 (위치 유지) 테스트"""
    teapot, sphere, box, pyramid = create_test_objects()
    objects = [teapot, sphere, box, pyramid]
    
    # 객체 선택 - 마지막을 Pyramid로 설정
    rt.select(objects)
    
    # 테스트 전 정보 출력
    print_object_info(objects, "테스트 4: 마지막 선택된 객체(Pyramid)의 회전으로 정렬 (위치 유지) (align_to_last_sel_rot)")
    
    # 정렬 메소드 실행
    align.align_to_last_sel_rot()
    
    # 테스트 후 정보 출력
    print_object_info(objects, "테스트 4 결과: 마지막 선택된 객체(Pyramid)의 회전으로 정렬 (위치 유지) 후")

def main():
    """메인 테스트 실행 함수"""
    try:
        print("\n" + "*"*60)
        print("JalTools Align 클래스 테스트 시작")
        print("*"*60)
        
        # Align 클래스 인스턴스 생성
        align = Align()
        
        # 각 정렬 메소드 테스트 실행
        run_test_align_to_last_sel_center(align)
        run_test_align_to_last_sel(align)
        run_test_align_to_last_sel_pos(align)
        run_test_align_to_last_sel_rot(align)
        
        print("\n" + "*"*60)
        print("JalTools Align 클래스 테스트 완료")
        print("*"*60)
        
    except Exception as e:
        import traceback
        print(f"오류 발생: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()

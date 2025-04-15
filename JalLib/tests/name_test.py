#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
3ds Max Name 클래스 테스트 스크립트
이 스크립트는 3ds Max에서 직접 실행되며, Name 클래스의 기능을 테스트합니다.
"""

from pymxs import runtime as rt
from JalLib import configPaths
from JalLib.max.name import Name

def create_test_objects():
    """테스트용 객체 생성 함수"""
    print("\n=== 테스트 객체 생성 ===")
    
    # 기존 객체 삭제
    rt.delete(rt.objects)
    
    # 테스트용 객체 생성
    box1 = rt.Box(width=10, length=10, height=10, name="b_P_L_Cube_001")
    box2 = rt.Box(width=10, length=10, height=10, name="b_P_R_Cube_001")
    box3 = rt.Box(width=10, length=10, height=10, name="b_Dum_L_F_Arm_001")
    box4 = rt.Box(width=10, length=10, height=10, name="b_Dum_R_B_Arm_001")
    
    print(f"생성된 객체: {box1.name}, {box2.name}, {box3.name}, {box4.name}")
    return [box1, box2, box3, box4]

def test_gen_unique_name(name_service):
    """고유 이름 생성 기능 테스트"""
    print("\n=== 고유 이름 생성 테스트 ===")
    
    base_name = "b_P_L_Cube_001"
    unique_name = name_service.gen_unique_name(base_name)
    print(f"기본 이름: {base_name}")
    print(f"고유 이름: {unique_name}")
    
    # 실제로 새 객체 생성
    new_box = rt.Box(width=10, length=10, height=10, name=unique_name)
    print(f"새 객체 생성됨: {new_box.name}")
    
    # 다시 고유 이름 생성
    another_unique_name = name_service.gen_unique_name(base_name)
    print(f"다음 고유 이름: {another_unique_name}")

def test_compare_and_sort(name_service, objects):
    """이름 비교 및 정렬 기능 테스트"""
    print("\n=== 이름 비교 및 정렬 테스트 ===")
    
    print("정렬 전 객체:")
    for obj in objects:
        print(f"  {obj.name}")
    
    # 첫 번째와 두 번째 객체 비교
    compare_result = name_service.compare_name(objects[0], objects[1])
    print(f"\n비교 결과 ({objects[0].name} vs {objects[1].name}): {compare_result}")
    
    # 이름으로 정렬
    sorted_objects = name_service.sort_by_name(objects)
    
    print("\n정렬 후 객체:")
    for obj in sorted_objects:
        print(f"  {obj.name}")

def test_mirroring_name(name_service):
    """미러링 이름 생성 테스트"""
    print("\n=== 미러링 이름 테스트 ===")
    
    test_names = [
        "b_P_L_Arm_001",
        "b_Dum_R_Leg_001",
        "b_P_L_F_Hand_001",
        "b_P_R_B_Foot_001"
    ]
    
    for name in test_names:
        mirrored_name = name_service.gen_mirroring_name(name)
        print(f"원본 이름: {name}")
        print(f"미러링 이름: {mirrored_name}")
        print()

def test_type_strings(name_service):
    """타입 문자열 가져오기 테스트"""
    print("\n=== 타입 문자열 테스트 ===")
    
    parent_str = name_service.get_parent_str()
    dummy_str = name_service.get_dummy_str()
    exposeTm_str = name_service.get_exposeTm_str()
    ik_str = name_service.get_ik_str()
    target_str = name_service.get_target_str()
    
    print(f"부모 문자열: {parent_str}")
    print(f"더미 문자열: {dummy_str}")
    print(f"ExposeTm 문자열: {exposeTm_str}")
    print(f"IK 문자열: {ik_str}")
    print(f"타겟 문자열: {target_str}")

def run_tests():
    """모든 테스트 실행"""
    print("\n========== Name 클래스 테스트 시작 ==========")
    
    # Name 서비스 인스턴스 생성
    name_service = Name(configPaths.get_naming_config_path())
    
    # 테스트 객체 생성
    test_objects = create_test_objects()
    
    # 각 기능 테스트
    test_gen_unique_name(name_service)
    test_compare_and_sort(name_service, test_objects)
    test_mirroring_name(name_service)
    test_type_strings(name_service)
    
    print("\n========== Name 클래스 테스트 완료 ==========")

# 스크립트 실행
if __name__ == "__main__":
    try:
        run_tests()
    except Exception as e:
        import traceback
        print(f"오류 발생: {e}")
        traceback.print_exc()
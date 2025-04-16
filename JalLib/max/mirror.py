#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
미러 모듈 - 3ds Max용 객체 미러링 관련 기능 제공
원본 MAXScript의 mirror.ms를 Python으로 변환하였으며, pymxs 모듈 기반으로 구현됨
"""

from pymxs import runtime as rt


class Mirror:
    """
    객체 미러링 관련 기능을 제공하는 클래스.
    MAXScript의 _Mirror 구조체 개념을 Python으로 재구현한 클래스이며,
    3ds Max의 기능들을 pymxs API를 통해 제어합니다.
    """
    
    def __init__(self, name_service, bone_service):
        """
        클래스 초기화
        
        Args:
            name_service: Name 서비스 인스턴스
            bone_service: Bone 서비스 인스턴스
        """
        self.name = name_service
        self.bone = bone_service
    
    def mirror_matrix(self, m_axis="x", m_flip="x", tm=None, pivot_tm=None):
        """
        미러링 행렬 생성
        
        Args:
            m_axis: 미러링 축 (기본값: "x")
            m_flip: 뒤집는 축 (기본값: "x")
            tm: 변환 행렬 (기본값: 단위 행렬)
            pivot_tm: 피벗 변환 행렬 (기본값: 단위 행렬)
            
        Returns:
            미러링된 변환 행렬
        """
        def fetch_reflection(a):
            """
            반사 벡터 값 반환
            
            Args:
                a: 축 식별자 ("x", "y", "z")
                
            Returns:
                해당 축에 대한 반사 벡터
            """
            if a == "x":
                return [-1, 1, 1]  # YZ 평면에 대한 반사
            elif a == "y":
                return [1, -1, 1]  # ZX 평면에 대한 반사
            elif a == "z":
                return [1, 1, -1]  # XY 평면에 대한 반사
            else:
                return [1, 1, 1]  # 반사 없음
        
        # 기본값 설정
        if tm is None:
            tm = rt.matrix3(1)
        if pivot_tm is None:
            pivot_tm = rt.matrix3(1)
        
        # 반사 행렬 생성
        a_reflection = rt.scalematrix(rt.Point3(*fetch_reflection(m_axis)))
        f_reflection = rt.scalematrix(rt.Point3(*fetch_reflection(m_flip)))
        
        # 미러링된 변환 행렬 계산: fReflection * tm * aReflection * pivotTm
        return f_reflection * tm * a_reflection * pivot_tm
    
    def apply_mirror(self, in_obj, axis=1, flip=2, pivot_obj=None, clone_status=2, negative=False):
        """
        객체에 미러링 적용
        
        Args:
            in_obj: 미러링할 객체
            axis: 미러링 축 인덱스 (1=x, 2=y, 3=z, 기본값: 1)
            flip: 뒤집기 축 인덱스 (1=x, 2=y, 3=z, 4=none, 기본값: 2)
            pivot_obj: 피벗 객체 (기본값: None)
            clone_status: 복제 상태 (1=원본 변경, 2=복제본 생성, 3=스냅샷, 기본값: 2)
            negative: 음수 좌표계 사용 여부 (기본값: False)
            
        Returns:
            미러링된 객체 (복제본 또는 원본)
        """
        axis_array = ["x", "y", "z", "none"]
        copy_obj = rt.copy(in_obj)
        obj_tm = in_obj.transform
        pivot_tm = rt.matrix3(1)
        mirror_axis_index = axis
        flip_axis_index = flip
        copy_obj_name = self.name.gen_mirroring_name(in_obj.name, axis=axis)
        
        # 피벗 객체가 지정된 경우 피벗 변환 행렬 사용
        if pivot_obj is not None:
            pivot_tm = pivot_obj.transform
        
        # negative가 True인 경우 뒤집기 없음으로 설정
        if negative:
            flip_axis_index = 4
        
        # 복제본 초기 설정
        copy_obj.name = copy_obj_name
        copy_obj.parent = None
        copy_obj.wirecolor = in_obj.wirecolor
        
        # 복제 상태에 따른 처리
        if clone_status == 1:  # 원본 변경
            rt.delete(copy_obj)
            copy_obj = None
            in_obj.transform = self.mirror_matrix(
                m_axis=axis_array[mirror_axis_index-1],
                m_flip=axis_array[flip_axis_index-1],
                tm=obj_tm,
                pivot_tm=pivot_tm
            )
            copy_obj = in_obj
        elif clone_status == 2:  # 복제본 생성
            copy_obj.transform = self.mirror_matrix(
                m_axis=axis_array[mirror_axis_index-1],
                m_flip=axis_array[flip_axis_index-1],
                tm=obj_tm,
                pivot_tm=pivot_tm
            )
        elif clone_status == 3:  # 스냅샷 생성
            rt.delete(copy_obj)
            copy_obj = None
            copy_obj = rt.snapShot(in_obj)
            copy_obj.transform = self.mirror_matrix(
                m_axis=axis_array[mirror_axis_index-1],
                m_flip=axis_array[flip_axis_index-1],
                tm=obj_tm,
                pivot_tm=pivot_tm
            )
        
        return copy_obj
    
    def mirror_object(self, in_obj_array, m_axis=1, pivot_obj=None, clone_status=2):
        """
        객체 배열을 음수 좌표계를 사용하여 미러링
        
        Args:
            in_obj_array: 미러링할 객체 배열
            m_axis: 미러링 축 (기본값: 1)
            pivot_obj: 피벗 객체 (기본값: None)
            clone_status: 복제 상태 (기본값: 2)
            
        Returns:
            미러링된 객체 배열
        """
        return_array = []
        
        for item in in_obj_array:
            mirrored_obj = self.apply_mirror(
                item, 
                axis=m_axis, 
                pivot_obj=pivot_obj, 
                clone_status=clone_status, 
                negative=True
            )
            return_array.append(mirrored_obj)
        
        return return_array
    
    def mirror_without_negative(self, in_mirror_obj_array, m_axis=1, pivot_obj=None, clone_status=2):
        """
        객체 배열을 양수 좌표계를 사용하여 미러링
        
        Args:
            in_mirror_obj_array: 미러링할 객체 배열
            m_axis: 미러링 축 인덱스 (1-6, 기본값: 1)
            pivot_obj: 피벗 객체 (기본값: None)
            clone_status: 복제 상태 (기본값: 2)
            
        Returns:
            미러링된 객체 배열
        """
        # 미러링 축과 뒤집기 축 매핑
        # 1=XY, 2=XZ, 3=YX, 4=YZ, 5=ZX, 6=ZY
        axis_index = 1
        flip_index = 1
        
        # 미러링 축 인덱스에 따른 매핑
        if m_axis == 1:
            axis_index = 1  # x
            flip_index = 2  # y
        elif m_axis == 2:
            axis_index = 1  # x
            flip_index = 3  # z
        elif m_axis == 3:
            axis_index = 2  # y
            flip_index = 1  # x
        elif m_axis == 4:
            axis_index = 2  # y
            flip_index = 3  # z
        elif m_axis == 5:
            axis_index = 3  # z
            flip_index = 1  # x
        elif m_axis == 6:
            axis_index = 3  # z
            flip_index = 2  # y
        else:
            axis_index = 1  # x
            flip_index = 1  # x
        
        # 미러링 적용
        return_array = []
        for item in in_mirror_obj_array:
            mirrored_obj = self.apply_mirror(
                item, 
                axis=axis_index, 
                flip=flip_index, 
                pivot_obj=pivot_obj, 
                clone_status=clone_status, 
                negative=False
            )
            return_array.append(mirrored_obj)
        
        return return_array
    
    def mirror_bone(self, in_bone_array, m_axis=1, flip_z=False, offset=0.0):
        """
        뼈대 객체를 미러링
        
        Args:
            in_bone_array: 미러링할 뼈대 배열
            m_axis: 미러링 축 (1=x, 2=y, 3=z, 기본값: 1)
            flip_z: Z축 뒤집기 여부 (기본값: False)
            offset: 미러링 오프셋 (기본값: 0.0)
            
        Returns:
            미러링된 뼈대 배열
        """
        # 계층 구조에 따라 뼈대 정렬
        bones = self.bone.sort_bones_as_hierarchy(in_bone_array)
        
        # 미러링 축 팩터 설정
        axis_factor = [1, 1, 1]
        if m_axis == 1:
            axis_factor = [-1, 1, 1]  # x축 미러링
        elif m_axis == 2:
            axis_factor = [1, -1, 1]  # y축 미러링
        elif m_axis == 3:
            axis_factor = [1, 1, -1]  # z축 미러링
        
        # 새 뼈대와 부모 정보 저장 배열 준비
        parents = []
        created = []
        
        # 시작점 위치 (미러링 중심) 설정
        root = bones[0].transform.translation
        
        # 정렬된 뼈대 순서대로 처리
        for i in range(len(bones)):
            original = bones[i]
            if rt.classOf(original) != rt.BoneGeometry:  # 실제 뼈대가 아닌 경우
                parents.append(None)  # 부모 없음 표시
                continue
            
            # 원본 뼈대의 시작점, 끝점, Z축 방향 가져오기
            bone_start = original.pos
            bone_end = self.bone.get_bone_end_position(original)
            bone_z = original.dir
            
            # 미러링 적용
            for k in range(3):  # x, y, z 좌표
                if axis_factor[k] < 0:
                    bone_start[k] = 2.0 * root[k] - bone_start[k] + offset
                    bone_end[k] = 2.0 * root[k] - bone_end[k] + offset
                    bone_z[k] = -bone_z[k]
            
            # Z축 뒤집기 옵션 적용
            if flip_z:
                bone_z = -bone_z
            
            # 새 뼈대 생성
            reflection = rt.bonesys.createbone(bone_start, bone_end, bone_z)
            
            # 원본 뼈대의 속성을 복사
            reflection.backfin = original.backfin
            reflection.backfinendtaper = original.backfinendtaper
            reflection.backfinsize = original.backfinsize
            reflection.backfinstarttaper = original.backfinstarttaper
            reflection.frontfin = original.frontfin
            reflection.frontfinendtaper = original.frontfinendtaper
            reflection.frontfinsize = original.frontfinsize
            reflection.frontfinstarttaper = original.frontfinstarttaper
            reflection.height = original.height
            
            # 이름 생성 (좌우/앞뒤 방향이 있는 경우 미러링된 이름 생성)
            if self.name.has_side(original.name) or self.name.has_front_back(original.name):
                reflection.name = self.name.gen_mirroring_name(original.name, axis=m_axis)
            else:
                reflection.name = self.name.add_sufix_to_realName(original.name, "Mirrored")
                
            reflection.sidefins = original.sidefins
            reflection.sidefinsendtaper = original.sidefinsendtaper
            reflection.sidefinssize = original.sidefinssize
            reflection.sidefinsstarttaper = original.sidefinsstarttaper
            reflection.taper = original.taper
            reflection.width = original.width
            reflection.wirecolor = original.wirecolor
            
            created.append(reflection)
            parents.append(reflection)
        
        # 계층 구조 연결 (자식부터 상위로)
        for i in range(len(created)-1, 0, -1):
            p_index = bones.index(bones[i].parent) if bones[i].parent in bones else 0
            if p_index != 0:
                created[i].parent = parents[p_index]
        
        # 루트 뼈대의 부모 설정
        created[0].parent = bones[0].parent
        
        # 부모가 없는 뼈대는 위치 조정
        for i in range(len(created)):
            if created[i].parent is None:
                created[i].position = rt.Point3(
                    bones[i].position.x * axis_factor[0],
                    bones[i].position.y * axis_factor[1],
                    bones[i].position.z * axis_factor[2]
                )
        
        return created
    
    def mirror_geo(self, in_mirror_obj_array, m_axis=1, pivot_obj=None, clone_status=2):
        """
        지오메트리 객체 미러링 (폴리곤 노멀 방향 조정 포함)
        
        Args:
            in_mirror_obj_array: 미러링할 객체 배열
            m_axis: 미러링 축 (기본값: 1)
            pivot_obj: 피벗 객체 (기본값: None)
            clone_status: 복제 상태 (기본값: 2)
            
        Returns:
            미러링된 객체 배열
        """
        # 객체 미러링
        mirrored_array = self.mirror_object(
            in_mirror_obj_array,
            m_axis=m_axis,
            pivot_obj=pivot_obj,
            clone_status=clone_status
        )
        
        # 리셋 대상, 비리셋 대상 분류
        reset_xform_array = []
        non_reset_xform_array = []
        return_array = []
        
        # 객체 타입에 따라 분류
        for item in mirrored_array:
            case_index = 0
            if rt.classOf(item) == rt.Editable_Poly:
                case_index += 1
            if rt.classOf(item) == rt.Editable_mesh:
                case_index += 1
            if item.modifiers.count > 0:
                case_index += 1
                
            if case_index == 1:  # 폴리곤, 메시 또는 모디파이어가 있는 경우
                reset_xform_array.append(item)
            else:
                non_reset_xform_array.append(item)
        
        # 리셋 대상 객체에 XForm 리셋 및 노멀 방향 뒤집기 적용
        for item in reset_xform_array:
            rt.ResetXForm(item)
            temp_normal_mod = rt.normalModifier()
            temp_normal_mod.flip = True
            rt.addModifier(item, temp_normal_mod)
            rt.collapseStack(item)
        
        # 처리된 객체들 합치기
        return_array.extend(reset_xform_array)
        return_array.extend(non_reset_xform_array)
        
        return return_array
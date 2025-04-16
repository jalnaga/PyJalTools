#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Biped 모듈 - 3ds Max의 Biped 객체 관련 기능 제공
원본 MAXScript의 bip.ms를 Python으로 변환하였으며, pymxs 모듈 기반으로 구현됨
"""

from pymxs import runtime as rt


class Bip:
    """
    Biped 객체 관련 기능을 제공하는 클래스.
    MAXScript의 _Bip 구조체 개념을 Python으로 재구현한 클래스이며,
    3ds Max의 기능들을 pymxs API를 통해 제어합니다.
    """
    
    def __init__(self, anim_service, name_service, bone_service):
        """
        클래스 초기화
        
        Args:
            anim_service: Anim 서비스 인스턴스
            name_service: Name 서비스 인스턴스
            bone_service: Bone 서비스 인스턴스
        """
        self.anim = anim_service
        self.name = name_service
        self.bone = bone_service
    
    def get_bips(self):
        """
        씬 내의 모든 Biped_Object를 찾음
        
        Returns:
            Biped_Object 리스트
        """
        return [obj for obj in rt.objects if rt.isKindOf(obj, rt.Biped_Object)]
    
    def get_coms_name(self):
        """
        씬 내 모든 Biped COM(Center of Mass)의 이름 리스트 반환
        
        Returns:
            Biped COM 이름 리스트
        """
        bips = self.get_bips()
        bip_coms_name = []
        
        for obj in bips:
            # appendIfUnique 구현
            root_name = obj.controller.rootName
            if root_name not in bip_coms_name:
                bip_coms_name.append(root_name)
                
        return bip_coms_name
    
    def get_coms(self):
        """
        씬 내 모든 Biped COM(Center of Mass) 객체 리스트 반환
        
        Returns:
            Biped COM 객체 리스트
        """
        bips = self.get_bips()
        bip_coms = []
        
        for obj in bips:
            # appendIfUnique 구현
            root_node = obj.controller.rootNode
            if root_node not in bip_coms:
                bip_coms.append(root_node)
                
        return bip_coms
    
    def is_biped_object(self, in_obj):
        """
        객체가 Biped 관련 객체인지 확인
        
        Args:
            in_obj: 확인할 객체
            
        Returns:
            Biped 관련 객체이면 True, 아니면 False
        """
        return (rt.classOf(in_obj.controller) == rt.BipSlave_control or 
                rt.classOf(in_obj.controller) == rt.Footsteps or 
                rt.classOf(in_obj.controller) == rt.Vertical_Horizontal_Turn)
    
    def get_com(self, in_bip):
        """
        Biped 객체의 COM(Center of Mass) 반환
        
        Args:
            in_bip: COM을 찾을 Biped 객체
            
        Returns:
            Biped의 COM 객체 또는 None
        """
        if self.is_biped_object(in_bip):
            return in_bip.controller.rootNode
        return None
    
    def get_all(self, in_bip):
        """
        Biped와 관련된 모든 객체 반환
        
        Args:
            in_bip: 기준 Biped 객체
            
        Returns:
            Biped 관련 모든 객체 리스트
        """
        return_val = []
        
        if self.is_biped_object(in_bip):
            root = self.get_com(in_bip)
            all_nodes = [root]
            return_val = [root]
            
            for obj in all_nodes:
                for child in obj.children:
                    # appendIfUnique 구현
                    if child not in all_nodes:
                        all_nodes.append(child)
                    if self.is_biped_object(child) and child not in return_val:
                        return_val.append(child)
                
                if obj.parent is not None:
                    if obj.parent not in all_nodes:
                        all_nodes.append(obj.parent)
                    if self.is_biped_object(obj.parent) and obj.parent not in return_val:
                        return_val.append(obj.parent)
        
        return return_val
    
    def get_nodes(self, in_bip):
        """
        Biped의 실제 노드만 반환 (더미나 Footstep은 제외)
        
        Args:
            in_bip: 기준 Biped 객체
            
        Returns:
            Biped의 노드 객체 리스트
        """
        return_val = []
        
        if self.is_biped_object(in_bip):
            root = self.get_com(in_bip)
            all_nodes = [root]
            return_val = [root]
            
            for obj in all_nodes:
                for child in obj.children:
                    if rt.classOf(child) != rt.Dummy and rt.classOf(child.controller) != rt.Footsteps:
                        if child not in all_nodes:
                            all_nodes.append(child)
                        if self.is_biped_object(child) and child not in return_val:
                            return_val.append(child)
                
                if obj.parent is not None:
                    if rt.classOf(obj.parent) != rt.Dummy and rt.classOf(obj.parent.controller) != rt.Footsteps:
                        if obj.parent not in all_nodes:
                            all_nodes.append(obj.parent)
                        if self.is_biped_object(obj.parent) and obj.parent not in return_val:
                            return_val.append(obj.parent)
        
        return return_val
    
    def get_dummy_and_footstep(self, in_bip):
        """
        Biped의 더미와 Footstep 객체만 반환
        
        Args:
            in_bip: 기준 Biped 객체
            
        Returns:
            더미와 Footstep 객체 리스트
        """
        return_val = []
        
        if self.is_biped_object(in_bip):
            bip_array = self.get_all(in_bip)
            return_val = [item for item in bip_array if rt.classOf(item) == rt.Dummy or rt.classOf(item.controller) == rt.Footsteps]
        
        return return_val
    
    def get_nodes_by_skeleton_order(self, in_bip):
        """
        스켈레톤 순서대로 Biped 노드 반환
        
        Args:
            in_bip: 기준 Biped 객체
            
        Returns:
            순서대로 정렬된 Biped 노드 리스트
        """
        if rt.classOf(in_bip) != rt.Biped_Object:
            return []
            
        com = in_bip.controller.rootNode
        
        # 각 바이패드 부위 노드 가져오기
        head = rt.biped.getNode(com, rt.Name("head"))
        hips = rt.biped.getNode(com, rt.Name("pelvis"))
        l_arm = rt.biped.getNode(com, rt.Name("larm"), link=2)
        l_clavicle = rt.biped.getNode(com, rt.Name("larm"), link=1)
        l_foot = rt.biped.getNode(com, rt.Name("lleg"), link=3)
        l_toe = rt.biped.getNode(com, rt.Name("ltoes"), link=1)
        l_forearm = rt.biped.getNode(com, rt.Name("larm"), link=3)
        l_hand = rt.biped.getNode(com, rt.Name("larm"), link=4)
        l_hand_index = rt.biped.getNode(com, rt.Name("lfingers"), link=5)
        l_hand_index1 = rt.biped.getNode(com, rt.Name("lfingers"), link=6)
        l_hand_index2 = rt.biped.getNode(com, rt.Name("lfingers"), link=7)
        l_hand_index3 = rt.biped.getNode(com, rt.Name("lfingers"), link=8)
        l_hand_middle = rt.biped.getNode(com, rt.Name("lfingers"), link=9)
        l_hand_middle1 = rt.biped.getNode(com, rt.Name("lfingers"), link=10)
        l_hand_middle2 = rt.biped.getNode(com, rt.Name("lfingers"), link=11)
        l_hand_middle3 = rt.biped.getNode(com, rt.Name("lfingers"), link=12)
        l_hand_pinky = rt.biped.getNode(com, rt.Name("lfingers"), link=17)
        l_hand_pinky1 = rt.biped.getNode(com, rt.Name("lfingers"), link=18)
        l_hand_pinky2 = rt.biped.getNode(com, rt.Name("lfingers"), link=19)
        l_hand_pinky3 = rt.biped.getNode(com, rt.Name("lfingers"), link=20)
        l_hand_ring = rt.biped.getNode(com, rt.Name("lfingers"), link=13)
        l_hand_ring1 = rt.biped.getNode(com, rt.Name("lfingers"), link=14)
        l_hand_ring2 = rt.biped.getNode(com, rt.Name("lfingers"), link=15)
        l_hand_ring3 = rt.biped.getNode(com, rt.Name("lfingers"), link=16)
        l_hand_thumb1 = rt.biped.getNode(com, rt.Name("lfingers"), link=1)
        l_hand_thumb2 = rt.biped.getNode(com, rt.Name("lfingers"), link=2)
        l_hand_thumb3 = rt.biped.getNode(com, rt.Name("lfingers"), link=3)
        l_leg = rt.biped.getNode(com, rt.Name("lleg"), link=2)
        l_upleg = rt.biped.getNode(com, rt.Name("lleg"), link=1)
        neck = rt.biped.getNode(com, rt.Name("neck"), link=1)
        neck1 = rt.biped.getNode(com, rt.Name("neck"), link=2)
        r_arm = rt.biped.getNode(com, rt.Name("rarm"), link=2)
        r_clavicle = rt.biped.getNode(com, rt.Name("rarm"), link=1)
        r_foot = rt.biped.getNode(com, rt.Name("rleg"), link=3)
        r_toe = rt.biped.getNode(com, rt.Name("rtoes"), link=1)
        r_forearm = rt.biped.getNode(com, rt.Name("rarm"), link=3)
        r_hand = rt.biped.getNode(com, rt.Name("rarm"), link=4)
        r_hand_index = rt.biped.getNode(com, rt.Name("rfingers"), link=5)
        r_hand_index1 = rt.biped.getNode(com, rt.Name("rfingers"), link=6)
        r_hand_index2 = rt.biped.getNode(com, rt.Name("rfingers"), link=7)
        r_hand_index3 = rt.biped.getNode(com, rt.Name("rfingers"), link=8)
        r_hand_middle = rt.biped.getNode(com, rt.Name("rfingers"), link=9)
        r_hand_middle1 = rt.biped.getNode(com, rt.Name("rfingers"), link=10)
        r_hand_middle2 = rt.biped.getNode(com, rt.Name("rfingers"), link=11)
        r_hand_middle3 = rt.biped.getNode(com, rt.Name("rfingers"), link=12)
        r_hand_pinky = rt.biped.getNode(com, rt.Name("rfingers"), link=17)
        r_hand_pinky1 = rt.biped.getNode(com, rt.Name("rfingers"), link=18)
        r_hand_pinky2 = rt.biped.getNode(com, rt.Name("rfingers"), link=19)
        r_hand_pinky3 = rt.biped.getNode(com, rt.Name("rfingers"), link=20)
        r_hand_ring = rt.biped.getNode(com, rt.Name("rfingers"), link=13)
        r_hand_ring1 = rt.biped.getNode(com, rt.Name("rfingers"), link=14)
        r_hand_ring2 = rt.biped.getNode(com, rt.Name("rfingers"), link=15)
        r_hand_ring3 = rt.biped.getNode(com, rt.Name("rfingers"), link=16)
        r_hand_thumb1 = rt.biped.getNode(com, rt.Name("rfingers"), link=1)
        r_hand_thumb2 = rt.biped.getNode(com, rt.Name("rfingers"), link=2)
        r_hand_thumb3 = rt.biped.getNode(com, rt.Name("rfingers"), link=3)
        r_leg = rt.biped.getNode(com, rt.Name("rleg"), link=2)
        r_upleg = rt.biped.getNode(com, rt.Name("rleg"), link=1)
        spine = rt.biped.getNode(com, rt.Name("spine"), link=1)
        spine1 = rt.biped.getNode(com, rt.Name("spine"), link=2)
        spine2 = rt.biped.getNode(com, rt.Name("spine"), link=3)
        
        # 순서대로 배열 생성
        bip_node_array = [head, hips, l_arm, l_clavicle, l_foot, l_toe, l_forearm, l_hand,
                         l_hand_index, l_hand_index1, l_hand_index2, l_hand_index3,
                         l_hand_middle, l_hand_middle1, l_hand_middle2, l_hand_middle3,
                         l_hand_pinky, l_hand_pinky1, l_hand_pinky2, l_hand_pinky3,
                         l_hand_ring, l_hand_ring1, l_hand_ring2, l_hand_ring3,
                         l_hand_thumb1, l_hand_thumb2, l_hand_thumb3,
                         l_leg, l_upleg, neck, neck1,
                         r_arm, r_clavicle, r_foot, r_toe, r_forearm, r_hand,
                         r_hand_index, r_hand_index1, r_hand_index2, r_hand_index3,
                         r_hand_middle, r_hand_middle1, r_hand_middle2, r_hand_middle3,
                         r_hand_pinky, r_hand_pinky1, r_hand_pinky2, r_hand_pinky3,
                         r_hand_ring, r_hand_ring1, r_hand_ring2, r_hand_ring3,
                         r_hand_thumb1, r_hand_thumb2, r_hand_thumb3,
                         r_leg, r_upleg, spine, spine1, spine2]
        
        return bip_node_array
    
    def load_bip_file(self, in_bip_root, in_file):
        """
        Biped BIP 파일 로드
        
        Args:
            in_bip_root: 로드 대상 Biped 루트 노드
            in_file: 로드할 BIP 파일 경로
        """
        bip_node_array = self.get_all(in_bip_root)
        
        # Figure 모드 전환
        in_bip_root.controller.figureMode = False
        rt.biped.loadBipFile(in_bip_root.controller, in_file)
        in_bip_root.controller.figureMode = True
        in_bip_root.controller.figureMode = False
        
        # 키 범위 설정
        key_range = []
        for i in range(1, len(bip_node_array)):
            if bip_node_array[i].controller.keys.count != 0 and bip_node_array[i].controller.keys.count != -1:
                key_time = bip_node_array[i].controller.keys[bip_node_array[i].controller.keys.count - 1].time
                if key_time not in key_range:
                    key_range.append(key_time)
        
        if key_range and max(key_range) != 0:
            rt.animationRange = rt.interval(0, max(key_range))
            rt.sliderTime = 0
    
    def load_fig_file(self, in_bip_root, in_file):
        """
        Biped FIG 파일 로드
        
        Args:
            in_bip_root: 로드 대상 Biped 루트 노드
            in_file: 로드할 FIG 파일 경로
        """
        in_bip_root.controller.figureMode = False
        in_bip_root.controller.figureMode = True
        rt.biped.LoadFigFile(in_bip_root.controller, in_file)
        in_bip_root.controller.figureMode = False
    
    def save_fig_file(self, in_bip_root, file_name):
        """
        Biped FIG 파일 저장
        
        Args:
            in_bip_root: 저장 대상 Biped 루트 노드
            file_name: 저장할 FIG 파일 경로
        """
        in_bip_root.controller.figureMode = False
        in_bip_root.controller.figureMode = True
        rt.biped.saveFigFile(in_bip_root.controller, file_name)
    
    def turn_on_figureMode(self, in_bip):
        """
        Biped Figure 모드 켜기
        
        Args:
            in_bip: 대상 Biped 객체
        """
        in_bip.controller.figureMode = True
    
    def turn_off_figureMode(self, in_bip):
        """
        Biped Figure 모드 끄기
        
        Args:
            in_bip: 대상 Biped 객체
        """
        in_bip.controller.figureMode = False
    
    def delete_copyCollection(self, in_bip, in_name):
        """
        Biped 복사 컬렉션 삭제
        
        Args:
            in_bip: 대상 Biped 객체
            in_name: 삭제할 컬렉션 이름
        """
        if self.is_biped_object(in_bip):
            col_num = rt.biped.numCopyCollections(in_bip.controller)
            if col_num > 0:
                for i in range(1, col_num + 1):
                    if rt.biped.getCopyCollection(in_bip.controller, i).name == in_name:
                        rt.biped.deleteCopyCollection(in_bip.controller, i)
                        break
    
    def link_base_skeleton(self):
        """
        기본 스켈레톤 링크 (Biped와 일반 뼈대 연결)
        """
        rt.setWaitCursor()
        skin_bone_base_name = "b"
        
        bip_skel = self.get_bips()
        base_skel = [None] * len(bip_skel)
        
        # 일치하는 기본 스켈레톤 찾기
        for i in range(len(bip_skel)):
            base_skeleton_name = self.name.replace_base(bip_skel[i].name, skin_bone_base_name)
            base_skeleton_name = self.name.replace_filteringChar(base_skeleton_name, "_")
            base_skel_obj = rt.getNodeByName(base_skeleton_name)
            if rt.isValidObj(base_skel_obj):
                base_skel[i] = base_skel_obj
        
        # 변환 저장 및 설정
        self.anim.save_xform(bip_skel)
        self.anim.set_xform(bip_skel)
        
        self.anim.save_xform(base_skel)
        self.anim.set_xform(base_skel)
        
        # 링크 설정
        for i in range(len(base_skel)):
            if base_skel[i] is not None:
                base_skel[i].scale.controller = rt.scaleXYZ()
                base_skel[i].controller = rt.link_constraint()
                
                self.anim.set_xform([base_skel[i]], space="World")
                base_skel[i].transform.controller.AddTarget(bip_skel[i], 0)
        
        # 뼈대 활성화
        for i in range(len(base_skel)):
            if base_skel[i] is not None:
                base_skel[i].boneEnable = True
                
        rt.setArrowCursor()
    
    def unlink_base_skeleton(self):
        """
        기본 스켈레톤 링크 해제
        """
        rt.setWaitCursor()
        skin_bone_base_name = "b"
        
        bip_skel = self.get_bips()
        base_skel = [None] * len(bip_skel)
        
        # 일치하는 기본 스켈레톤 찾기
        for i in range(len(bip_skel)):
            base_skeleton_name = self.name.replace_base(bip_skel[i].name, skin_bone_base_name)
            base_skeleton_name = self.name.replace_filteringChar(base_skeleton_name, "_")
            base_skel_obj = rt.getNodeByName(base_skeleton_name)
            if rt.isValidObj(base_skel_obj):
                base_skel[i] = base_skel_obj
        
        # 변환 저장 및 설정
        self.anim.save_xform(bip_skel)
        self.anim.set_xform(bip_skel)
        
        self.anim.save_xform(base_skel)
        self.anim.set_xform(base_skel)
        
        # 링크 해제
        for i in range(len(base_skel)):
            if base_skel[i] is not None:
                base_skel[i].controller = rt.prs()
                self.anim.set_xform([base_skel[i]], space="World")
        
        # 뼈대 활성화
        for i in range(len(base_skel)):
            if base_skel[i] is not None:
                base_skel[i].boneEnable = True
                
        rt.setArrowCursor()
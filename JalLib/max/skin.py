#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
스킨 모듈 - 3ds Max용 고급 스킨 관련 기능 제공
원본 MAXScript의 skin2.ms를 Python으로 변환하였으며, pymxs 모듈 기반으로 구현됨
"""

import os
from pymxs import runtime as rt


class Skin:
    """
    고급 스킨 관련 기능을 제공하는 클래스.
    MAXScript의 ODC_Char_Skin 구조체 개념을 Python으로 재구현한 클래스이며,
    3ds Max의 기능들을 pymxs API를 통해 제어합니다.
    """
    
    def __init__(self):
        """
        클래스 초기화
        """
        self.skin_match_list = []
    
    def has_skin(self, obj=None):
        """
        객체에 스킨 모디파이어가 있는지 확인
        
        Args:
            obj: 확인할 객체 (기본값: 현재 선택된 객체)
            
        Returns:
            True: 스킨 모디파이어가 있는 경우
            False: 없는 경우
        """
        if obj is None:
            if len(rt.selection) > 0:
                obj = rt.selection[0]
            else:
                return False
        
        # 객체의 모든 모디파이어를 검사하여 Skin 모디파이어가 있는지 확인
        for mod in obj.modifiers:
            if rt.classOf(mod) == rt.Skin:
                return True
        return False
    
    def is_valid_bone(self, inNode):
        """
        노드가 유효한 스킨 본인지 확인
        
        Args:
            inNode: 확인할 노드
            
        Returns:
            True: 유효한 본인 경우
            False: 아닌 경우
        """
        return (rt.superClassOf(inNode) == rt.GeometryClass or 
                rt.classOf(inNode) == rt.BoneGeometry or 
                rt.superClassOf(inNode) == rt.Helper)
    
    def get_skin_mod(self, obj=None):
        """
        객체의 스킨 모디파이어 배열 반환
        
        Args:
            obj: 모디파이어를 가져올 객체 (기본값: 현재 선택된 객체)
            
        Returns:
            스킨 모디파이어 배열
        """
        if obj is None:
            if len(rt.selection) > 0:
                obj = rt.selection[0]
            else:
                return []
        
        return [mod for mod in obj.modifiers if rt.classOf(mod) == rt.Skin]
    
    def bind_skin(self, obj, bone_array):
        """
        객체에 스킨 모디파이어 바인딩
        
        Args:
            obj: 바인딩할 객체
            bone_array: 바인딩할 본 배열
            
        Returns:
            True: 성공한 경우
            False: 실패한 경우
        """
        if obj is None or len(bone_array) < 1:
            print("Select at least 1 influence and an object.")
            return False
        
        # Switch to modify mode
        rt.execute("max modify mode")
        
        # Check if the object is valid for skinning
        if rt.superClassOf(obj) != rt.GeometryClass:
            print(f"{obj.name} must be 'Edit_Mesh' or 'Edit_Poly'.")
            return False
        
        # Add skin modifier
        objmod = rt.Skin()
        rt.addModifier(obj, objmod)
        rt.select(obj)
        
        # Add bones to skin modifier
        wgt = 1.0
        for each in bone_array:
            rt.skinOps.addBone(objmod, each, wgt)
        
        # Set skin modifier options
        objmod.filter_vertices = True
        objmod.filter_envelopes = False
        objmod.filter_cross_sections = True
        objmod.enableDQ = False
        objmod.bone_Limit = 8
        objmod.colorAllWeights = True
        objmod.showNoEnvelopes = True
        
        return True
    
    def optimize_skin(self, skin_mod, bone_limit=8, skin_tolerance=0.01):
        """
        스킨 모디파이어 최적화
        
        Args:
            skin_mod: 스킨 모디파이어
            bone_limit: 본 제한 수 (기본값: 8)
            skin_tolerance: 스킨 가중치 허용 오차 (기본값: 0.01)
        """
        # 스킨 모디파이어 설정
        skin_mod.enableDQ = False
        skin_mod.bone_Limit = bone_limit
        skin_mod.clearZeroLimit = skin_tolerance
        rt.skinOps.RemoveZeroWeights(skin_mod)
        skin_mod.clearZeroLimit = 0
        
        if rt.skinOps.getNumberBones(skin_mod) > 1:
            list_of_bones = [i for i in range(1, rt.skinOps.GetNumberBones(skin_mod) + 1)]
            
            for v in range(1, rt.skinOps.GetNumberVertices(skin_mod) + 1):
                for b in range(1, rt.skinOps.GetVertexWeightCount(skin_mod, v) + 1):
                    bone_id = rt.skinOps.GetVertexWeightBoneID(skin_mod, v, b)
                    if bone_id in list_of_bones:
                        list_of_bones.remove(bone_id)
            
            # 역순으로 본 제거 (인덱스 변경 문제 방지)
            for i in range(len(list_of_bones) - 1, -1, -1):
                bone_id = list_of_bones[i]
                rt.skinOps.SelectBone(skin_mod, bone_id)
                rt.skinOps.removebone(skin_mod, bone_id)
                
            if rt.skinOps.getNumberBones(skin_mod) > 1:
                rt.skinOps.SelectBone(skin_mod, 1)
                
            skin_mod_obj = rt.getCurrentSelection()[0]
                
            print(f"Obj:{skin_mod_obj.name} Removed:{len(list_of_bones)} Left:{rt.skinOps.GetNumberBones(skin_mod)}")
    
    def optimize_skin_process(self, objs=None, optim_all_skin_mod=False, bone_limit=8, skin_tolerance=0.01):
        """
        여러 객체의 스킨 최적화 프로세스
        
        Args:
            objs: 최적화할 객체 배열 (기본값: 현재 선택된 객체들)
            optim_all_skin_mod: 모든 스킨 모디파이어 최적화 여부 (기본값: False)
            bone_limit: 본 제한 수 (기본값: 8)
            skin_tolerance: 스킨 가중치 허용 오차 (기본값: 0.01)
        """
        if objs is None:
            objs = rt.selection
            
        if not objs:
            return
            
        rt.execute("max modify mode")
        
        for obj in objs:
            if self.has_skin(obj):
                mod_id = [i+1 for i in range(len(obj.modifiers)) if rt.classOf(obj.modifiers[i]) == rt.Skin]
                
                if not optim_all_skin_mod:
                    mod_id = [mod_id[0]]
                    
                for each in mod_id:
                    rt.modPanel.setCurrentObject(obj.modifiers[each-1])
                    self.optimize_skin(obj.modifiers[each-1], bone_limit=bone_limit, skin_tolerance=skin_tolerance)
        
        rt.select(objs)
    
    def load_skin(self, obj, file_path, load_bind_pose=False, keep_skin=False):
        """
        스킨 데이터 로드
        
        Args:
            obj: 로드할 객체
            file_path: 스킨 파일 경로
            load_bind_pose: 바인드 포즈 로드 여부
            keep_skin: 기존 스킨 유지 여부
            
        Returns:
            누락된 본 배열
        """
        # 기본값 설정
        if keep_skin != True:
            keep_skin = False
            
        # 객체 선택
        rt.select(obj)
        data = []
        missing_bones = []
        
        # 파일 열기
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    data.append(line.strip())
        except:
            return []
        
        # 버텍스 수 확인
        if len(data) - 1 != obj.verts.count or obj.verts.count == 0:
            print("Bad number of verts")
            return []
        
        # 기존 스킨 모디파이어 처리
        if not keep_skin:
            for i in range(len(obj.modifiers) - 1, -1, -1):
                if rt.classOf(obj.modifiers[i]) == rt.Skin:
                    rt.deleteModifier(obj, i+1)
                    
        # 모디파이 모드 설정
        rt.setCommandPanelTaskMode(rt.Name('modify'))
        
        # 새 스킨 모디파이어 생성
        new_skin = rt.Skin()
        rt.addModifier(obj, new_skin, before=1 if keep_skin else 0)
        
        # 스킨 이름 설정
        if keep_skin:
            new_skin.name = "Skin_" + os.path.splitext(os.path.basename(file_path))[0]
            
        # 현재 모디파이어 설정
        rt.modPanel.setCurrentObject(new_skin)
        
        tempData = [rt.execute(item) for item in data]
        
        # 본 데이터 처리
        bones_data = rt.execute(tempData[0])
        hierarchy = []
        
        for i in range(len(bones_data)):
            # 본 이름으로 노드 찾기
            my_bone = [node for node in rt.objects if node.name == bones_data[i]]
            
            # 없는 본인 경우 더미 생성
            if len(my_bone) == 0:
                print(f"Missing bone: {bones_data[i]}")
                tmp = rt.Dummy(name=bones_data[i])
                my_bone = [tmp]
                missing_bones.append(tmp)
                
            # 계층 구조 확인
            if len(my_bone) > 1 and len(hierarchy) != 0:
                print(f"Multiple bones are named: {my_bone[0].name} ({len(my_bone)})")
                good_bone = None
                for o in my_bone:
                    if o in hierarchy:
                        good_bone = o
                        break
                if good_bone is not None:
                    my_bone = [good_bone]
                    
            # 사용할 본 결정
            my_bone = my_bone[0]
            
            # 계층에 추가
            if my_bone not in hierarchy:
                hierarchy.append(my_bone)
                all_nodes = list(hierarchy)
                
                for node in all_nodes:
                    # 자식 노드 추가
                    for child in node.children:
                        if child not in all_nodes:
                            all_nodes.append(child)
                    # 부모 노드 추가
                    if node.parent is not None and node.parent not in all_nodes:
                        all_nodes.append(node.parent)
                        
                    # 계층에 추가
                    for node in all_nodes:
                        if self.is_valid_bone(node) and node not in hierarchy:
                            hierarchy.append(node)
                            
            # 본 추가
            rt.skinOps.addBone(new_skin, my_bone, 1.0)
            
            # 바인드 포즈 로드
            if load_bind_pose:
                bind_pose_file = os.path.splitext(file_path)[0] + "bp"
                bind_poses = []
                
                if os.path.exists(bind_pose_file):
                    try:
                        with open(bind_pose_file, 'r') as f:
                            for line in f:
                                bind_poses.append(rt.execute(line.strip()))
                    except:
                        pass
                        
                if i < len(bind_poses) and bind_poses[i] is not None:
                    rt.skinUtils.SetBoneBindTM(obj, my_bone, bind_poses[i])
        
        # 가중치 데이터 처리
        for i in range(1, obj.verts.count + 1):
            bone_id = []
            bone_weight = []
            good_bones = []
            all_bone_weight = [0] * len(bones_data)
            
            # 가중치 합산
            for b in range(len(tempData[i][0])):
                bone_index = tempData[i][0][b]
                weight = tempData[i][1][b]
                all_bone_weight[bone_index-1] += weight
                good_bones.append(bone_index)
                
            # 가중치 적용
            for b in good_bones:
                bone_id.append(b)
                bone_weight.append(all_bone_weight[b-1])
                
            # 가중치 설정
            if len(bone_id) != 0:
                rt.skinOps.SetVertexWeights(new_skin, i, bone_id[0], 1.0)  # Max 2014 sp5 hack
                rt.skinOps.ReplaceVertexWeights(new_skin, i, bone_id, bone_weight)
                
        return missing_bones
    
    def save_skin(self, obj=None, file_path=None):
        """
        스킨 데이터 저장
        MAXScript의 saveskin.ms 를 Python으로 변환한 함수
        
        Args:
            obj: 저장할 객체 (기본값: 현재 선택된 객체)
            file_path: 저장할 파일 경로 (기본값: None, 자동 생성)
            
        Returns:
            저장된 파일 경로
        """
        # 현재 선택된 객체가 없는 경우 선택된 객체 사용
        if obj is None:
            if len(rt.selection) > 0:
                obj = rt.selection[0]
            else:
                print("No object selected")
                return None
                
        # 현재 스킨 모디파이어 가져오기
        skin_mod = rt.modPanel.getCurrentObject()
        
        # 스킨 모디파이어가 아니거나 본이 없는 경우 종료
        if rt.classOf(skin_mod) != rt.Skin or rt.skinOps.GetNumberBones(skin_mod) <= 0:
            print("Current modifier is not a Skin modifier or has no bones")
            return None
            
        # 본 리스트 생성
        bones_list = []
        for i in range(1, rt.skinOps.GetNumberBones(skin_mod) + 1):
            bones_list.append(rt.skinOps.GetBoneName(skin_mod, i, 1))
        
        # 스킨 데이터 생성
        skin_data = "\"#(\\\"" + "\\\",\\\"".join(str(x) for x in bones_list) + "\\\")\"\n"
            
        # 버텍스별 가중치 데이터 수집
        for v in range(1, rt.skinOps.GetNumberVertices(skin_mod) + 1):
            bone_array = []
            weight_array = []
            
            for b in range(1, rt.skinOps.GetVertexWeightCount(skin_mod, v) + 1):
                bone_array.append(rt.skinOps.GetVertexWeightBoneID(skin_mod, v, b))
                weight_array.append(rt.skinOps.GetVertexWeight(skin_mod, v, b))
            
            stringBoneArray = "#(" + ",".join(str(x) for x in bone_array) + ")"
            stringWeightArray = "#(" + ",".join(str(w) for w in weight_array) + ")"
            skin_data += ("#(" + stringBoneArray + ", " + stringWeightArray + ")\n")
            
        # 파일 경로가 지정되지 않은 경우 자동 생성
        if file_path is None:
            # animations 폴더 내 skindata 폴더 생성
            animations_dir = rt.getDir(rt.Name('animations'))
            skin_data_dir = os.path.join(animations_dir, "skindata")
            
            if not os.path.exists(skin_data_dir):
                os.makedirs(skin_data_dir)
                
            # 파일명 생성 (객체명 + 버텍스수 + 면수)
            file_name = f"{obj.name} [v{obj.mesh.verts.count}] [t{obj.mesh.faces.count}].skin"
            file_path = os.path.join(skin_data_dir, file_name)
            
        print(f"Saving to: {file_path}")
        
        # 스킨 데이터 파일 저장
        try:
            with open(file_path, 'w') as f:
                for data in skin_data:
                    f.write(data)
        except Exception as e:
            print(f"Error saving skin data: {e}")
            return None
            
        # 바인드 포즈 데이터 수집 및 저장
        bind_poses = []
        for i in range(1, rt.skinOps.GetNumberBones(skin_mod) + 1):
            bone_name = rt.skinOps.GetBoneName(skin_mod, i, 1)
            bone_node = rt.getNodeByName(bone_name)
            bind_pose = rt.skinUtils.GetBoneBindTM(obj, bone_node)
            bind_poses.append(bind_pose)
            
        # 바인드 포즈 파일 저장
        bind_pose_file = file_path[:-4] + "bp"  # .skin -> .bp
        try:
            with open(bind_pose_file, 'w') as f:
                for pose in bind_poses:
                    f.write(str(pose) + '\n')
        except Exception as e:
            print(f"Error saving bind pose data: {e}")
            
        return file_path
    
    def get_bone_id(self, skin_mod, b_array, type=1, refresh=True):
        """
        스킨 모디파이어에서 본 ID 가져오기
        
        Args:
            skin_mod: 스킨 모디파이어
            b_array: 본 배열
            type: 0=객체, 1=객체 이름
            refresh: 인터페이스 업데이트 여부
            
        Returns:
            본 ID 배열
        """
        bone_id = []
        
        if refresh:
            rt.modPanel.setCurrentObject(skin_mod)
            
        for i in range(1, rt.skinOps.GetNumberBones(skin_mod) + 1):
            if type == 0:
                bone_name = rt.skinOps.GetBoneName(skin_mod, i, 1)
                id = b_array.index(bone_name) + 1 if bone_name in b_array else 0
            elif type == 1:
                bone = rt.getNodeByName(rt.skinOps.GetBoneName(skin_mod, i, 1))
                id = b_array.index(bone) + 1 if bone in b_array else 0
                
            if id != 0:
                bone_id.append(i)
                
        return bone_id
    
    def get_bone_id_from_name(self, in_skin_mod, bone_name):
        """
        본 이름으로 본 ID 가져오기
        
        Args:
            in_skin_mod: 스킨 모디파이어를 가진 객체
            bone_name: 본 이름
            
        Returns:
            본 ID
        """
        for i in range(1, rt.skinOps.GetNumberBones(in_skin_mod) + 1):
            if rt.skinOps.GetBoneName(in_skin_mod, i, 1) == bone_name:
                return i
        return None
    
    def get_bones_from_skin(self, objs, skin_mod_index):
        """
        스킨 모디파이어에서 사용된 본 배열 가져오기
        
        Args:
            objs: 객체 배열
            skin_mod_index: 스킨 모디파이어 인덱스
            
        Returns:
            본 배열
        """
        inf_list = []
        
        for obj in objs:
            if rt.isValidNode(obj):
                deps = rt.refs.dependsOn(obj.modifiers[skin_mod_index])
                for n in deps:
                    if rt.isValidNode(n) and self.is_valid_bone(n):
                        if n not in inf_list:
                            inf_list.append(n)
                            
        return inf_list
    
    def find_skin_mod_id(self, obj):
        """
        객체에서 스킨 모디파이어 인덱스 찾기
        
        Args:
            obj: 대상 객체
            
        Returns:
            스킨 모디파이어 인덱스 배열
        """
        return [i+1 for i in range(len(obj.modifiers)) if rt.classOf(obj.modifiers[i]) == rt.Skin]
    
    def sel_vert_from_bones(self, skin_mod, threshold=0.01):
        """
        선택된 본에 영향 받는 버텍스 선택
        
        Args:
            skin_mod: 스킨 모디파이어
            threshold: 가중치 임계값 (기본값: 0.01)
            
        Returns:
            선택된 버텍스 배열
        """
        verts_to_sel = []
        
        if skin_mod is not None:
            le_bone = rt.skinOps.getSelectedBone(skin_mod)
            svc = rt.skinOps.GetNumberVertices(skin_mod)
            
            for o in range(1, svc + 1):
                lv = rt.skinOps.GetVertexWeightCount(skin_mod, o)
                
                for k in range(1, lv + 1):
                    if rt.skinOps.GetVertexWeightBoneID(skin_mod, o, k) == le_bone:
                        if rt.skinOps.GetVertexWeight(skin_mod, o, k) >= threshold:
                            if o not in verts_to_sel:
                                verts_to_sel.append(o)
                                
            rt.skinOps.SelectVertices(skin_mod, verts_to_sel)
            
        else:
            print("You must have a skinned object selected")
            
        return verts_to_sel
    
    def make_rigid_skin(self, skin_mod, vert_list):
        """
        버텍스 가중치를 경직화(rigid) 처리
        
        Args:
            skin_mod: 스킨 모디파이어
            vert_list: 버텍스 리스트
            
        Returns:
            [본 ID 배열, 가중치 배열]
        """
        weight_array = {}
        vert_count = 0
        bone_array = []
        final_weight = []
        
        # 가중치 수집
        for v in vert_list:
            for cur_bone in range(1, rt.skinOps.GetVertexWeightCount(skin_mod, v) + 1):
                cur_id = rt.skinOps.GetVertexWeightBoneID(skin_mod, v, cur_bone)
                
                if cur_id not in weight_array:
                    weight_array[cur_id] = 0
                    
                cur_weight = rt.skinOps.GetVertexWeight(skin_mod, v, cur_bone)
                weight_array[cur_id] += cur_weight
                vert_count += cur_weight
                
        # 최종 가중치 계산
        for i in weight_array:
            if weight_array[i] > 0:
                new_val = weight_array[i] / vert_count
                if new_val > 0.01:
                    bone_array.append(i)
                    final_weight.append(new_val)
                    
        return [bone_array, final_weight]
    
    def transfert_skin_data(self, obj, source_bones, target_bones, vtx_list):
        """
        스킨 가중치 데이터 이전
        
        Args:
            obj: 대상 객체
            source_bones: 원본 본 배열
            target_bones: 대상 본
            vtx_list: 버텍스 리스트
        """
        skin_data = []
        new_skin_data = []
        
        # 본 ID 가져오기
        source_bones_id = [self.get_bone_id_from_name(obj, b.name) for b in source_bones]
        target_bone_id = self.get_bone_id_from_name(obj, target_bones.name)
        
        bone_list = [n for n in rt.refs.dependsOn(obj.skin) if rt.isValidNode(n) and self.is_valid_bone(n)]
        bone_id_map = {self.get_bone_id_from_name(obj, b.name): i for i, b in enumerate(bone_list)}
        
        # 스킨 데이터 수집
        for vtx in vtx_list:
            bone_array = []
            weight_array = []
            bone_weight = [0] * len(bone_list)
            
            for b in range(1, rt.skinOps.GetVertexWeightCount(obj.skin, vtx) + 1):
                bone_idx = rt.skinOps.GetVertexWeightBoneID(obj.skin, vtx, b)
                bone_weight[bone_id_map[bone_idx]] += rt.skinOps.GetVertexWeight(obj.skin, vtx, b)
                
            for b in range(len(bone_weight)):
                if bone_weight[b] > 0:
                    bone_array.append(b+1)
                    weight_array.append(bone_weight[b])
                    
            skin_data.append([bone_array, weight_array])
            new_skin_data.append([bone_array[:], weight_array[:]])
            
        # 스킨 데이터 이전
        for b, source_bone_id in enumerate(source_bones_id):
            vtx_id = []
            vtx_weight = []
            
            # 원본 본의 가중치 추출
            for vtx in range(len(skin_data)):
                for i in range(len(skin_data[vtx][0])):
                    if skin_data[vtx][0][i] == source_bone_id:
                        vtx_id.append(vtx)
                        vtx_weight.append(skin_data[vtx][1][i])
                        
            # 원본 본 영향력 제거
            for vtx in range(len(vtx_id)):
                for i in range(len(new_skin_data[vtx_id[vtx]][0])):
                    if new_skin_data[vtx_id[vtx]][0][i] == source_bone_id:
                        new_skin_data[vtx_id[vtx]][1][i] = 0.0
                        
            # 타겟 본에 영향력 추가
            for vtx in range(len(vtx_id)):
                id = new_skin_data[vtx_id[vtx]][0].index(target_bone_id) if target_bone_id in new_skin_data[vtx_id[vtx]][0] else -1
                
                if id == -1:
                    new_skin_data[vtx_id[vtx]][0].append(target_bone_id)
                    new_skin_data[vtx_id[vtx]][1].append(vtx_weight[vtx])
                else:
                    new_skin_data[vtx_id[vtx]][1][id] += vtx_weight[vtx]
                    
        # 스킨 데이터 적용
        for i in range(len(vtx_list)):
            rt.skinOps.ReplaceVertexWeights(obj.skin, vtx_list[i], 
                                           skin_data[i][0], new_skin_data[i][1])
    
    def smooth_skin(self, smooth_skin_data=None, vert_group_mode=1, smooth_radius=5.0, keep_max=False, smooth_skin_max_undo=10, undo_weights=None):
        """
        스킨 가중치 스무딩 적용
        
        Args:
            smooth_skin_data: 스무딩 데이터 캐시
            vert_group_mode: 버텍스 그룹 모드 (1=이웃 버텍스, 2=선택되지 않은 버텍스, 3=반경 내 모든 버텍스, 4=엘리먼트/루프)
            smooth_radius: 스무딩 반경
            keep_max: 최대 가중치 보존 여부
            smooth_skin_max_undo: 최대 언두 스택 수
            undo_weights: 언두 가중치 데이터
            
        Returns:
            업데이트된 undo_weights 리스트
        """
        # 초기화
        if smooth_skin_data is None:
            smooth_skin_data = [[] for _ in range(8)]
        if undo_weights is None:
            undo_weights = []
            
        obj = rt.selection[0] if len(rt.selection) > 0 else None
        skin_mod = rt.modPanel.getCurrentObject()
        final_bone_array = {}
        final_weight_array = {}
            
        # 데이터 캐시 확인 및 초기화
        use_old_data = False
        if len(smooth_skin_data[0]) > 0:
            if len(smooth_skin_data[0]) >= 2:
                if obj == smooth_skin_data[0][0] and obj.verts.count == smooth_skin_data[0][1]:
                    use_old_data = True
                    
        if not use_old_data:
            smooth_skin_data = [[] for _ in range(8)]
            if obj is not None:
                smooth_skin_data[0] = [obj, obj.verts.count]
        
        # 임시 객체 복사
        tmp_obj = rt.copy(obj)
        tmp_obj.modifiers[skin_mod.name].enabled = False
        
        # 정규화 가중치 함수 정의
        def do_normalize_weight(weight):
            weight_length = sum(weight)
            if weight_length != 0:
                return [w * (1 / weight_length) for w in weight]
            else:
                return [1.0] + [0.0] * (len(weight) - 1) if len(weight) > 0 else [1.0]
        
        # 영향치 0인 버텍스 제거
        skin_mod.clearZeroLimit = 0.0
        rt.skinOps.RemoveZeroWeights(skin_mod)
        
        # 위치 배열 캐시
        pos_array = [v.pos for v in tmp_obj.verts]
        
        # 반경이 변경된 경우 캐시 초기화
        if len(smooth_skin_data) > 7 and smooth_skin_data[7] != smooth_radius:
            smooth_skin_data[5] = []
            smooth_skin_data[6] = []
            
        # 각 선택된 버텍스에 대해 처리
        for v in range(1, obj.verts.count + 1):
            # 버텍스가 선택되고 최대값 보존 조건을 충족하는 경우만 처리
            if rt.skinOps.IsVertexSelected(skin_mod, v) == 1 and (not keep_max or rt.skinOps.GetVertexWeightCount(skin_mod, v) != 1):
                vert_bros = set()
                vert_bros_ratio = []
                weight_array = []
                bone_array = []
                final_weight = []
                
                # 배열 초기화
                weight_array = [None] * (rt.skinOps.GetNumberBones(skin_mod) + 1)
                
                # 버텍스 그룹 모드 1: 이웃 버텍스
                if vert_group_mode == 1 and v not in smooth_skin_data[1]:
                    # 폴리곤이나 메시 타입에 따라 버텍스 연결 정보 가져오기
                    if rt.classOf(tmp_obj) == rt.Editable_Poly or rt.classOf(tmp_obj) == rt.PolyMeshObject:
                        cur_edges = rt.polyop.GetEdgesUsingVert(tmp_obj, v)
                        for ce in cur_edges:
                            edge_verts = rt.polyop.getEdgeVerts(tmp_obj, ce)
                            vert_bros.update(edge_verts)
                    else:
                        cur_edges = rt.meshop.GetEdgesUsingvert(tmp_obj, v)
                        for i in range(len(cur_edges)):
                            edge_idx = cur_edges[i]
                            edge_vis = rt.getEdgeVis(tmp_obj, 1 + (edge_idx - 1) // 3, 1 + (edge_idx - 1) % 3)
                            cur_edges[i] = edge_vis
                        for ce in cur_edges:
                            edge_verts = rt.meshop.getVertsUsingEdge(tmp_obj, ce)
                            vert_bros.update(edge_verts)
                    
                    # 배열로 변환
                    vert_bros = list(vert_bros)
                    smooth_skin_data[1][v] = []
                    smooth_skin_data[2][v] = []
                    
                    # 이웃 버텍스가 있으면 가중치 계산
                    if len(vert_bros) > 0:
                        for vb in vert_bros:
                            cur_dist = rt.distance(pos_array[v-1], pos_array[vb-1])
                            vert_bros_ratio.append(0 if cur_dist == 0 else 1 / cur_dist)
                            
                        # 가중치 정규화
                        vert_bros_ratio = do_normalize_weight(vert_bros_ratio)
                        
                        # 자기 자신의 가중치는 1로 설정
                        if v in vert_bros:
                            self_idx = vert_bros.index(v)
                            vert_bros_ratio[self_idx] = 1
                            
                        smooth_skin_data[1][v] = vert_bros
                        smooth_skin_data[2][v] = vert_bros_ratio
                
                # 버텍스 그룹 모드 2: 선택되지 않은 버텍스
                if vert_group_mode == 2:
                    smooth_skin_data[3][v] = []
                    for vb in range(1, len(pos_array) + 1):
                        if rt.skinOps.IsVertexSelected(skin_mod, vb) == 0:
                            if rt.distance(pos_array[v-1], pos_array[vb-1]) < smooth_radius:
                                smooth_skin_data[3][v].append(vb)
                    
                    smooth_skin_data[4][v] = []
                    for vb in smooth_skin_data[3][v]:
                        cur_dist = rt.distance(pos_array[v-1], pos_array[vb-1])
                        smooth_skin_data[4][v].append(0 if cur_dist == 0 else 1 / cur_dist)
                    
                    # 가중치 정규화 및 강화
                    smooth_skin_data[4][v] = do_normalize_weight(smooth_skin_data[4][v])
                    smooth_skin_data[4][v] = [w * 2 for w in smooth_skin_data[4][v]]
                
                # 버텍스 그룹 모드 3: 반경 내 모든 버텍스
                if vert_group_mode == 3 and v not in smooth_skin_data[5]:
                    smooth_skin_data[5][v] = []
                    for vb in range(1, len(pos_array) + 1):
                        if rt.distance(pos_array[v-1], pos_array[vb-1]) < smooth_radius:
                            smooth_skin_data[5][v].append(vb)
                    
                    smooth_skin_data[6][v] = []
                    for vb in smooth_skin_data[5][v]:
                        cur_dist = rt.distance(pos_array[v-1], pos_array[vb-1])
                        smooth_skin_data[6][v].append(0 if cur_dist == 0 else 1 / cur_dist)
                    
                    # 가중치 정규화 및 강화
                    smooth_skin_data[6][v] = do_normalize_weight(smooth_skin_data[6][v])
                    smooth_skin_data[6][v] = [w * 2 for w in smooth_skin_data[6][v]]
                
                # 엘리먼트/루프 모드가 아닌 경우 가중치 계산
                if vert_group_mode != 4:
                    # 현재 버텍스 그룹 모드에 따라 데이터 가져오기
                    vert_bros = smooth_skin_data[vert_group_mode * 2 - 1][v]
                    vert_bros_ratio = smooth_skin_data[vert_group_mode * 2][v]
                    
                    # 각 이웃 버텍스의 가중치 반영
                    for z in range(len(vert_bros)):
                        for cur_bone in range(1, rt.skinOps.GetVertexWeightCount(skin_mod, vert_bros[z]) + 1):
                            cur_id = rt.skinOps.GetVertexWeightBoneID(skin_mod, vert_bros[z], cur_bone)
                            if weight_array[cur_id] is None:
                                weight_array[cur_id] = 0
                            weight_array[cur_id] += rt.skinOps.GetVertexWeight(skin_mod, vert_bros[z], cur_bone) * vert_bros_ratio[z]
                    
                    # 최종 가중치 계산
                    for i in range(1, len(weight_array)):
                        if weight_array[i] is not None and weight_array[i] > 0:
                            new_val = weight_array[i] / 2
                            if new_val > 0.01:
                                bone_array.append(i)
                                final_weight.append(new_val)
                    
                    final_bone_array[v] = bone_array
                    final_weight_array[v] = final_weight
        
        # 버텍스 그룹 모드 4: 엘리먼트/루프
        if vert_group_mode == 4:
            # 임시 객체를 폴리곤으로 변환
            rt.convertToPoly(tmp_obj)
            poly_obj = tmp_obj
            
            # 선택된 버텍스만 대상으로 처리
            vert_selection = []
            for v in range(1, obj.verts.count + 1):
                if rt.skinOps.IsVertexSelected(skin_mod, v) == 1:
                    vert_selection.append(v)
            
            # 선택되지 않은 엣지와 페이스 계산
            done_edge = rt.BitArray(poly_obj.edges)
            edges_using_vert = rt.polyop.getEdgesUsingVert(poly_obj, vert_selection)
            done_edge = done_edge - edges_using_vert
            
            done_face = rt.BitArray(poly_obj.faces)
            faces_using_vert = rt.polyop.getFacesUsingVert(poly_obj, vert_selection)
            done_face = done_face - faces_using_vert
            
            # 작은 엘리먼트 찾기
            small_elements = []
            for f in range(1, poly_obj.faces.count + 1):
                if not done_face[f]:
                    cur_element = rt.polyop.getElementsUsingFace(poly_obj, rt.BitArray(f))
                    cur_verts = rt.polyop.getVertsUsingFace(poly_obj, cur_element)
                    max_dist = 0
                    
                    # 최대 거리 계산
                    for v1 in cur_verts:
                        for v2 in cur_verts:
                            if max_dist < (smooth_radius * 2):
                                dist = rt.distance(poly_obj.verts[v1-1].pos, poly_obj.verts[v2-1].pos)
                                if dist > max_dist:
                                    max_dist = dist
                    
                    # 반경 이내의 작은 엘리먼트 추가
                    if max_dist < (smooth_radius * 2):
                        small_elements.append(list(cur_verts))
                    
                    done_face = done_face | cur_element
            
            # 엣지 루프 찾기
            edge_loops = []
            for ed in small_elements:
                edges = rt.polyop.getEdgesUsingVert(poly_obj, ed)
                done_edge = done_edge | edges
                
            for ed in range(1, poly_obj.edges.count + 1):
                if not done_edge[ed]:
                    poly_obj.selectedEdges = rt.BitArray(ed)
                    poly_obj.ButtonOp(rt.Name("SelectEdgeLoop"))
                    cur_edge_loop = poly_obj.selectedEdges
                    
                    if cur_edge_loop.numberSet > 2:
                        cur_verts = rt.polyop.getvertsusingedge(poly_obj, cur_edge_loop)
                        max_dist = 0
                        
                        # 최대 거리 계산
                        for v1 in cur_verts:
                            for v2 in cur_verts:
                                if max_dist < (smooth_radius * 2):
                                    dist = rt.distance(poly_obj.verts[v1-1].pos, poly_obj.verts[v2-1].pos)
                                    if dist > max_dist:
                                        max_dist = dist
                        
                        # 반경 이내의 엣지 루프 추가
                        if max_dist < (smooth_radius * 2):
                            edge_loops.append(list(cur_verts))
                        
                    done_edge = done_edge | cur_edge_loop
            
            # 스킨 모드 설정
            rt.modPanel.setCurrentObject(skin_mod)
            rt.subObjectLevel = 1
            
            # 엘리먼트와 엣지 루프에 대해 가중치 계산
            for z in [small_elements, edge_loops]:
                for i in z:
                    vert_list = []
                    for v3 in i:
                        if rt.skinOps.IsVertexSelected(skin_mod, v3) == 1:
                            vert_list.append(v3)
                    
                    # 가중치 계산
                    if len(vert_list) > 0:
                        new_weights = self.make_rigid_skin(skin_mod, vert_list)
                        for v3 in vert_list:
                            final_bone_array[v3] = new_weights[0]
                            final_weight_array[v3] = new_weights[1]
        
        # 반경 정보 저장
        if len(smooth_skin_data) <= 7:
            smooth_skin_data.append(None)
        smooth_skin_data[7] = smooth_radius
        
        # 임시 객체 삭제
        rt.delete(tmp_obj)
        
        # 가중치 적용 및 언두 데이터 저장
        old_weight_array = []
        old_bone_array = []
        last_weights = []
        
        for sv in final_bone_array:
            if final_bone_array[sv] and len(final_bone_array[sv]) > 0:
                # 언두를 위한 현재 가중치 저장
                num_item = rt.skinOps.GetVertexWeightCount(skin_mod, sv)
                old_weight_array = [0] * num_item
                old_bone_array = [0] * num_item
                
                for cur_bone in range(1, num_item + 1):
                    old_bone_array[cur_bone-1] = rt.skinOps.GetVertexWeightBoneID(skin_mod, sv, cur_bone)
                    old_weight_array[cur_bone-1] = rt.skinOps.GetVertexWeight(skin_mod, sv, cur_bone)
                
                # 언두 스택 저장
                last_weights.append([skin_mod, sv, list(old_bone_array), list(old_weight_array)])
                if len(undo_weights) >= smooth_skin_max_undo:
                    undo_weights.pop(0)  # 가장 오래된 항목 제거
                
                # 새 가중치 적용
                rt.skinOps.ReplaceVertexWeights(skin_mod, sv, final_bone_array[sv], final_weight_array[sv])
        
        # 언두 스택에 추가
        if last_weights:
            undo_weights.append(last_weights)
            
        return undo_weights
    
    def smooth_skin_iter(self, vert_group_mode=1, smooth_radius=5.0, keep_max=False, max_iter=3, smooth_skin_max_undo=10):
        """
        스킨 가중치 스무딩을 여러번 반복 적용
        
        Args:
            vert_group_mode: 버텍스 그룹 모드 (1=이웃 버텍스, 2=선택되지 않은 버텍스, 3=반경 내 모든 버텍스, 4=엘리먼트/루프)
            smooth_radius: 스무딩 반경
            keep_max: 최대 가중치 보존 여부
            max_iter: 반복 횟수
            smooth_skin_max_undo: 최대 언두 스택 수
            
        Returns:
            True: 성공
            False: 실패
        """
        if len(rt.selection) != 1:
            return False
            
        # 초기화
        undo_weights = []
        smooth_skin_data = [[] for _ in range(8)]
        
        # 반복 적용
        for iter in range(max_iter):
            # 스무딩 적용
            undo_weights = self.smooth_skin(
                smooth_skin_data=smooth_skin_data,
                vert_group_mode=vert_group_mode,
                smooth_radius=smooth_radius,
                keep_max=keep_max,
                smooth_skin_max_undo=smooth_skin_max_undo,
                undo_weights=undo_weights
            )
            
            # 진행상황 출력
            progress = ((iter + 1) / max_iter) * 100.0
            print(f"Smoothing progress: {progress:.1f}%")
            
        return True
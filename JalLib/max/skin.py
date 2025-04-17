#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
스킨 모듈 - 3ds Max용 스킨 관련 기능 제공
원본 MAXScript의 skin.ms를 Python으로 변환하였으며, pymxs 모듈 기반으로 구현됨
"""

from dataclasses import dataclass
from pymxs import runtime as rt


@dataclass
class SkinVert:
    """
    스킨 버텍스 정보를 저장하는 데이터 클래스
    """
    index: int = 0
    boneArray: list = None
    boneIDArray: list = None
    boneNameArray: list = None
    weightArray: list = None
    
    def __post_init__(self):
        if self.boneArray is None:
            self.boneArray = []
        if self.boneIDArray is None:
            self.boneIDArray = []
        if self.boneNameArray is None:
            self.boneNameArray = []
        if self.weightArray is None:
            self.weightArray = []


class Skin:
    """
    스킨 관련 기능을 제공하는 클래스.
    MAXScript의 _Skin 구조체 개념을 Python으로 재구현한 클래스이며,
    3ds Max의 기능들을 pymxs API를 통해 제어합니다.
    """
    
    def __init__(self, name_service, prog_service=None):
        """
        클래스 초기화
        
        Args:
            name_service: Name 서비스 인스턴스
            prog_service: Progress 서비스 인스턴스 (선택 사항)
        """
        self.name = name_service
        self.prog = prog_service
        
        self.skinMod = None
        self.modIndex = 0
        self.allBoneNamesArray = []
        self.allBonesArray = []
        self.skinWeightsArray = []
    
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
    
    def is_valid_bone(self, node):
        """
        노드가 유효한 스킨 본인지 확인
        
        Args:
            node: 확인할 노드
            
        Returns:
            True: 유효한 본인 경우
            False: 아닌 경우
        """
        return (rt.superClassOf(node) == rt.GeometryClass or 
                rt.classOf(node) == rt.BoneGeometry or 
                rt.superClassOf(node) == rt.Helper)
    
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
    
    def find_skin(self, input_obj):
        """
        객체에서 스킨 모디파이어를 찾아 인덱스 반환
        
        Args:
            input_obj: 스킨 모디파이어를 찾을 객체
            
        Returns:
            스킨 모디파이어 인덱스 (없으면 0)
        """
        return_val = 0
        
        if len(input_obj.modifiers) == 0:
            return return_val
        
        for i in range(len(input_obj.modifiers)):
            if rt.classOf(input_obj.modifiers[i]) == rt.Skin:
                self.skinMod = input_obj.modifiers[i]
                self.modIndex = i
                return_val = i + 1  # MaxScript는 1-based, Python은 0-based이므로 조정
        
        return return_val
    
    def select_skin_obj(self, input_obj):
        """
        스킨이 있는 객체를 선택하고 모디파이어 패널에서 스킨 선택
        
        Args:
            input_obj: 선택할 객체
            
        Returns:
            True: 성공한 경우
            False: 실패한 경우
        """
        return_val = False
        
        if self.find_skin(input_obj) == 0:
            return return_val
        
        rt.max.setModifierMode()  # max modify mode
        rt.select(input_obj)
        rt.modPanel.setCurrentObject(input_obj.modifiers[self.modIndex])
        rt.subObjectLevel = 1
        return_val = True
        
        return return_val
    
    def get_all_bones(self, input_obj):
        """
        스킨 모디파이어의 모든 본 배열 반환
        
        Args:
            input_obj: 스킨 모디파이어가 있는 객체
        
        Returns:
            True: 본을 찾은 경우
            False: 본을 찾지 못한 경우
        """
        return_val = False
        
        if self.find_skin(input_obj) == 0:
            return return_val
            
        bone_count = rt.skinOps.GetNumberBones(self.skinMod)
        self.allBoneNamesArray = []
        self.allBonesArray = []
        
        for i in range(1, bone_count + 1):
            bone_name = rt.skinOps.GetBoneName(self.skinMod, i, 0)
            self.allBoneNamesArray.append(bone_name)
            bone_obj = rt.getNodeByName(bone_name)
            self.allBonesArray.append(bone_obj)
            
        if len(self.allBonesArray) > 0:
            return_val = True
            
        return return_val
    
    def remove_unused_bones(self, input_obj, weight_thresh=0.0001):
        """
        스킨에서 사용되지 않는 본 제거
        
        Args:
            input_obj: 스킨 모디파이어가 있는 객체
            weight_thresh: 가중치 임계값 (기본값: 0.0001)
            
        Returns:
            True: 성공한 경우
            False: 실패한 경우
        """
        return_val = False
        
        if not self.select_skin_obj(input_obj):
            return return_val
        
        vert_count = rt.skinOps.GetNumberVertices(self.skinMod)
        bones_count = rt.skinOps.GetNumberBones(self.skinMod)
        unused_bones = set(range(1, bones_count + 1))  # 1-based 인덱스
        
        for v in range(1, vert_count + 1):
            vert_weight_count = rt.skinOps.GetVertexWeightCount(self.skinMod, v)
            
            for i in range(1, vert_weight_count + 1):
                weight = rt.skinOps.GetVertexWeight(self.skinMod, v, i)
                if weight >= weight_thresh:
                    bone_id = rt.skinOps.GetVertexWeightBoneID(self.skinMod, v, i)
                    if bone_id in unused_bones:
                        unused_bones.remove(bone_id)
        
        # 사용되지 않는 본을 역순으로 제거
        sorted_unused_bones = sorted(list(unused_bones), reverse=True)
        for bone_id in sorted_unused_bones:
            rt.skinOps.SelectBone(self.skinMod, bone_id)
            rt.skinOps.RemoveBone(self.skinMod)
        
        return_val = True
        return return_val
    
    def get_bones_from_skin(self, objs, skin_mod_index):
        """
        스킨 모디파이어의 본 목록 반환
        
        Args:
            objs: 객체 배열
            skin_mod_index: 스킨 모디파이어 인덱스
            
        Returns:
            본 배열
        """
        inf_list = []
        
        for obj in objs:
            if rt.isValidNode(obj):
                # 의존성 참조 확인 및 유효한 본만 추가
                deps = rt.refs.dependsOn(obj.modifiers[skin_mod_index])
                for n in deps:
                    if rt.isValidNode(n) and self.is_valid_bone(n):
                        if n not in inf_list:
                            inf_list.append(n)
        
        return inf_list
    
    def get_bone_index(self, input_obj, target_bone):
        """
        대상 본의 인덱스 반환
        
        Args:
            input_obj: 스킨 모디파이어가 있는 객체
            target_bone: 인덱스를 찾을 본 객체
            
        Returns:
            본 인덱스 (없으면 0)
        """
        return_val = 0
        
        if len(self.allBonesArray) > 0:
            if target_bone in self.allBonesArray:
                bone_id = self.allBonesArray.index(target_bone) + 1  # 1-based 인덱스
                return_val = bone_id
        
        return return_val
    
    def round_number(self, num, precision=3):
        """
        숫자를 지정된 정밀도로 반올림
        
        Args:
            num: 반올림할 숫자
            precision: 소수점 자릿수 (기본값: 3)
            
        Returns:
            반올림된 숫자
        """
        multiplier = 10 ** precision
        return int((num * multiplier) + 0.5) / multiplier
    
    def get_selected_skin_verts(self, input_obj):
        """
        선택된 스킨 버텍스 인덱스 배열 반환
        
        Args:
            input_obj: 스킨 모디파이어가 있는 객체
            
        Returns:
            선택된 버텍스 인덱스 배열
        """
        return_val = []
        
        if not self.select_skin_obj(input_obj):
            return return_val
        
        vert_count = rt.skinOps.GetNumberVertices(self.skinMod)
        return_val = [v for v in range(1, vert_count + 1) if rt.skinOps.IsVertexSelected(self.skinMod, v) == 1]
        
        return return_val
    
    def get_vert_weight(self, input_obj, in_vert_index):
        """
        버텍스의 가중치 정보 반환
        
        Args:
            input_obj: 스킨 모디파이어가 있는 객체
            in_vert_index: 버텍스 인덱스
            
        Returns:
            SkinVert 객체
        """
        return_val = SkinVert()
        
        if len(self.allBonesArray) == 0:
            self.get_all_bones(input_obj)
            if len(self.allBonesArray) == 0:
                return return_val
        
        bone_array = []
        bone_id_array = []
        bone_name_array = []
        weight_array = []
        bone_num = rt.skinOps.getVertexWeightCount(self.skinMod, in_vert_index)
        
        for i in range(1, bone_num + 1):
            bone_id = rt.skinOps.getVertexWeightBoneID(self.skinMod, in_vert_index, i)
            bone_name = rt.skinOps.GetBoneName(self.skinMod, bone_id, 0)
            bone_sys_id = self.allBoneNamesArray.index(bone_name) + 1 if bone_name in self.allBoneNamesArray else 0
            bone_weight = rt.skinOps.getVertexWeight(self.skinMod, in_vert_index, i)
            
            if bone_sys_id > 0:
                bone_array.append(self.allBonesArray[bone_sys_id - 1])
                bone_id_array.append(bone_id)
                bone_name_array.append(bone_name)
                weight_array.append(self.round_number(bone_weight))
        
        return_val.index = in_vert_index
        return_val.boneArray = bone_array.copy()
        return_val.boneIDArray = bone_id_array.copy()
        return_val.boneNameArray = bone_name_array.copy()
        return_val.weightArray = weight_array.copy()
        
        return return_val
    
    def get_skin_weights(self, input_obj):
        """
        모든 스킨 버텍스의 가중치 정보 반환
        
        Args:
            input_obj: 스킨 모디파이어가 있는 객체
            
        Returns:
            SkinVert 객체 배열
        """
        return_val = []
        
        if len(self.allBonesArray) > 0:
            self.skinWeightsArray = []
            num_verts = rt.skinOps.GetNumberVertices(self.skinMod)
            
            for i in range(1, num_verts + 1):
                self.skinWeightsArray.append(self.get_vert_weight(input_obj, i))
            
            return_val = self.skinWeightsArray.copy()
        
        return return_val
    
    def select_zero_weight_vertex(self, input_obj):
        """
        가중치가 0인 버텍스 선택
        
        Args:
            input_obj: 스킨 모디파이어가 있는 객체
            
        Returns:
            선택된 0 가중치 버텍스 배열
        """
        return_array = []
        
        if not self.select_skin_obj(input_obj):
            return return_array
        
        num_verts = rt.skinOps.GetNumberVertices(self.skinMod)
        
        for v in range(1, num_verts + 1):
            weights = self.get_vert_weight(input_obj, v).weightArray
            weight_val = sum(weights) if weights else 0.0
            
            if weight_val == 0.0:
                return_array.append(v)
        
        rt.skinOps.SelectVertices(self.skinMod, return_array)
        rt.redrawViews()
        
        return return_array
    
    def replace_bone(self, input_obj, ori_bone, new_bone, remove_old_bone=True):
        """
        스킨에서 본 교체
        
        Args:
            input_obj: 스킨 모디파이어가 있는 객체
            ori_bone: 원본 본
            new_bone: 새 본
            remove_old_bone: 원래 본 제거 여부 (기본값: True)
            
        Returns:
            True: 성공한 경우
            False: 실패한 경우
        """
        if self.find_skin(input_obj) == 0:
            return False
        
        rt.skinOps.addbone(self.skinMod, new_bone, 1)
        self.get_all_bones(input_obj)
        
        if len(self.allBonesArray) < 2:
            return False
        
        self.get_skin_weights(input_obj)
        prev_skin_weights_array = self.skinWeightsArray.copy()
        ori_bone_index = self.get_bone_index(input_obj, ori_bone)
        
        if ori_bone_index == 0:
            return False
            
        new_bone_index = self.get_bone_index(input_obj, new_bone)
        vert_num = rt.skinOps.GetNumberVertices(self.skinMod)
        
        # Progress dialog would be here in MaxScript
        for v in range(1, vert_num + 1):
            fined_bone_id = prev_skin_weights_array[v-1].boneIDArray.index(ori_bone_index) + 1 if ori_bone_index in prev_skin_weights_array[v-1].boneIDArray else 0
            
            if fined_bone_id > 0:
                prev_skin_weights_array[v-1].boneIDArray[fined_bone_id-1] = new_bone_index
                rt.skinOps.ReplaceVertexWeights(self.skinMod, v, prev_skin_weights_array[v-1].boneIDArray, self.skinWeightsArray[v-1].weightArray)
        
        if remove_old_bone:
            rt.skinOps.removebone(self.skinMod, ori_bone_index)
        
        return True
    
    def copy_weight_between_bones_in_skin(self, input_obj, ori_bone, new_bone, remove_old_bone=False):
        """
        스킨 내에서 본 간 가중치 복사
        
        Args:
            input_obj: 스킨 모디파이어가 있는 객체
            ori_bone: 원본 본
            new_bone: 새 본
            remove_old_bone: 원래 본 제거 여부 (기본값: False)
            
        Returns:
            True: 성공한 경우
            False: 실패한 경우
        """
        if self.find_skin(input_obj) == 0:
            return False
        
        self.get_skin_weights(input_obj)
        prev_skin_weights_array = self.skinWeightsArray.copy()
        ori_bone_index = self.get_bone_index(input_obj, ori_bone)
        
        if ori_bone_index == 0:
            return False
            
        new_bone_index = self.get_bone_index(input_obj, new_bone)
        vert_num = rt.skinOps.GetNumberVertices(self.skinMod)
        
        # Progress dialog would be here in MaxScript
        for v in range(1, vert_num + 1):
            if ori_bone_index in prev_skin_weights_array[v-1].boneIDArray:
                fined_bone_id = prev_skin_weights_array[v-1].boneIDArray.index(ori_bone_index)
                prev_skin_weights_array[v-1].boneIDArray[fined_bone_id] = new_bone_index
                rt.skinOps.ReplaceVertexWeights(self.skinMod, v, prev_skin_weights_array[v-1].boneIDArray, self.skinWeightsArray[v-1].weightArray)
        
        if remove_old_bone:
            rt.skinOps.removebone(self.skinMod, ori_bone_index)
        
        return True
    
    def replace_multi_bones(self, input_obj, ori_bone_array, new_bone_array):
        """
        여러 본을 한번에 교체
        
        Args:
            input_obj: 스킨 모디파이어가 있는 객체
            ori_bone_array: 원본 본 배열
            new_bone_array: 새 본 배열
            
        Returns:
            True: 성공한 경우
            False: 실패한 경우
        """
        if len(ori_bone_array) != len(new_bone_array):
            return False
            
        if self.find_skin(input_obj) == 0:
            return False
        
        for item in new_bone_array:
            rt.skinOps.addbone(self.skinMod, item, 1)
        
        self.get_skin_weights(input_obj)
        del_bones = set(range(1, len(self.allBonesArray) + 1))
        prev_skin_weights_array = self.skinWeightsArray.copy()
        
        # Progress dialog would be here in MaxScript
        vert_num = rt.skinOps.GetNumberVertices(self.skinMod)
        
        for i in range(len(ori_bone_array)):
            ori_bone_index = self.get_bone_index(input_obj, ori_bone_array[i])
            new_bone_index = self.get_bone_index(input_obj, new_bone_array[i])
            
            if ori_bone_index != 0:
                del_bones.discard(ori_bone_index)
                
                for v in range(1, vert_num + 1):
                    if ori_bone_index in prev_skin_weights_array[v-1].boneIDArray:
                        fined_bone_id = prev_skin_weights_array[v-1].boneIDArray.index(ori_bone_index)
                        prev_skin_weights_array[v-1].boneIDArray[fined_bone_id] = new_bone_index
                        rt.skinOps.ReplaceVertexWeights(self.skinMod, v, prev_skin_weights_array[v-1].boneIDArray, self.skinWeightsArray[v-1].weightArray)
        
        # 더 이상 사용되지 않는 본 제거
        for bone_id in sorted(list(del_bones), reverse=True):
            rt.skinOps.SelectBone(self.skinMod, bone_id)
            rt.skinOps.RemoveBone(self.skinMod)
        
        return True
    
    def replace_bones_by_base_name(self, in_obj, in_new_base_name):
        """
        기본 이름을 기준으로 본 교체
        
        Args:
            in_obj: 스킨 모디파이어가 있는 객체
            in_new_base_name: 새로운 기본 이름
            
        Returns:
            True: 성공한 경우
            False: 실패한 경우
        """
        if self.find_skin(in_obj) == 0:
            return False
            
        self.get_all_bones(in_obj)
        
        if len(self.allBonesArray) == 0:
            return False
        
        new_bone_names_array = []
        for item in self.allBoneNamesArray:
            new_bone_name = self.name.replace_base(item, in_new_base_name)
            new_bone_names_array.append(new_bone_name)
        
        new_bones_array = []
        for item in new_bone_names_array:
            temp_new_bone = rt.getNodeByName(item)
            if temp_new_bone is not None:
                new_bones_array.append(temp_new_bone)
            else:
                print(f"Cant Find {item}")
                return False
        
        return self.replace_multi_bones(in_obj, self.allBonesArray, new_bones_array)
    
    def copy_skin(self, source_obj, target_obj):
        """
        한 객체에서 다른 객체로 스킨 복사
        
        Args:
            source_obj: 소스 객체
            target_obj: 대상 객체
        """
        self.get_skin_weights(source_obj)
        
        rt.max.setModifierMode()
        rt.select(target_obj)
        
        # 스킨 모디파이어 복사
        target_obj.addModifier(rt.copy(self.skinMod))
        
        # 대상 객체의 스킨 모디파이어 찾기
        target_skin_mod = None
        for i in range(len(target_obj.modifiers)):
            if rt.classOf(target_obj.modifiers[i]) == rt.Skin:
                target_skin_mod = target_obj.modifiers[i]
                break
                
        if target_skin_mod is None:
            return
        
        # 가중치 적용
        target_obj_num_vert = rt.skinOps.GetNumberVertices(target_skin_mod)
        for v in range(1, target_obj_num_vert + 1):
            if v-1 < len(self.skinWeightsArray):
                rt.skinOps.ReplaceVertexWeights(target_skin_mod, v, self.skinWeightsArray[v-1].boneIDArray, self.skinWeightsArray[v-1].weightArray)
    
    def select_bone(self, in_obj, in_bone_obj):
        """
        스킨에서 특정 본 선택
        
        Args:
            in_obj: 스킨 모디파이어가 있는 객체
            in_bone_obj: 선택할 본 객체
            
        Returns:
            True: 성공한 경우
            False: 실패한 경우
        """
        return_val = False
        
        bone_index = self.get_bone_index(in_obj, in_bone_obj)
        if bone_index > 0:
            rt.skinOps.SelectBone(self.skinMod, bone_index)
            return_val = True
        
        return return_val
    
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
            list_of_bones = set(range(1, rt.skinOps.GetNumberBones(skin_mod) + 1))
            
            for v in range(1, rt.skinOps.GetNumberVertices(skin_mod) + 1):
                for b in range(1, rt.skinOps.GetVertexWeightCount(skin_mod, v) + 1):
                    bone_id = rt.skinOps.GetVertexWeightBoneID(skin_mod, v, b)
                    if bone_id in list_of_bones:
                        list_of_bones.remove(bone_id)
            
            list_of_bones = sorted(list(list_of_bones), reverse=True)
            for bone_id in list_of_bones:
                rt.skinOps.SelectBone(skin_mod, bone_id)
                rt.skinOps.removebone(skin_mod, bone_id)
                
            if rt.skinOps.getNumberBones(skin_mod) > 1:
                rt.skinOps.SelectBone(skin_mod, 1)
                
            print(f"Obj:{skin_mod.node.name} Removed:{len(list_of_bones)} Left:{rt.skinOps.GetNumberBones(skin_mod)}")
    
    def optimize_skin_process(self, objs=None, optim_all_skin_mod=False, b_limit=8, s_tolerance=0.01):
        """
        여러 객체의 스킨 최적화 프로세스
        
        Args:
            objs: 최적화할 객체 배열 (기본값: 현재 선택된 객체들)
            optim_all_skin_mod: 모든 스킨 모디파이어 최적화 여부 (기본값: False)
            b_limit: 본 제한 수 (기본값: 8)
            s_tolerance: 스킨 가중치 허용 오차 (기본값: 0.01)
        """
        if objs is None:
            objs = rt.selection
            
        if not objs:
            return
            
        rt.max.setModifierMode()
        
        for obj in objs:
            if self.has_skin(obj):
                mod_id = [i+1 for i in range(len(obj.modifiers)) if rt.classOf(obj.modifiers[i]) == rt.Skin]
                
                if not optim_all_skin_mod:
                    mod_id = [mod_id[0]]
                    
                for each in mod_id:
                    rt.modPanel.setCurrentObject(obj.modifiers[each-1])
                    self.optimize_skin(obj.modifiers[each-1], bone_limit=b_limit, skin_tolerance=s_tolerance)
        
        rt.select(objs)
    
    def sel_vert_from_bones(self, skin_mod, threshold=0.01):
        """
        특정 본이 영향을 주는 버텍스 선택
        
        Args:
            skin_mod: 스킨 모디파이어
            threshold: 가중치 임계값 (기본값: 0.01)
            
        Returns:
            선택된 버텍스 배열
        """
        final_verts_2_sel = []
        
        if skin_mod is not None:
            le_bone = rt.skinops.getSelectedBone(skin_mod)
            svc = rt.skinOps.GetNumberVertices(skin_mod)
            
            for o in range(1, svc + 1):
                lv = rt.skinOps.GetVertexWeightCount(skin_mod, o)
                
                for k in range(1, lv + 1):
                    if rt.skinOps.GetVertexWeightBoneID(skin_mod, o, k) == le_bone:
                        if rt.skinOps.GetVertexWeight(skin_mod, o, k) >= threshold:
                            if o not in final_verts_2_sel:
                                final_verts_2_sel.append(o)
            
            rt.skinOps.SelectVertices(skin_mod, final_verts_2_sel)
        
        return final_verts_2_sel
    
    def make_rigid_skin(self, skin_mod, vert_list):
        """
        버텍스에 대한 리지드 스킨 생성
        
        Args:
            skin_mod: 스킨 모디파이어
            vert_list: 버텍스 리스트
            
        Returns:
            [본 인덱스 배열, 가중치 배열]
        """
        weight_array = {}
        vert_count = 0
        bone_array = []
        final_weight = []
        
        for v in vert_list:
            for cur_bone in range(1, rt.skinOps.GetVertexWeightCount(skin_mod, v) + 1):
                cur_id = rt.skinOps.GetVertexWeightBoneID(skin_mod, v, cur_bone)
                if cur_id not in weight_array:
                    weight_array[cur_id] = 0
                
                cur_weight = rt.skinOps.GetVertexWeight(skin_mod, v, cur_bone)
                weight_array[cur_id] += cur_weight
                vert_count += cur_weight
        
        for i in weight_array:
            if weight_array[i] > 0:
                new_val = weight_array[i] / vert_count
                if new_val > 0.01:
                    bone_array.append(i)
                    final_weight.append(new_val)
        
        return [bone_array, final_weight]
    
    def load_skin(self, obj, file_path, load_bind_pose=False, keep_skin=False):
        """
        파일에서 스킨 가중치 로드
        
        Args:
            obj: 스킨을 로드할 객체
            file_path: 스킨 파일 경로
            load_bind_pose: 바인드 포즈 로드 여부 (기본값: False)
            keep_skin: 기존 스킨 유지 여부 (기본값: False)
            
        Returns:
            누락된 본 목록
        """
        if keep_skin is None:
            keep_skin = False
        
        rt.select(obj)
        data = []
        missing_bones = []
        
        # 파일 읽기
        with open(file_path, 'r') as file:
            for line in file:
                data.append(eval(line))
        
        if len(data) - 1 != obj.verts.count or obj.verts.count == 0:
            print("Bad number of verts")
            return missing_bones
        
        # 기존 스킨 모디파이어 제거
        for i in range(len(obj.modifiers)-1, -1, -1):
            if rt.classOf(obj.modifiers[i]) == rt.Skin:
                rt.deleteModifier(obj, i+1)
        
        rt.setCommandPanelTaskMode(rt.Name("modify"))
        new_skin = rt.Skin()
        
        before_param = 1 if keep_skin else 0
        rt.addmodifier(obj, new_skin, before=before_param)
        
        if keep_skin:
            new_skin.name = "Skin_" + rt.getfilenamefile(file_path)
        
        rt.modPanel.setCurrentObject(new_skin)
        bone_names = data[0]  # 본 이름 목록
        hierarchy = []
        
        for i in range(len(bone_names)):
            my_bone = [obj for obj in rt.objects if obj.name == bone_names[i]]
            
            if not my_bone:
                print(f"Missing bone: {bone_names[i]}")
                tmp = rt.dummy(name=bone_names[i])
                my_bone = [tmp]
                missing_bones.append(tmp)
            
            if len(my_bone) > 1 and hierarchy:
                print(f"Multiple bones are named: {my_bone[0].name} ({len(my_bone)})")
                good_bone = None
                for o in my_bone:
                    if o in hierarchy:
                        good_bone = o
                if good_bone is not None:
                    my_bone = [good_bone]
            
            # 여러 본이 있는 경우 사용자가 선택할 수 있게 함 (Python GUI 필요)
            if len(my_bone) > 1:
                rt.unhide(my_bone)
                rt.unfreeze(my_bone)
                rt.select(my_bone)
                
                # pickObject는 맥스스크립트 기능으로 파이썬에서 다르게 처리해야 함
                # 여기서는 첫 번째 본 사용
                pick_bone = my_bone[0]  
                if pick_bone is not None:
                    my_bone[0] = pick_bone
                rt.select(obj)
            
            my_bone = my_bone[0]
            if my_bone not in hierarchy:
                hierarchy.append(my_bone)
                # 계층 구조에 있는 모든 객체 추가
                for hier_obj in hierarchy:
                    for cur_child in hier_obj.children:
                        if cur_child not in hierarchy:
                            hierarchy.append(cur_child)
                    if hier_obj.parent is not None and hier_obj.parent not in hierarchy:
                        hierarchy.append(hier_obj.parent)
            
            rt.setCommandPanelTaskMode(rt.Name("modify"))
            rt.skinOps.addbone(new_skin, my_bone, 1)
            
            # 바인드 포즈 로드 옵션 처리
            if load_bind_pose:
                my_file_bp = file_path[:-4] + "bp"
                bind_poses = []
                
                if rt.doesFileExist(my_file_bp):
                    with open(my_file_bp, 'r') as bp_file:
                        for line in bp_file:
                            bind_poses.append(eval(line))
                
                if i < len(bind_poses) and bind_poses[i] is not None:
                    rt.skinUtils.SetBoneBindTM(obj, my_bone, bind_poses[i])
        
        # 버텍스 가중치 설정
        for i in range(1, obj.verts.count + 1):
            if i < len(data):
                bone_id = []
                bone_weight = []
                good_bones = set()
                all_bone_weight = [0] * len(bone_names)
                
                for b in range(len(data[i][0])):
                    if 0 <= data[i][0][b]-1 < len(all_bone_weight):
                        all_bone_weight[data[i][0][b]-1] += data[i][1][b]
                        good_bones.add(data[i][0][b])
                
                for b in good_bones:
                    bone_id.append(b)
                    bone_weight.append(all_bone_weight[b-1])
                
                if bone_id:
                    # Max 2014 sp5 hack
                    rt.skinOps.SetVertexWeights(new_skin, i, bone_id[0], 1)
                    rt.skinOps.ReplaceVertexWeights(new_skin, i, bone_id, bone_weight)
        
        return missing_bones
    
    def save_skin(self, obj, skin_mod, file_path):
        """
        스킨 가중치를 파일로 저장
        
        Args:
            obj: 스킨이 있는 객체
            skin_mod: 스킨 모디파이어
            file_path: 저장할 파일 경로
            
        Returns:
            저장된 파일 경로
        """
        rt.select(obj)
        rt.max.setModifierMode()
        rt.modPanel.setCurrentObject(obj.modifiers[rt.Name("#Skin")])
        
        if rt.classOf(obj.modifiers[rt.Name("#Skin")]) == rt.Skin and rt.skinOps.GetNumberBones(skin_mod) > 0:
            bone_list = "["
            for i in range(1, rt.skinOps.GetNumberBones(skin_mod) + 1):
                bone_name = rt.skinOps.GetBoneName(skin_mod, i, 1)
                bone_list += f"\"{bone_name}\", "
            
            bone_list = bone_list[:-2] + "]" if len(bone_list) > 1 else bone_list + "]"
            skin_data = [bone_list]
            
            # 초기화
            for i in range(rt.skinOps.GetNumberVertices(skin_mod)):
                skin_data.append(None)
            
            for v in range(1, rt.skinOps.GetNumberVertices(skin_mod) + 1):
                bone_array = []
                weight_array = []
                
                for b in range(1, rt.skinOps.GetVertexWeightCount(skin_mod, v) + 1):
                    bone_array.append(rt.skinOps.GetVertexWeightBoneID(skin_mod, v, b))
                    weight_array.append(rt.skinOps.GetVertexWeight(skin_mod, v, b))
                
                skin_data[v] = [bone_array, weight_array]
            
            with open(file_path, 'w') as file:
                for item in skin_data:
                    file.write(f"{item}\n")
            
            return file_path
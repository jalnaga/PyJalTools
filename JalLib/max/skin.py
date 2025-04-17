#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
스킨 모듈 - 3ds Max용 스킨 관련 기능 제공
원본 MAXScript의 skin.ms를 Python으로 변환하였으며, pymxs 모듈 기반으로 구현됨
"""

from pymxs import runtime as rt


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
    
    def has_skin(self, inObj=None):
        """
        객체에 스킨 모디파이어가 있는지 확인
        
        Args:
            inObj: 확인할 객체 (기본값: 현재 선택된 객체)
            
        Returns:
            True: 스킨 모디파이어가 있는 경우
            False: 없는 경우
        """
        if inObj is None:
            if len(rt.selection) > 0:
                inObj = rt.selection[0]
            else:
                return False
        
        # 객체의 모든 모디파이어를 검사하여 Skin 모디파이어가 있는지 확인
        for mod in inObj.modifiers:
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
    
    def get_skin_mod(self, inObj=None):
        """
        객체의 스킨 모디파이어 배열 반환
        
        Args:
            inObj: 모디파이어를 가져올 객체 (기본값: 현재 선택된 객체)
            
        Returns:
            스킨 모디파이어 배열
        """
        if inObj is None:
            if len(rt.selection) > 0:
                inObj = rt.selection[0]
            else:
                return []
        
        return [mod for mod in inObj.modifiers if rt.classOf(mod) == rt.Skin]
    
    def bind_skin(self, inObj, inBoneArray):
        """
        객체에 스킨 모디파이어 바인딩
        
        Args:
            inObj: 바인딩할 객체
            inBoneArray: 바인딩할 본 배열
            
        Returns:
            True: 성공한 경우
            False: 실패한 경우
        """
        if inObj is None or len(inBoneArray) < 1:
            print("Select at least 1 influence and an object.")
            return False
        
        # Switch to modify mode
        rt.execute("max modify mode")
        
        # Check if the object is valid for skinning
        if rt.superClassOf(inObj) != rt.GeometryClass:
            print(f"{inObj.name} must be 'Edit_Mesh' or 'Edit_Poly'.")
            return False
        
        # Add skin modifier
        objmod = rt.Skin()
        rt.addModifier(inObj, objmod)
        rt.select(inObj)
        
        # Add bones to skin modifier
        wgt = 1.0
        for each in inBoneArray:
            rt.skinOps.addBone(objmod, each, wgt)
        
        # Set skin modifier options
        objmod.filter_vertices = True
        objmod.filter_envelopes = False
        objmod.filter_cross_sections = True
        objmod.enableDQ = False
        objmod.bone_Limit = 8
        objmod.colorAllWeights = True
        objmod.showNoEnvelopes = True
    
    def optimize_skin(self, inSkinMod, boneLimit=8, skinTolerance=0.01):
        """
        스킨 모디파이어 최적화
        
        Args:
            inSkinMod: 스킨 모디파이어
            boneLimit: 본 제한 수 (기본값: 8)
            skinTolerance: 스킨 가중치 허용 오차 (기본값: 0.01)
        """
        # 스킨 모디파이어 설정
        inSkinMod.enableDQ = False
        inSkinMod.enableDQ = False
        inSkinMod.bone_Limit = boneLimit
        inSkinMod.clearZeroLimit = skinTolerance
        rt.skinOps.RemoveZeroWeights(inSkinMod)
        inSkinMod.clearZeroLimit = 0
        
        if rt.skinOps.getNumberBones(inSkinMod) > 1:
            listOfBones = [i for i in range(1, rt.skinOps.GetNumberBones(inSkinMod) + 1)]
            
            for v in range(1, rt.skinOps.GetNumberVertices(inSkinMod) + 1):
                for b in range(1, rt.skinOps.GetVertexWeightCount(inSkinMod, v) + 1):
                    boneID = rt.skinOps.GetVertexWeightBoneID(inSkinMod, v, b)
                    if boneID in listOfBones:
                        listOfBones.remove(boneID)
            
            for boneID in listOfBones:
                rt.skinOps.SelectBone(inSkinMod, boneID)
                rt.skinOps.removebone(inSkinMod, boneID)
                
            if rt.skinOps.getNumberBones(inSkinMod) > 1:
                rt.skinOps.SelectBone(inSkinMod, 1)
                
            print(f"Obj:{inSkinMod.node.name} Removed:{len(listOfBones)} Left:{rt.skinOps.GetNumberBones(skin_mod)}")
    
    def optimize_skin_process(self, inObjs=None, optimAllSkinMod=False, boneLimit=8, skinTolerance=0.01):
        """
        여러 객체의 스킨 최적화 프로세스
        
        Args:
            inObjs: 최적화할 객체 배열 (기본값: 현재 선택된 객체들)
            optimAllSkinMod: 모든 스킨 모디파이어 최적화 여부 (기본값: False)
            boneLimit: 본 제한 수 (기본값: 8)
            skinTolerance: 스킨 가중치 허용 오차 (기본값: 0.01)
        """
        if inObjs is None:
            inObjs = rt.selection
            
        if not inObjs:
            return
            
        rt.max.setModifierMode()
        
        for obj in inObjs:
            if self.has_skin(obj):
                mod_id = [i+1 for i in range(len(obj.modifiers)) if rt.classOf(obj.modifiers[i]) == rt.Skin]
                
                if not optimAllSkinMod:
                    mod_id = [mod_id[0]]
                    
                for each in mod_id:
                    rt.modPanel.setCurrentObject(obj.modifiers[each-1])
                    self.optimize_skin(obj.modifiers[each-1], boneLimit=boneLimit, skinTolerance=skinTolerance)
        
        rt.select(inObjs)
    
    def sel_vert_from_bones(self, inSkinMod, threshold=0.01):
        """
        특정 본이 영향을 주는 버텍스 선택
        
        Args:
            inSkinMod: 스킨 모디파이어
            threshold: 가중치 임계값 (기본값: 0.01)
            
        Returns:
            선택된 버텍스 배열
        """
        finalVerts2Sel = []
        
        if inSkinMod is not None:
            selBone = rt.skinops.getSelectedBone(inSkinMod)
            svc = rt.skinOps.GetNumberVertices(inSkinMod)
            
            for o in range(1, svc + 1):
                lv = rt.skinOps.GetVertexWeightCount(inSkinMod, o)
                
                for k in range(1, lv + 1):
                    if rt.skinOps.GetVertexWeightBoneID(inSkinMod, o, k) == selBone:
                        if rt.skinOps.GetVertexWeight(inSkinMod, o, k) >= threshold:
                            if o not in finalVerts2Sel:
                                finalVerts2Sel.append(o)
            
            rt.skinOps.SelectVertices(inSkinMod, finalVerts2Sel)
        
        return finalVerts2Sel
    
    def make_rigid_skin(self, inSkinMode, inVertList):
        """
        버텍스에 대한 리지드 스킨 생성
        
        Args:
            inSkinMode: 스킨 모디파이어
            inVertList: 버텍스 리스트
            
        Returns:
            [본 인덱스 배열, 가중치 배열]
        """
        weightArray = []
        vertCount = 0
        boneArray = []
        fianlWeight = []
        
        for v in inVertList:
            for curBone in range(1, rt.skinOps.GetVertexWeightCount(inSkinMode, v) + 1):
                curID = rt.skinOps.GetVertexWeightBoneID(inSkinMode, v, curBone)
                if curID not in weightArray:
                    weightArray[curID] = 0
                
                curWeight = rt.skinOps.GetVertexWeight(inSkinMode, v, curBone)
                weightArray[curID] += curWeight
                vertCount += curWeight
        
        for i in weightArray:
            if weightArray[i] > 0:
                newVal = weightArray[i] / vertCount
                if newVal > 0.01:
                    boneArray.append(i)
                    fianlWeight.append(newVal)
        
        return [boneArray, fianlWeight]
    
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
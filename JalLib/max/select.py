#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
선택 모듈 - 3ds Max용 객체 선택 관련 기능 제공
원본 MAXScript의 select.ms를 Python으로 변환하였으며, pymxs 모듈 기반으로 구현됨
"""

from pymxs import runtime as rt


class Select:
    """
    객체 선택 관련 기능을 제공하는 클래스.
    MAXScript의 _Select 구조체 개념을 Python으로 재구현한 클래스이며,
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
    
    def set_selectionSet_to_all(self):
        """
        모든 유형의 객체를 선택하도록 필터 설정
        """
        rt.SetSelectFilter(1)
    
    def set_selectionSet_to_bone(self):
        """
        뼈대 객체만 선택하도록 필터 설정
        """
        rt.SetSelectFilter(8)
    
    def reset_selectionSet(self):
        """
        선택 필터를 기본값으로 재설정
        """
        rt.SetSelectFilter(1)
    
    def set_selectionSet_to_helper(self):
        """
        헬퍼 객체만 선택하도록 필터 설정
        """
        rt.SetSelectFilter(6)
    
    def set_selectionSet_to_point(self):
        """
        포인트 객체만 선택하도록 필터 설정
        """
        rt.SetSelectFilter(10)
    
    def set_selectionSet_to_spline(self):
        """
        스플라인 객체만 선택하도록 필터 설정
        """
        rt.SetSelectFilter(3)
    
    def set_selectionSet_to_mesh(self):
        """
        메시 객체만 선택하도록 필터 설정
        """
        rt.SetSelectFilter(2)
    
    def filter_bip(self):
        """
        현재 선택 항목에서 Biped 객체만 필터링하여 선택
        """
        sel_array = rt.getCurrentSelection()
        if len(sel_array) > 0:
            filtered_sel = [item for item in sel_array if rt.classOf(item) == rt.Biped_Object]
            rt.clearSelection()
            rt.select(filtered_sel)
    
    def filter_bone(self):
        """
        현재 선택 항목에서 뼈대 객체만 필터링하여 선택
        """
        sel_array = rt.getCurrentSelection()
        if len(sel_array) > 0:
            filtered_sel = [item for item in sel_array if rt.classOf(item) == rt.BoneGeometry]
            rt.clearSelection()
            rt.select(filtered_sel)
    
    def filter_helper(self):
        """
        현재 선택 항목에서 헬퍼 객체(Point, IK_Chain)만 필터링하여 선택
        """
        sel_array = rt.getCurrentSelection()
        if len(sel_array) > 0:
            filtered_sel = [item for item in sel_array if rt.classOf(item) == rt.Point or rt.classOf(item) == rt.IK_Chain_Object]
            rt.clearSelection()
            rt.select(filtered_sel)
    
    def filter_expTm(self):
        """
        현재 선택 항목에서 ExposeTm 객체만 필터링하여 선택
        """
        sel_array = rt.getCurrentSelection()
        if len(sel_array) > 0:
            filtered_sel = [item for item in sel_array if rt.classOf(item) == rt.ExposeTm]
            rt.clearSelection()
            rt.select(filtered_sel)
    
    def filter_spline(self):
        """
        현재 선택 항목에서 스플라인 객체만 필터링하여 선택
        """
        sel_array = rt.getCurrentSelection()
        if len(sel_array) > 0:
            filtered_sel = [item for item in sel_array if rt.superClassOf(item) == rt.shape]
            rt.clearSelection()
            rt.select(filtered_sel)
    
    def select_children(self, in_obj, include_self=False):
        """
        객체의 모든 자식을 선택
        
        Args:
            in_obj: 부모 객체
            include_self: 자신도 포함할지 여부 (기본값: False)
            
        Returns:
            선택된 자식 객체 리스트
        """
        # MAXScript의 $'name'/*/*/*..와 같은 표현식을 Python으로 구현
        # 재귀적으로 모든 자식 객체 수집
        children = []
        
        def collect_children(obj):
            for child in obj.children:
                children.append(child)
                collect_children(child)
        
        collect_children(in_obj)
        
        if include_self:
            children.insert(0, in_obj)
        
        return children
    
    def distinguish_hierachy_objects(self, in_array):
        """
        계층이 있는 객체와 없는 객체 구분
        
        Args:
            in_array: 검사할 객체 배열
            
        Returns:
            [계층이 없는 객체 배열, 계층이 있는 객체 배열]
        """
        return_array = [[], []]  # 첫 번째는 독립 객체, 두 번째는 계층 객체
        
        for item in in_array:
            if item.parent is None and item.children.count == 0:
                return_array[0].append(item)  # 부모와 자식이 없는 경우
            else:
                return_array[1].append(item)  # 부모나 자식이 있는 경우
        
        return return_array
    
    def get_nonLinked_objects(self, in_array):
        """
        링크(계층구조)가 없는 독립 객체만 반환
        
        Args:
            in_array: 검사할 객체 배열
            
        Returns:
            독립적인 객체 배열
        """
        return self.distinguish_hierachy_objects(in_array)[0]
    
    def get_linked_objects(self, in_array):
        """
        링크(계층구조)가 있는 객체만 반환
        
        Args:
            in_array: 검사할 객체 배열
            
        Returns:
            계층 구조를 가진 객체 배열
        """
        return self.distinguish_hierachy_objects(in_array)[1]
    
    def sort_by_hierachy(self, in_array):
        """
        객체를 계층 구조에 따라 정렬
        
        Args:
            in_array: 정렬할 객체 배열
            
        Returns:
            계층 순서대로 정렬된 객체 배열
        """
        return self.bone.sort_bones_as_hierarchy(in_array)
    
    def sort_by_index(self, in_array):
        """
        객체를 이름에 포함된 인덱스 번호에 따라 정렬
        
        Args:
            in_array: 정렬할 객체 배열
            
        Returns:
            인덱스 순서대로 정렬된 객체 배열
        """
        if len(in_array) == 0:
            return []
            
        # 인덱스 정보를 포함한 구조체 구현
        class IndexSorting:
            def __init__(self, ori_index, new_index):
                self.ori_index = ori_index
                self.new_index = new_index
        
        sorted_array = []
        struct_array = []
        
        # 각 객체의 이름에서 인덱스 추출
        for i in range(len(in_array)):
            temp_index = self.name.get_index_as_digit(in_array[i].name)
            if temp_index is False:
                struct_array.append(IndexSorting(i, 0))
            else:
                struct_array.append(IndexSorting(i, temp_index))
        
        # 추출된 인덱스에 따라 정렬
        struct_array.sort(key=lambda x: x.new_index)
        
        # 정렬된 순서에 따라 원본 객체 배열 재구성
        for i in range(len(in_array)):
            sorted_array.append(in_array[struct_array[i].ori_index])
        
        return sorted_array
    
    def sort_objects(self, in_array):
        """
        객체를 적절한 방법으로 정렬 (독립 객체와 계층 객체 모두 고려)
        
        Args:
            in_array: 정렬할 객체 배열
            
        Returns:
            정렬된 객체 배열
        """
        return_array = []
        
        # 독립 객체와 계층 객체 분류
        alone_obj_array = self.get_nonLinked_objects(in_array)
        hierachy_obj_array = self.get_linked_objects(in_array)
        
        # 각각의 방식으로 정렬
        sorted_alone_obj_array = self.sort_by_index(alone_obj_array)
        sorted_hierach_obj_array = self.sort_by_hierachy(hierachy_obj_array)
        
        # 첫 인덱스 비교를 위한 초기화
        first_index_of_alone_obj = 10000
        first_index_of_hierachy_obj = 10000
        is_alone_importer = False
        
        # 독립 객체의 첫 인덱스 확인
        if len(sorted_alone_obj_array) > 0:
            index_digit = self.name.get_index_as_digit(sorted_alone_obj_array[0].name)
            if index_digit is False:
                first_index_of_alone_obj = 0
            else:
                first_index_of_alone_obj = index_digit
        
        # 계층 객체의 첫 인덱스 확인
        if len(sorted_hierach_obj_array) > 0:
            index_digit = self.name.get_index_as_digit(sorted_hierach_obj_array[0].name)
            if index_digit is False:
                first_index_of_hierachy_obj = 0
            else:
                first_index_of_hierachy_obj = index_digit
        
        # 인덱스에 따라 순서 결정
        if first_index_of_alone_obj < first_index_of_hierachy_obj:
            is_alone_importer = True
            
        # 결정된 순서에 따라 배열 합치기    
        if is_alone_importer:
            for item in sorted_alone_obj_array:
                return_array.append(item)
            for item in sorted_hierach_obj_array:
                return_array.append(item)
        else:
            for item in sorted_hierach_obj_array:
                return_array.append(item)
            for item in sorted_alone_obj_array:
                return_array.append(item)
        
        return return_array
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
namingConfig 모듈 - Naming 클래스의 설정을 관리하는 기능 제공
NamePart 객체를 기반으로 네이밍 설정을 저장하고 불러오는 기능 구현
"""

import json
import os
import copy
from typing import List, Dict, Any, Optional, Union

# NamePart 클래스 임포트
from JalLib.namePart import NamePart


class NamingConfig:
    """
    Naming 클래스의 설정을 관리하는 클래스.
    NamePart 객체 리스트를 관리하고 JSON 파일로 저장/불러오기 기능 제공.
    """
    
    def __init__(self):
        """클래스 초기화 및 기본 설정값 정의"""
        # NamePart 객체 리스트
        self.name_parts = []
        
        # 추가 설정
        self.padding_num = 2
        
        # 필수 namePart 정의 (삭제 불가능)
        self.required_parts = ["RealName"]
        
        # 설정 파일 경로 및 기본 파일명
        self.config_file_path = ""
        self.default_file_name = "namingConfig.json"
        
        # 스크립트 디렉토리 기준 기본 경로 설정
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.default_file_path = os.path.join(script_dir, self.default_file_name)
        
        # 기본 NamePart 초기화
        self._initialize_default_parts()
    
    def _initialize_default_parts(self):
        """기본 NamePart 객체들 초기화"""
        # Base 부분
        base_part = NamePart("Base", ["b", "Bip001"], {"b": 5, "Bip001": 10})
        self.name_parts.append(base_part)
        
        # Type 부분
        type_part = NamePart("Type", ["P", "Dum", "Exp", "IK", "T"], 
                             {"P": 5, "Dum": 10, "Exp": 15, "IK": 20, "T": 25})
        self.name_parts.append(type_part)
        
        # Side 부분
        side_part = NamePart("Side", ["L", "R"], {"L": 5, "R": 10})
        self.name_parts.append(side_part)
        
        # FrontBack 부분
        front_back_part = NamePart("FrontBack", ["F", "B"], {"F": 5, "B": 10})
        self.name_parts.append(front_back_part)
        
        # RealName 부분
        real_name_part = NamePart("RealName")
        self.name_parts.append(real_name_part)
        
        # Index 부분
        index_part = NamePart("Index")
        self.name_parts.append(index_part)
        
        # Nub 부분
        nub_part = NamePart("Nub", ["Nub"], {"Nub": 5})
        self.name_parts.append(nub_part)
    
    def get_part_names(self) -> List[str]:
        """
        모든 NamePart 이름 목록 반환
        
        Returns:
            NamePart 이름 목록
        """
        return [part.get_name() for part in self.name_parts]
    
    def get_part(self, name: str) -> Optional[NamePart]:
        """
        이름으로 NamePart 객체 가져오기
        
        Args:
            name: NamePart 이름
            
        Returns:
            NamePart 객체, 없으면 None
        """
        for part in self.name_parts:
            if part.get_name() == name:
                return part
        return None
    
    def add_part(self, name: str) -> bool:
        """
        새 NamePart 객체 추가
        
        Args:
            name: 추가할 NamePart 이름
            
        Returns:
            추가 성공 여부 (True/False)
        """
        if not name:
            print("오류: 유효한 NamePart 이름을 입력하세요.")
            return False
        
        # 이미 존재하는지 확인
        if self.get_part(name) is not None:
            print(f"오류: '{name}' NamePart가 이미 존재합니다.")
            return False
        
        # 새 NamePart 추가
        new_part = NamePart(name)
        self.name_parts.append(new_part)
        return True
    
    def remove_part(self, name: str) -> bool:
        """
        NamePart 객체 제거 (필수 부분은 제거 불가)
        
        Args:
            name: 제거할 NamePart 이름
            
        Returns:
            제거 성공 여부 (True/False)
        """
        # 필수 부분은 제거 불가능
        if name in self.required_parts:
            print(f"오류: 필수 NamePart '{name}'는 제거할 수 없습니다.")
            return False
        
        # 찾아서 제거
        for i, part in enumerate(self.name_parts):
            if part.get_name() == name:
                del self.name_parts[i]
                return True
        
        print(f"오류: '{name}' NamePart가 존재하지 않습니다.")
        return False
    
    def reorder_parts(self, new_order: List[str]) -> bool:
        """
        NamePart 순서 변경
        
        Args:
            new_order: 새로운 NamePart 이름 순서 배열
            
        Returns:
            변경 성공 여부 (True/False)
        """
        # 배열 길이 확인
        if len(new_order) != len(self.name_parts):
            print("오류: 새 순서의 항목 수가 기존 NamePart와 일치하지 않습니다.")
            return False
        
        # 모든 필수 부분이 포함되어 있는지 확인
        for part in self.required_parts:
            if part not in new_order:
                print(f"오류: 필수 NamePart '{part}'가 새 순서에 포함되어 있지 않습니다.")
                return False
        
        # 모든 이름이 현재 존재하는지 확인
        current_names = self.get_part_names()
        for name in new_order:
            if name not in current_names:
                print(f"오류: '{name}' NamePart가 존재하지 않습니다.")
                return False
        
        # 순서 변경을 위한 새 리스트 생성
        reordered_parts = []
        for name in new_order:
            part = self.get_part(name)
            if part:
                reordered_parts.append(part)
        
        # 새 순서로 업데이트
        self.name_parts = reordered_parts
        return True
    
    def set_padding_num(self, padding_num: int) -> bool:
        """
        인덱스 자릿수 설정
        
        Args:
            padding_num: 설정할 패딩 자릿수
            
        Returns:
            설정 성공 여부 (True/False)
        """
        if not isinstance(padding_num, int) or padding_num < 1:
            print("오류: 패딩 자릿수는 1 이상의 정수여야 합니다.")
            return False
        
        self.padding_num = padding_num
        return True
    
    def set_part_values(self, part_name: str, values: List[str]) -> bool:
        """
        특정 NamePart의 사전 정의 값 설정
        
        Args:
            part_name: NamePart 이름
            values: 설정할 사전 정의 값 리스트
            
        Returns:
            설정 성공 여부 (True/False)
        """
        part = self.get_part(part_name)
        if not part:
            print(f"오류: '{part_name}' NamePart가 존재하지 않습니다.")
            return False
        
        if part_name == "RealName":
            print("오류: RealName 부분은 사전 정의 값을 설정할 수 없습니다.")
            return False
        
        if not values:
            print(f"오류: {part_name} 부분의 사전 정의 값은 적어도 하나 이상 있어야 합니다.")
            return False
        
        part.set_predefined_values(values)
        
        # semantics 자동 설정 (5씩 증가)
        semantics = {}
        for i, value in enumerate(values, 1):
            semantics[value] = i * 5  # 첫 번째 값: 5, 두 번째 값: 10, 세 번째 값: 15, ...
        
        part.set_semantic_mapping(semantics)
        return True
    
    def add_part_value(self, part_name: str, value: str) -> bool:
        """
        특정 NamePart에 사전 정의 값 추가 (semantics 자동 설정)
        
        Args:
            part_name: NamePart 이름
            value: 추가할 사전 정의 값
            
        Returns:
            추가 성공 여부 (True/False)
        """
        part = self.get_part(part_name)
        if not part:
            print(f"오류: '{part_name}' NamePart가 존재하지 않습니다.")
            return False
        
        if part_name == "RealName":
            print("오류: RealName 부분은 사전 정의 값을 추가할 수 없습니다.")
            return False
        
        # 값 추가
        if part.add_predefined_value(value):
            # 성공적으로 추가되었을 경우 semantics 자동 설정
            # (기존 값 수) * 5 = 새 값의 semantics
            current_values = part.get_predefined_values()
            semantic_value = len(current_values) * 5  # 새로 추가된 값의 semantics
            part.add_semantic_mapping(value, semantic_value)
            return True
        
        return False
    
    def remove_part_value(self, part_name: str, value: str) -> bool:
        """
        특정 NamePart에서 사전 정의 값 제거
        
        Args:
            part_name: NamePart 이름
            value: 제거할 사전 정의 값
            
        Returns:
            제거 성공 여부 (True/False)
        """
        part = self.get_part(part_name)
        if not part:
            print(f"오류: '{part_name}' NamePart가 존재하지 않습니다.")
            return False
        
        if part_name == "RealName":
            print("오류: RealName 부분은 사전 정의 값을 제거할 수 없습니다.")
            return False
        
        # 값이 존재하는지 확인하고 제거
        if part.contains_value(value):
            # 마지막 값인지 확인
            if part.get_value_count() <= 1:
                print(f"오류: {part_name} 부분의 사전 정의 값은 적어도 하나 이상 있어야 합니다.")
                return False
            
            return part.remove_predefined_value(value)
        else:
            print(f"오류: '{value}'가 {part_name} 부분의 사전 정의 값에 존재하지 않습니다.")
            return False
    
    def set_part_semantics(self, part_name: str, semantics: Dict[str, Union[str, int, float]]) -> bool:
        """
        특정 NamePart의 의미론적 매핑 설정
        
        Args:
            part_name: NamePart 이름
            semantics: 설정할 의미론적 매핑 딕셔너리
            
        Returns:
            설정 성공 여부 (True/False)
        """
        part = self.get_part(part_name)
        if not part:
            print(f"오류: '{part_name}' NamePart가 존재하지 않습니다.")
            return False
        
        if part_name == "RealName":
            print("오류: RealName 부분은 의미론적 매핑을 설정할 수 없습니다.")
            return False
        
        part.set_semantic_mapping(semantics)
        return True
    
    def add_part_semantic(self, part_name: str, key: str, value: Union[str, int, float]) -> bool:
        """
        특정 NamePart의 의미론적 매핑에 항목 추가
        
        Args:
            part_name: NamePart 이름
            key: 매핑할 키(값 이름)
            value: 의미 또는 가중치
            
        Returns:
            추가 성공 여부 (True/False)
        """
        part = self.get_part(part_name)
        if not part:
            print(f"오류: '{part_name}' NamePart가 존재하지 않습니다.")
            return False
        
        if part_name == "RealName":
            print("오류: RealName 부분은 의미론적 매핑을 추가할 수 없습니다.")
            return False
        
        return part.add_semantic_mapping(key, value)
    
    def get_part_semantics(self, part_name: str) -> Dict[str, Union[str, int, float]]:
        """
        특정 NamePart의 의미론적 매핑 가져오기
        
        Args:
            part_name: NamePart 이름
            
        Returns:
            의미론적 매핑 딕셔너리
        """
        part = self.get_part(part_name)
        if not part:
            print(f"오류: '{part_name}' NamePart가 존재하지 않습니다.")
            return {}
        
        return part.get_semantic_mapping()
    
    def get_part_values(self, part_name: str) -> List[str]:
        """
        특정 NamePart의 사전 정의 값 목록 가져오기
        
        Args:
            part_name: NamePart 이름
            
        Returns:
            사전 정의 값 목록
        """
        part = self.get_part(part_name)
        if not part:
            print(f"오류: '{part_name}' NamePart가 존재하지 않습니다.")
            return []
        
        return part.get_predefined_values()
    
    def save(self, file_path: Optional[str] = None) -> bool:
        """
        현재 설정을 JSON 파일로 저장
        
        Args:
            file_path: 저장할 파일 경로 (기본값: self.default_file_path)
            
        Returns:
            저장 성공 여부 (True/False)
        """
        save_path = file_path or self.default_file_path
        
        try:
            # 저장할 데이터 준비
            save_data = {
                "paddingNum": self.padding_num,
                "nameParts": []
            }
            
            # 각 NamePart 객체를 딕셔너리로 변환하여 추가
            for part in self.name_parts:
                save_data["nameParts"].append(part.to_dict())
            
            # JSON 파일로 저장
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=4, ensure_ascii=False)
            
            self.config_file_path = save_path
            return True
        except Exception as e:
            print(f"설정 저장 중 오류 발생: {e}")
            return False
    
    def load(self, file_path: Optional[str] = None) -> bool:
        """
        JSON 파일에서 설정 불러오기
        
        Args:
            file_path: 불러올 파일 경로 (기본값: self.default_file_path)
            
        Returns:
            로드 성공 여부 (True/False)
        """
        load_path = file_path or self.default_file_path
        
        try:
            if os.path.exists(load_path):
                with open(load_path, 'r', encoding='utf-8') as f:
                    loaded_data = json.load(f)
                
                # 필수 키가 있는지 확인
                if "nameParts" not in loaded_data:
                    print("경고: 설정 파일에 필수 키 'nameParts'가 없습니다.")
                    return False
                
                # paddingNum 불러오기
                if "paddingNum" in loaded_data:
                    self.padding_num = loaded_data["paddingNum"]
                
                # NamePart 객체 리스트 생성
                new_parts = []
                for part_data in loaded_data["nameParts"]:
                    part = NamePart.from_dict(part_data)
                    new_parts.append(part)
                
                # 필수 NamePart가 포함되어 있는지 확인
                part_names = [part.get_name() for part in new_parts]
                for required_name in self.required_parts:
                    if required_name not in part_names:
                        print(f"경고: 필수 NamePart '{required_name}'가 설정에 포함되어 있지 않습니다.")
                        return False
                
                # 모든 확인이 통과되면 데이터 업데이트
                self.name_parts = new_parts
                self.config_file_path = load_path
                return True
            else:
                print(f"설정 파일을 찾을 수 없습니다: {load_path}")
                return False
        except Exception as e:
            print(f"설정 로드 중 오류 발생: {e}")
            return False
    
    def apply_to_naming(self, naming_instance) -> bool:
        """
        설정을 Naming 인스턴스에 적용
        
        Args:
            naming_instance: 설정을 적용할 Naming 클래스 인스턴스
            
        Returns:
            적용 성공 여부 (True/False)
        """
        try:
            # NamePart 객체 리스트 복사하여 적용
            naming_instance._nameParts = copy.deepcopy(self.name_parts)
            
            # paddingNum 설정
            naming_instance._paddingNum = self.padding_num
            
            return True
        except Exception as e:
            print(f"설정 적용 중 오류 발생: {e}")
            return False


# 메인 함수: namingConfig.json 파일 생성 예제
def main():
    """namingConfig.json 파일 생성 예제"""
    config = NamingConfig()
    
    # 설정 예시
    config.set_padding_num(3)
    
    # Base 부분 설정
    config.set_part_values("Base", ["b", "Bip001"])
    # semantics는 자동으로 설정됨: {"b": 5, "Bip001": 10}
    
    # Type 부분 설정
    config.set_part_values("Type", ["P", "Dum", "Exp", "IK", "T"])
    # semantics는 자동으로 설정됨: {"P": 5, "Dum": 10, "Exp": 15, "IK": 20, "T": 25}
    
    # Side 부분 설정
    config.set_part_values("Side", ["L", "R"])
    # semantics는 자동으로 설정됨: {"L": 5, "R": 10}
    
    # FrontBack 부분 설정
    config.set_part_values("FrontBack", ["F", "B"])
    # semantics는 자동으로 설정됨: {"F": 5, "B": 10}
    
    # Nub 부분 설정
    config.set_part_values("Nub", ["Nub"])
    # semantics는 자동으로 설정됨: {"Nub": 5}
    
    # JSON 파일 저장
    success = config.save()
    if success:
        print(f"namingConfig.json 파일이 성공적으로 생성되었습니다: {config.config_file_path}")
    else:
        print("namingConfig.json 파일 생성에 실패했습니다.")


# 스크립트가 직접 실행될 때만 메인 함수 호출
if __name__ == "__main__":
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
서비스 모듈 - max 패키지의 서비스 인스턴스 관리
3DS Max가 실행될 때 메모리에 한번만 로드되는 서비스 인스턴스들을 관리
"""

from JalLib.lib import configPaths
from .name import Name

# 기본 서비스 인스턴스 생성
name_service = Name(configPaths.get_naming_config_path())

# 순환 참조 방지를 위해 서비스들은 초기화를 미루고 함수를 통해 접근
_helper_service = None
_constraint_service = None
_align_service = None

def get_helper_service():
    """
    Helper 서비스 인스턴스를 제공하는 함수
    지연 초기화를 통해 순환 참조 문제 해결
    
    Returns:
        Helper 인스턴스
    """
    global _helper_service
    if _helper_service is None:
        from .helper import Helper
        _helper_service = Helper(name_service=name_service)
    return _helper_service

def get_constraint_service():
    """
    Constraint 서비스 인스턴스를 제공하는 함수
    지연 초기화를 통해 순환 참조 문제 해결
    
    Returns:
        Constraint 인스턴스
    """
    global _constraint_service
    if _constraint_service is None:
        from .constraint import Constraint
        _constraint_service = Constraint(name_service=name_service, helper_service=get_helper_service())
    return _constraint_service

def get_align_service():
    """
    Align 서비스 인스턴스를 제공하는 함수
    지연 초기화를 통해 순환 참조 문제 해결
    
    Returns:
        Align 인스턴스
    """
    global _align_service
    if _align_service is None:
        from .align import Align
        _align_service = Align()
    return _align_service

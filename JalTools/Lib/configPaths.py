#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
configPaths 모듈 - 설정 파일 경로를 중앙에서 관리
전체 라이브러리에서 공통으로 사용되는 설정 파일 경로를 저장
"""

import os

# 현재 스크립트 디렉토리
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 기본 설정 파일 경로들
NAMING_CONFIG_PATH = os.path.join(SCRIPT_DIR, "namingConfig.json")

# 사용자 지정 설정 파일 경로들 (필요시 업데이트)
USER_NAMING_CONFIG_PATH = None

def get_naming_config_path():
    """
    현재 사용할 네이밍 설정 파일 경로 반환
    사용자 지정 경로가 있으면 해당 경로 반환, 없으면 기본 경로 반환
    
    Returns:
        string: 네이밍 설정 파일 경로
    """
    return USER_NAMING_CONFIG_PATH if USER_NAMING_CONFIG_PATH else NAMING_CONFIG_PATH

def set_user_naming_config_path(path):
    """
    사용자 지정 네이밍 설정 파일 경로 설정
    
    Args:
        path (string): 설정할 파일 경로
    """
    global USER_NAMING_CONFIG_PATH
    USER_NAMING_CONFIG_PATH = path

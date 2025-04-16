#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Layer 클래스 테스트
3ds Max 내부에서 실행할 수 있는 테스트 스크립트
"""

import sys
import os

from pymxs import runtime as rt

# 부모 디렉토리 추가하여 JalLib 모듈 import 가능하게 설정
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
    
from JalLib.max.link import Link

# tests 디렉토리를 sys.path에 추가
tests_dir = os.path.dirname(os.path.abspath(__file__))
if tests_dir not in sys.path:
    sys.path.append(tests_dir)

from reload_modules import reload_jaltools_modules
reload_jaltools_modules()

jalLink = Link()

jalLink.unlink_children()
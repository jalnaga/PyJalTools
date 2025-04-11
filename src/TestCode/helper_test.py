#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Helper 모듈 테스트 코드
3DS Max 내에서 직접 실행하기 위한 테스트 코드
"""

import sys
import os
import importlib
from pymxs import runtime as rt

lib_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if lib_root not in sys.path:
    sys.path.insert(0, lib_root)
    
lib_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if lib_dir not in sys.path:
    sys.path.append(lib_dir)

import helper
importlib.reload(helper)

from helper import Helper


# 테스트용 빈 리스트 초기화
testSpheres = [rt.getNodeByName("Sphere001"), rt.getNodeByName("Sphere002"), rt.getNodeByName("Sphere003")]
testHelpers = [rt.getNodeByName("Point001"), rt.getNodeByName("Point002"), rt.getNodeByName("Point003")]
testBones = [rt.getNodeByName("Bone001"), rt.getNodeByName("Bone002"), rt.getNodeByName("Bone003")]

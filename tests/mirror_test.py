#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os

from pymxs import runtime as rt

# 부모 디렉토리 추가하여 JalLib 모듈 import 가능하게 설정
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
    
# For debugging - add this temporarily to see what's available
import JalLib.max.header

# Import the correct class from header module
from JalLib.max.header import Header
from JalLib.max.select import Select

# tests 디렉토리를 sys.path에 추가
tests_dir = os.path.dirname(os.path.abspath(__file__))
if tests_dir not in sys.path:
    sys.path.append(tests_dir)

from reload_modules import reload_jaltools_modules
reload_jaltools_modules()

from JalLib.max.header import Header
from JalLib.max.mirror import Mirror

# Use the correct class name
jal = Header()  # Update this to match the actual class name
jalMirror = Mirror(name_service=jal.name, bone_service=jal.bone)

selObjs = rt.getCurrentSelection()
jalMirror.mirror_geo(selObjs)

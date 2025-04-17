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
from JalLib.max.bip import Bip

# tests 디렉토리를 sys.path에 추가
tests_dir = os.path.dirname(os.path.abspath(__file__))
if tests_dir not in sys.path:
    sys.path.append(tests_dir)

from reload_modules import reload_jaltools_modules
reload_jaltools_modules()

from JalLib.max.header import Header
from JalLib.max.bip import Bip

# Use the correct class name
jal = Header()  # Update this to match the actual class name
jalBip = Bip(anim_service=jal.anim, name_service=jal.name, bone_service=jal.bone)

selNodes = rt.getCurrentSelection()
bipCom = rt.getNodeByName("Bip001")
rt.select(jalBip.get_nodes_by_skeleton_order(bipCom))

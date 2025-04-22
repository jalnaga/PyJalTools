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
from JalLib.max.twistBone import TwistBone

# tests 디렉토리를 sys.path에 추가
tests_dir = os.path.dirname(os.path.abspath(__file__))
if tests_dir not in sys.path:
    sys.path.append(tests_dir)

from reload_modules import reload_jaltools_modules
reload_jaltools_modules()

from JalLib.max.header import Header
from JalLib.max.twistBone import TwistBone

# Use the correct class name
jal = Header()  # Update this to match the actual class name
jalTwist = TwistBone(name_service=jal.name, anim_service=jal.anim, const_service=jal.constraint, bip_service=jal.bip)
bipCom = (jal.bip.get_coms())[0]

lUpperArm = (jal.bip.get_grouped_nodes(bipCom, "lArm"))[1]
lForeArm = (jal.bip.get_grouped_nodes(bipCom, "lArm"))[2]

rUpperArm = (jal.bip.get_grouped_nodes(bipCom, "rArm"))[1]
rForeArm = (jal.bip.get_grouped_nodes(bipCom, "rArm"))[2]

lThigh = (jal.bip.get_grouped_nodes(bipCom, "lLeg"))[0]
lCalf = (jal.bip.get_grouped_nodes(bipCom, "lLeg"))[1]

rThigh = (jal.bip.get_grouped_nodes(bipCom, "rLeg"))[0]
rCalf = (jal.bip.get_grouped_nodes(bipCom, "rLeg"))[1]

jalTwist.create_thigh_type(lThigh,5)
jalTwist.create_thigh_type(rThigh,5)
jalTwist.create_calf_type(lCalf,5)
jalTwist.create_calf_type(rCalf,5)

jalTwist.create_upperArm_type(lUpperArm,5)
jalTwist.create_foreArm_type(lForeArm,5)
jalTwist.create_upperArm_type(rUpperArm,5)
jalTwist.create_foreArm_type(rForeArm,5)


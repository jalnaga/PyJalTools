#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
constraint.py 모듈 테스트 코드
3DS Max 내에서 실행 가능하도록 작성됨
"""

import os
import sys
import importlib
from pymxs import runtime as rt

# JalLib 패키지를 임포트할 수 있도록 경로 설정
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if root_dir not in sys.path:
    sys.path.append(root_dir)
    
import JalLib
import JalLib.max.constraint
importlib.reload(JalLib)
importlib.reload(JalLib.max.constraint)

# JalLib 모듈 리로드
from JalLib.tests import reload_jaltools_modules
reload_jaltools_modules()

from JalLib.max.constraint import Constraint

teapot = rt.teapot()
teapot.name = "Teapot 01"
teapot.position = rt.Point3(0, 0, 10)
box = rt.box()
box.name = "Box 01"
sphere = rt.sphere()
sphere.name = "Sphere 01"
pyramid = rt.pyramid()
pyramid.name = "Pyramid 01"

teapot.parent = sphere

const = Constraint()
const.assign_rot_const_scripted(teapot, pyramid)
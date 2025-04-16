#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
헤더 모듈 - max 패키지의 인스턴스 관리
3DS Max가 실행될 때 메모리에 한번만 로드되는 패키지 인스턴스들을 관리
"""

from .name import Name
from .anim import Anim
from .align import Align

from .helper import Helper
from .constraint import Constraint
from .bone import Bone


jalName = Name()
jalAnim = Anim()
jalAlign = Align()

jalHelper = Helper(name_service=jalName)
jalConstraint = Constraint(name_service=jalName, helper_service=jalHelper)
jalBone = Bone(name_service=jalName, anim_service=jalAnim, helper_service=jalHelper, constraint_service=jalConstraint)

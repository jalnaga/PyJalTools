#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
헤더 모듈 - max 패키지의 인스턴스 관리
3DS Max가 실행될 때 메모리에 한번만 로드되는 패키지 인스턴스들을 관리
"""

import os

from .name import Name
from .anim import Anim

from .helper import Helper
from .constraint import Constraint
from .bone import Bone

from .mirror import Mirror
from .layer import Layer
from .align import Align
from .select import Select
from .link import Link

from .bip import Bip
from .skin import Skin

class Header:
    """
    JalLib.max 패키지의 헤더 모듈
    3DS Max에서 사용하는 다양한 기능을 제공하는 클래스들을 초기화하고 관리합니다.
    """
    def __init__(self):
        """
        Header 클래스 초기화
        """
        self.configDir = os.path.join(os.path.dirname(__file__), "ConfigFiles")
        self.nameConfigDir = os.path.join(self.configDir, "3DSMaxNamingConfig.json")

        self.name = Name(configPath=self.nameConfigDir)
        self.anim = Anim()
        
        self.helper = Helper(name_service=self.name)
        self.constraint = Constraint(name_service=self.name, helper_service=self.helper)
        self.bone = Bone(name_service=self.name, anim_service=self.anim, helper_service=self.helper, constraint_service=self.constraint)
        
        self.mirror = Mirror(name_service=self.name, bone_service=self.bone)
        self.layer = Layer()
        self.align = Align()
        self.sel = Select(name_service=self.name, bone_service=self.bone)
        self.link = Link()
        
        self.bip = Bip(name_service=self.name, bone_service=self.bone, anim_service=self.anim)
        self.skin = Skin()

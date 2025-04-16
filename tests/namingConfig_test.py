#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import math
import importlib
import unittest

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "JalLib", ".."))
print(f"JalLib root_dir: {root_dir}")
if root_dir not in sys.path:
    sys.path.append(root_dir)

import JalLib
importlib.reload(JalLib)

from JalLib.namePart import NamePart, NamePartType
from JalLib.namingConfig import NamingConfig

# tests 디렉토리를 sys.path에 추가
tests_dir = os.path.dirname(os.path.abspath(__file__))
if tests_dir not in sys.path:
    sys.path.append(tests_dir)

from reload_modules import reload_jaltools_modules
reload_jaltools_modules()

nameParts = [
    NamePart("Base", NamePartType.PREFIX, ["b", "Bip001"], ["Skin Bone", "Biped"]),
    NamePart("Type", NamePartType.PREFIX, ["P", "Dum", "Exp", "IK", "T"], ["Parent", "Dummy", "ExposeTM", "IK", "Target"]),
    NamePart("Side", NamePartType.PREFIX, ["L", "R"], ["Left", "Right"]),
    NamePart("FrontBack", NamePartType.PREFIX, ["F", "B"], ["Front", "Back"]),
    NamePart("RealName", NamePartType.REALNAME, [], []),
    NamePart("Index", NamePartType.INDEX, [], []),
    NamePart("Nub", NamePartType.SUFFIX, ["Nub"], ["Nub"])
]

jalNamingConfig = NamingConfig(name_parts=nameParts, required_parts=["RealName", "Index"], padding_num=2)

config_dir = os.path.join(os.path.dirname(__file__), "..", "JalLib", "max", "ConfigFiles")
MaxNamingConfigFileName = os.path.join(config_dir, "3DSMaxNamingConfig.json")
jalNamingConfig.save(file_path=MaxNamingConfigFileName)
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os

# 부모 디렉토리 추가하여 JalLib 모듈 import 가능하게 설정
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
    
import JalLib
from JalLib.reloadModules import reload_jallib_modules
reload_jallib_modules()

from JalLib.namingConfig import NamingConfig

jalNaming = NamingConfig()

configPath = os.path.normpath(r"D:\Dropbox\Programing\Python\PyJalTools\JalLib\max\ConfigFiles\3DSMaxNamingConfig.json")
jalNaming.load(file_path=configPath)

jalNaming.reorder_parts(["Base", "Type", "RealName", "Index", "Nub", "Side", "FrontBack"])

savePath = os.path.normpath(r"C:\Users\Admin\Desktop\3DSMaxNamingConfig.json")
jalNaming.save(file_path=savePath)
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

configPath = os.path.normpath(r"D:\Dropbox\Programing\Python\PyJalTools\JalLib\ConfigFiles\CharModelerNamingConfig.json")
jalNaming.load(file_path=configPath)

csvPath = os.path.normpath(r"D:\Dropbox\Programing\Python\PyJalTools\tests\Species.csv")
jalNaming.set_part_value_by_csv("Species", csvPath)
print(jalNaming.get_part("Species").get_korean_descriptions())

savePath = os.path.normpath(r"C:\Users\Admin\Desktop\CharModelerNamingConfig.json")
jalNaming.save(file_path=savePath)
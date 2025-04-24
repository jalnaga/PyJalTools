#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import csv

# 부모 디렉토리 추가하여 JalLib 모듈 import 가능하게 설정
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
    
import JalLib
from JalLib.reloadModules import reload_jallib_modules
reload_jallib_modules()

from JalLib.namingConfig import NamingConfig
from JalLib.naming import Naming
from JalLib.nameToPath import NameToPath

jalModelingNaming = Naming(configPath=os.path.normpath(r"D:\Dropbox\Programing\Python\PyJalTools\JalLib\ConfigFiles\CharModelerNamingConfig.json"))
jalNameToPath = NameToPath(configPath=os.path.normpath(r"D:\Dropbox\Programing\Python\PyJalTools\JalLib\ConfigFiles\CharModelerPathConfig.json"), sourceNaming=jalModelingNaming)

jalNameToPath.set_root_path(r"E:\DevStorage_root\DevStorage\Characters")
print(jalNameToPath.gen_path("T_Mn_KimDokja_M_LongCoat_B_Upper_01_SC"))
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

from JalLib.perforce import Perforce

jalP4 = Perforce()
jalP4.add_files([r"E:\DevStorage_root\DevStorage\Tools\qwer.txt"], inWorkSpace="DongseokKim_DevStorage")
changeList = jalP4.get_changelists(inWorkSpace="DongseokKim_DevStorage")
print(f"Change List: {changeList}")
changeListID = changeList[0]["id"]
print(f"Target CL ID: {changeListID}")
filePath = jalP4.get_changelist_files(changeListID, inWorkSpace="DongseokKim_DevStorage")
print(f"File Path: {filePath}")
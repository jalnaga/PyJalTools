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

jalP4 = Perforce(workspace="DongseokKim_DevStorage")
# Specify a changelist when deleting files
jalP4.revert_changelist("14964")
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import math
import importlib

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "JalLib", ".."))
print(f"JalLib root_dir: {root_dir}")
if root_dir not in sys.path:
    sys.path.append(root_dir)

import JalLib
import JalLib.max.bone
importlib.reload(JalLib)
importlib.reload(JalLib.max.bone)

# tests 디렉토리를 sys.path에 추가
tests_dir = os.path.dirname(os.path.abspath(__file__))
if tests_dir not in sys.path:
    sys.path.append(tests_dir)

from reload_modules import reload_jaltools_modules
reload_jaltools_modules()
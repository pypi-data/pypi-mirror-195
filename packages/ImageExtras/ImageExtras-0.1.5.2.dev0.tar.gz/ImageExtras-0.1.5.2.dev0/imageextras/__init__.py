# Native imports
from imageextras.src.utils import *



# Compiled imports
import os
import platform
import sys

system = platform.system()

if sys.version_info >= (3, 10):
    py_ver = "py310"
elif sys.version_info >= (3, 9):
    py_ver = "py39"
else:
    raise RuntimeError("Unsupported Python version")

if system == "Windows":
    os_choice = "win"
elif system == "Linux":
    os_choice = "linux"
else:
    raise OSError(f"Unsupported platform: {system}")

module_names = ["dithering"] # modules to add

for module_name in module_names:
    module_dir = os.path.join("imageextras", "compiled", py_ver, os_choice)
    sys.path.append(module_dir)
    __import__(module_name)

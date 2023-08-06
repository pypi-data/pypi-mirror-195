# Native imports
from imageextras.src.utils import *



# Compiled imports
import os
import platform
import sys

system = platform.system()

if system == "Windows":
    os_choice = "win"
elif system == "Linux":
    os_choice = "linux"
else:
    raise OSError(f"Unsupported platform: {system}")

module_names = ["dithering"] # modules to add

for module_name in module_names:
    module_dir = os.path.join("imageextras", "compiled", os_choice, module_name) # folder needs to have the same name as the module
    sys.path.append(module_dir)
    __import__(module_name)

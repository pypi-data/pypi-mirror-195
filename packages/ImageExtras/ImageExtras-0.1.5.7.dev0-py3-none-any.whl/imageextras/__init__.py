# Native imports
from imageextras.src.utils import *

"""
# Provisional workaround while I figure out why the other method doesn't work
try:
    from imageextras.compiled.py310.win import dithering
except:
    
    try:
        from imageextras.compiled.py39.win import dithering
    except:
        
        try:
            from imageextras.compiled.py310.linux import dithering
        except:    
            from imageextras.compiled.py39.linux import dithering
"""


# Compiled imports
import os
import platform
import sys
import pkg_resources

system = platform.system()

if (sys.version_info >= (3, 10)) and (sys.version_info < (3, 11)):
    py_ver = "py310"
elif (sys.version_info >= (3, 9)) and (sys.version_info < (3, 10)):
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
    package_dir = pkg_resources.resource_filename(__name__, "")
    module_dir = os.path.join(package_dir, "compiled", py_ver, os_choice)
    sys.path.append(module_dir)
    __import__(module_name)

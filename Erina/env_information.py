"""
Environment Informations for the Erina Project\n

Erina Project\n
© Anime no Sekai - 2020
"""


import os
import sys
import pkg_resources
import time


##### SYSTEM AND PROCESS INFO
try:
    _ = startTime
except:
    startTime = time.time()
cpu_count = os.cpu_count()
working_dir = os.getcwd()
pid = os.getpid()
system = os.name

##### PYTHON INFO
python_version = sys.version
python_version_info = sys.version_info
python_implementation = sys.implementation
python_apiversion = sys.api_version
python_executable_path = sys.executable
python_builtin_module_names = sys.builtin_module_names
python_path = sys.path
python_installed_modules = []
for pkg in pkg_resources.working_set:
    python_installed_modules.append(pkg)

##### ENV INFO
erina_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
erina_version = "v2.0-019 (Beta)"

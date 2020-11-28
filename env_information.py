"""
Environment Informations for the Erina Project\n

Erina Project\n
© Anime no Sekai - 2020
"""


import os
import sys
import pkg_resources
#import lifeeasy

"""
##### SYSTEM INFO
start_date = lifeeasy.today(), lifeeasy.current_time()
system = lifeeasy.system()
system_name = lifeeasy.system_name()
kernel_version = lifeeasy.version()
cpu = lifeeasy.processor()
number_of_cpu_cores = lifeeasy.number_of_cores()
number_of_cpu_physical_cores = lifeeasy.number_of_physical_cores()
cpu_max_frequency = str(lifeeasy.cpu_max_frequency()) + 'Mhz'
cpu_min_frequency = str(lifeeasy.cpu_min_frequency()) + 'Mhz'
cpu_current_frequency = str(lifeeasy.cpu_current_frequency()) + 'Mhz'
cpu_usage_per_core = lifeeasy.cpu_usage_per_core()
cpu_usage = lifeeasy.cpu_usage()
total_ram = lifeeasy.total_ram()
used_ram_percentage = str(lifeeasy.used_ram_percentage()) + '%'
total_swap = lifeeasy.total_swap_memory()
total_swap_percentage = str(lifeeasy.used_swap_memory_percentage()) + '%'
disks_info = lifeeasy.disks_info()
"""

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
erina_dir = os.path.dirname(os.path.abspath(__file__))
import re

def convert_to_int(element):
    element = str(element).split('.')[0]
    element = re.sub("[^0-9]", "", str(element))
    if element != '':
        return int(element)
    else:
        return 0


def convert_to_float(element):
    element = re.sub("[^0-9.]", "", str(element))
    if element != '':
        return float(element)
    else:
        return 0

def get_scaled_size(bytes, suffix="B"):
    """
    Credit to PythonCode for this function.\n
    > https://www.thepythoncode.com/article/get-hardware-system-information-python\n
    Scale bytes to its proper format\n
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    (> string)
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor
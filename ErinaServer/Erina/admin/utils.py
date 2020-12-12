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
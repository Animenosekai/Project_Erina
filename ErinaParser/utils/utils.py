"""
A set of utilities
"""
import re

######## UTILITY FUNCTION ########
def capitalize_string(string):
    string = str(string).replace("_", " ")
    final_string = ''
    for word in string.split(' '):
        if final_string == '':
            final_string = word.capitalize()
            continue
        else:
            final_string += ' ' + word.capitalize()
    return final_string

def create_nice_list(input_list):
    result = ''
    try:
        result = capitalize_string(str(input_list[0]))
        try:
            result = capitalize_string(str(input_list[0])) + ', ' + capitalize_string(str(input_list[1]))
            try:
                result = capitalize_string(str(input_list[0])) + ', ' + capitalize_string(str(input_list[1])) + ', ' + capitalize_string(str(input_list[2]))
            except:
                result = capitalize_string(str(input_list[0])) + ', ' + capitalize_string(str(input_list[1]))
        except:
            result = capitalize_string(str(input_list[0]))
    except:
        result = 'Unknown'
    return result

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

def convert_to_boolean(element):
    element = str(element)
    if element.lower().replace(' ', '') in ['true', '1', 'yes']:
        return True
    else:
        return False

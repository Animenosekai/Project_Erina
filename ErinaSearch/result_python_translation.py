import re
import json

def verify_if_boolean(element):
    element_to_verify = str(element)
    if element_to_verify.lower() in ['true', '1', 'yes']:
        return True
    else:
        return False

def verify_dict(verifying_dict, consider_zeroes_and_ones_as_bool=False):

    def _verify_list(verifying_list):
        _result = []
        for element in verifying_list:
            element_str = str(element)
            if consider_zeroes_and_ones_as_bool:
                if element_str.lower() == 'true' or element_str.lower() == 'false' or element_str == '0' or element_str == '1':
                    _result.append(verify_if_boolean(element_str))
                    continue
            else:
                if element_str.lower() == 'true' or element_str.lower() == 'false':
                    _result.append(verify_if_boolean(element_str))
                    continue
            if re.sub('[0123456789]', '', element_str) == '' and element_str != '':
                _result.append(int(element_str))
            elif re.sub('[0123456789.]', '', element_str) == '' and element_str != '':
                _result.append(float(element_str))
            elif isinstance(element, dict):
                _result.append(verify_dict(element))
            elif isinstance(element, list):
                _result.append(verify_list(element))
            else:
                try:
                    _result.append(json.loads(element_str))
                except:
                    _result.append(element)
        return _result

    result = {}
    for key in verifying_dict:
        element = verifying_dict[key]
        element_str = str(element)
        if consider_zeroes_and_ones_as_bool:
            if element_str.lower() == 'true' or element_str.lower() == 'false' or element_str == '0' or element_str == '1':
                result[key] = verify_if_boolean(element_str)
                continue
        else:
            if element_str.lower() == 'true' or element_str.lower() == 'false':
                result[key] = verify_if_boolean(element_str)
                continue
        if re.sub('[0123456789]', '', element_str) == '' and element_str != '':
            result[key] = int(element_str)
        elif re.sub('[0123456789.]', '', element_str) == '' and element_str != '':
            result[key] = float(element_str)
        elif isinstance(element, dict):
            result[key] = verify_dict(element)
        elif isinstance(element, list):
            result[key] = _verify_list(element)
        else:
            try:
                result[key] = json.loads(element_str)
            except:
                result[key] = element
    return result

def verify_list(verifying_list, consider_zeroes_and_ones_as_bool=False):
    result = []
    for element in verifying_list:
        element_str = str(element)
        if consider_zeroes_and_ones_as_bool:
            if element_str.lower() == 'true' or element_str.lower() == 'false' or element_str == '0' or element_str == '1':
                result.append(verify_if_boolean(element_str))
                continue
        else:
            if element_str.lower() == 'true' or element_str.lower() == 'false':
                result.append(verify_if_boolean(element_str))
                continue
        if re.sub('[0123456789]', '', element_str) == '' and element_str != '':
            result.append(int(element_str))
        elif re.sub('[0123456789.]', '', element_str) == '' and element_str != '':
            result.append(float(element_str))
        elif isinstance(element, dict):
            result.append(verify_dict(element))
        elif isinstance(element, list):
            result.append(verify_list(element))
        else:
            try:
                result.append(json.loads(element_str))
            except:
                result.append(element)
    
    return result
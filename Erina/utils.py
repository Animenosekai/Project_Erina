"""
A set of utilities for different APIs in Erina

© Anime no Sekai
"""

### Imports
import re

### Preparing the dataz
tagsName = ["a","abbr","address","area","article","aside","audio","b","base","bdi","bdo","blockquote","body","br","button","canvas","caption","cite","code","col","colgroup","data","datalist","dd","del","details","dfn","dialog","div","dl","dt","em","embed","fieldset","figcaption","figure","footer","form","h1","h2","h3","h4","h5","h6","head","header","hgroup","hr","html","i","iframe","img","input","ins","kbd","label","legend","li","link","main","map","mark","math","menu","menuitem","meta","meter","nav","noscript","object","ol","optgroup","option","output","p","param","picture","pre","progress","q","rb","rp","rt","rtc","ruby","s","samp","script","section","select","slot","small","source","span","strong","style","sub","summary","sup","svg","table","tbody","td","template","textarea","tfoot","th","thead","time","title","tr","track","u","ul","var","video","wbr"]
htmlTags = []
for tag in tagsName:
    htmlTags.append("<" + tag + ">")
    htmlTags.append("</" + tag + ">")
    htmlTags.append("<" + tag + "/>")
    htmlTags.append("<" + tag + " />")


### Utils
def convert_to_int(element):
    """
    Safely converts anything to an integer
    """
    element = re.sub("[^0-9-]", "", str(element).split('.')[0])
    if element != '':
        return int(element)
    else:
        return 0


def convert_to_float(element):
    """
    Safely converts anything to a float
    """
    element = re.sub("[^0-9.-]", "", str(element))
    if element != '':
        return float(element)
    else:
        return 0


def convert_to_boolean(element):
    """
    Safely converts an element to a boolean value
    """
    element = str(element)
    if element.lower().replace(' ', '') in ['true', '1', 'yes']:
        return True
    else:
        return False


def textFromHTML(html):
    """
    Removes all of the HTML tags from a text
    """
    result = str(html)
    for tag in htmlTags:
        result = result.replace(tag, '')
    return result


def removeSpaceBefore(string):
    """
    Removes all of the space before the first (non-space) character in a string
    """
    string = str(string)
    cuurentCharacter = string[0]
    while cuurentCharacter == " ":
        string = string[1:]
        cuurentCharacter = string[0]

    return string

def removeSpaceBeforeAndAfter(string):
    """
    Removes any space before and after a string.
    """
    new_text = string
    for index, _ in enumerate(string):
        if string[index] != ' ':
            new_text = string[index:] + ' '
            break
    try:
        if new_text[-1] == ' ':
            for index, _ in enumerate(new_text):
                if new_text[-int(index + 1)] != ' ':
                    new_text = new_text[:-int(index)]
                    break
    except:
        pass
    return new_text

def capitalize_string(string):
    """
    Capitalizes a string
    """
    string = str(string).replace("_", " ")
    return " ".join([word.capitalize() for word in string.split()])

def create_nice_list(input_list):
    """
    Creates a nice string from a list
    """
    if isinstance(input_list, (list, tuple)):
        if len(input_list) == 0:
            return "Unknown"
        elif len(input_list) == 1:
            return capitalize_string(input_list[0])
        elif len(input_list) == 2:
            return capitalize_string(input_list[0]) + ", " + capitalize_string(input_list[1])
        else:
            return capitalize_string(input_list[0]) + ", " + capitalize_string(input_list[1] + ", " + capitalize_string(input_list[2]))
    else:
        return str(input_list)


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
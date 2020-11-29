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
    """
    Creates a list a nice string
    """
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

tagsName = ["a","abbr","address","area","article","aside","audio","b","base","bdi","bdo","blockquote","body","br","button","canvas","caption","cite","code","col","colgroup","data","datalist","dd","del","details","dfn","dialog","div","dl","dt","em","embed","fieldset","figcaption","figure","footer","form","h1","h2","h3","h4","h5","h6","head","header","hgroup","hr","html","i","iframe","img","input","ins","kbd","label","legend","li","link","main","map","mark","math","menu","menuitem","meta","meter","nav","noscript","object","ol","optgroup","option","output","p","param","picture","pre","progress","q","rb","rp","rt","rtc","ruby","s","samp","script","section","select","slot","small","source","span","strong","style","sub","summary","sup","svg","table","tbody","td","template","textarea","tfoot","th","thead","time","title","tr","track","u","ul","var","video","wbr"]
htmlTags = []
for tag in tagsName:
    htmlTags.append("<" + tag + ">")
    htmlTags.append("</" + tag + ">")
    htmlTags.append("<" + tag + "/>")
    htmlTags.append("<" + tag + " />")

def textFromHTML(html):
    result = html
    for tag in htmlTags:
        result = result.replace(tag, '')
    return result

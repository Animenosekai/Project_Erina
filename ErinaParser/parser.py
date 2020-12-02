from safeIO import TextFile

from Erina.env_information import erina_dir
from ErinaParser.utils import anilist_parser
from ErinaParser.utils import erina_parser
from ErinaParser.utils import erinadb_parser
from ErinaParser.utils import iqdb_parser
from ErinaParser.utils import saucenao_parser
from ErinaParser.utils import tracemoe_parser
from ErinaParser.utils.Errors import ParserError

def _get_type(data):
    """
    Returns the type of .erina file
    """
    data = str(data)
    if data[:27] == "   --- ANILIST CACHE ---   ":
        return "anilist_cache"
    elif data[:25] == "   --- ERINA CACHE ---   ":
        return "erina_cache"
    elif data[:28] == "   --- ERINA DATABASE ---   ":
        return "erina_database"
    elif data[:24] == "   --- IQDB CACHE ---   ":
        return "iqdb_cache"
    elif data[:28] == "   --- SAUCENAO CACHE ---   ":
        return "saucenao_cache"
    elif data[:28] == "   --- TRACEMOE CACHE ---   ":
        return "tracemoe_cache"
    else:
        return ParserError("IMPOSSIBLE_TYPE_DETECTION", "We couldn't define the type of the given file")        

def _return_content(type, data):
    """
    Returns the content of the file
    """
    if type == "anilist_cache":
        return anilist_parser.AnilistCache(data)
    elif type == "erina_cache":
        return erina_parser.ErinaCache(data)
    elif type == "erina_database":
        return erinadb_parser.ErinaData(data)
    elif type == "iqdb_cache":
        return iqdb_parser(data)
    elif type == "saucenao_cache":
        return saucenao_parser.SauceNAOCache(data)
    elif type == "tracemoe_cache":
        return tracemoe_parser.TraceMOECache(data)

class ErinaFile():
    """
    An .erina object (Erina File Parser)
    """
    def __init__(self, type=None, filename=None, data=None) -> None:
        self.type = None
        self.data = None
        self.content = None
        if type is not None and filename is not None:
            self.type = str(type)
            if self.type == "anilist_cache":
                self.data = TextFile(erina_dir + "/ErinaCaches/AniList_Cache/").read()
                
            elif self.type == "erina_cache":
                self.data = TextFile(erina_dir + "/ErinaCaches/Erina_Cache/").read()
            
            elif self.type == "erina_database":
                self.data = TextFile(erina_dir + "/ErinaCaches/ErinaDatabase/").read()
            
            elif self.type == "iqdb_cache":
                self.data = TextFile(erina_dir + "/ErinaCaches/IQDB_Cache/").read()
            
            elif self.type == "saucenao_cache":
                self.data = TextFile(erina_dir + "/ErinaCaches/SauceNAO_Cache/").read()
            
            elif self.type == "tracemoe_cache":
                self.data = TextFile(erina_dir + "/ErinaCaches/TraceMOE_Cache/").read()
            
        elif data is not None:
            self.type = _get_type(data)
            self.data = str(data)
        
        self.content = _return_content(self.type, self.data)
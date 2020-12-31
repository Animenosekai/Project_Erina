"""
ErinaConfig Python Parser

© Anime no Sekai
Erina Project — 2020
"""
import os
from Erina._config.files import configFile
storedData = {'Erina': {'flags': ['what is this anime', "what's this anime", 'anime sauce', 'anime source', 'what anime this is', 'what anime is this', 'called this anime', 'name of this anime', "what's that anime", 'what anime is it', 'name of anime', 'sauce to that anime'], 'consoleLog': True, 'fileLog': True, 'stats': True, 'logsTimeout': 604800}, 'Twitter': {'run': False, 'ignoredUsers': [], 'flags': [], 'ignoreRT': True, 'imagePreview': False, 'checkMentions': False, 'checkDM': False, 'keys': {'consumerKey': None, 'consumerSecret': None, 'accessTokenKey': None, 'accessTokenSecret': None}, 'stream': {'languages': ['en'], 'flags': []}, 'monitoring': {'accounts': [], 'checkReplies': False}}, 'Discord': {'run': False, 'flags': [], 'keys': {'token': None}}, 'Line': {'run': False, 'flags': [], 'keys': {'channelAccessToken': None, 'channelSecret': None}, 'imagesTimeout': 3600}, 'Caches': {'encoding': 'utf-8', 'keys': {'tracemoe': None, 'saucenao': None}}, 'Database': {}, 'Hash': {'algorithm': 'Average Hash'}, 'Parser': {}, 'Search': {'thresholds': {'erinaSimilarity': 100, 'tracemoeSimilarity': 90, 'saucenaoSimilarity': 90, 'iqdbSimilarity': 90}}, 'Server': {'host': '127.0.0.1', 'port': 5000, 'publicAPI': True}}
tempData = configFile.read()
for element in tempData:
    storedData[element] = tempData[element]

import re
from Erina.utils import convert_to_float, convert_to_int

def environ(erina_environ):
    """
    Returns an env variable if it has the correct erina environ format
    """
    if str(erina_environ)[:2] == "{{" and str(erina_environ)[-2:] == "}}":
        environResult = os.environ.get(str(erina_environ)[2:-2], None)
        if environResult is None:
            return erina_environ
        elif re.sub("[0-9-]", "", str(environResult)) == "":
            return convert_to_int(environResult)
        elif re.sub("[0-9.-]", "", str(environResult)) == "":
            return convert_to_float(environResult)
        else:
            return environResult
    else:
        return erina_environ

class ErinaConfig():
    """
    Erina General Configuration
    """
    def __init__(self) -> None:
        self.as_dict = storedData["Erina"]
        self.flags = environ(self.as_dict["flags"])
        self.console_log = environ(self.as_dict["consoleLog"])
        self.file_log = environ(self.as_dict["fileLog"])
        self.stats = environ(self.as_dict["stats"])
        self.logs_timeout = environ(self.as_dict["logsTimeout"])

    def update(self, path, value):
        """
        Updates Erina Configuration
        """
        if path[0] == "flags":
            self.flags = environ(value)
            self.as_dict["flags"] = value
        elif path[0] == "consoleLog":
            self.console_log = environ(value)
            self.as_dict["consoleLog"] = value
        elif path[0] == "fileLog":
            self.file_log = environ(value)
            self.as_dict["fileLog"] = value
        elif path[0] == "stats":
            self.stats = environ(value)
            self.as_dict["stats"] = value
        elif path[0] == "logsTimeout":
            self.logs_timeout = environ(value)
            self.as_dict["logsTimeout"] = value
        

class TwitterConfig():
    class MonitorMode():
        def __init__(self) -> None:
            self.as_dict = storedData["Twitter"]["monitoring"]
            self.accounts = environ(self.as_dict["accounts"])
            if len(self.accounts) > 0:
                self.enabled = True
            else:
                self.enabled = False
            self.check_replies = environ(self.as_dict["checkReplies"])

        def update(self, path, value):
            if path[0] == "accounts":
                self.accounts = environ(value)
                self.as_dict["accounts"] = value
                if len(self.accounts) > 0:
                    self.enabled = True
                else:
                    self.enabled = False
            elif path[0] == "checkReplies":
                self.check_replies = environ(value)
                self.as_dict["checkReplies"] = value
            
    class StreamConfig():
        def __init__(self) -> None:
            self.as_dict = storedData["Twitter"]["stream"]
            self.languages = environ(self.as_dict["languages"])
            self.flags = environ(self.as_dict["flags"])

        def update(self, path, value):
            if path[0] == "languages":
                self.languages = environ(value)
                self.as_dict["languages"] = value
            elif path[0] == "flags":
                self.flags = environ(value)
                self.as_dict["flags"] = value


    class Keys():
        def __init__(self) -> None:
            self.as_dict = storedData["Twitter"]["keys"]
            self.consumer_key = environ(self.as_dict["consumerKey"])
            self.consumer_secret = environ(self.as_dict["consumerSecret"])
            self.access_token_key = environ(self.as_dict["accessTokenKey"])
            self.access_token_secret = environ(self.as_dict["accessTokenSecret"])

        def update(self, path, value):
            if path[0] == "consumerKey":
                self.consumer_key = environ(value)
                self.as_dict["consumerKey"] = value
            elif path[0] == "consumerSecret":
                self.consumer_secret = environ(value)
                self.as_dict["consumerSecret"] = value
            elif path[0] == "accessTokenKey":
                self.access_token_key = environ(value)
                self.as_dict["accessTokenKey"] = value
            elif path[0] == "accessTokenSecret":
                self.access_token_secret = environ(value)
                self.as_dict["accessTokenSecret"] = value

    def __init__(self) -> None:
        self.as_dict = storedData["Twitter"]
        self.run = environ(self.as_dict["run"])
        self.ignored_users = environ(self.as_dict["ignoredUsers"])
        self.flags = environ(self.as_dict["flags"])
        self.ignore_rt = environ(self.as_dict["ignoreRT"])
        self.image_preview = environ(self.as_dict["imagePreview"])
        self.check_mentions = environ(self.as_dict["checkMentions"])
        self.check_dm = environ(self.as_dict["checkDM"])
        self.keys = self.Keys()
        self.stream = self.StreamConfig()
        self.monitoring = self.MonitorMode()
    
    def update(self, path, value):
        """
        Updates Erina Configuration
        """
        if path[0] == "run":
            self.run = environ(value)
            self.as_dict["run"] = value
        elif path[0] == "ignoredUsers":
            self.ignored_users = environ(value)
            self.as_dict["ignoredUsers"] = value
        elif path[0] == "flags":
            self.flags = environ(value)
            self.as_dict["flags"] = value
        elif path[0] == "ignoreRT":
            self.ignore_rt = environ(value)
            self.as_dict["ignoreRT"] = value
        elif path[0] == "imagePreview":
            self.image_preview = environ(value)
            self.as_dict["imagePreview"] = value
        elif path[0] == "checkMentions":
            self.check_mentions = environ(value)
            self.as_dict["checkMentions"] = value
        elif path[0] == "checkDM":
            self.check_dm = environ(value)
            self.as_dict["checkDM"] = value
        elif path[0] == "keys":
            self.keys.update(path[1:], value)
            self.as_dict["keys"] = self.keys.as_dict
        elif path[0] == "stream":
            self.stream.update(path[1:], value)
            self.as_dict["stream"] = self.stream.as_dict
        elif path[0] == "monitoring":
            self.monitoring.update(path[1:], value)
            self.as_dict["monitoring"] = self.monitoring.as_dict
        

class DiscordConfig():
    class Keys():
        def __init__(self) -> None:
            self.as_dict = storedData["Discord"]["keys"]
            self.token = environ(self.as_dict["token"])

        def update(self, path, value):
            if path[0] == "token":
                self.token = environ(value)
                self.as_dict["token"] = value
            
    def __init__(self) -> None:
        self.as_dict = storedData["Discord"]
        self.run = environ(self.as_dict["run"])
        self.flags = environ(self.as_dict["flags"])
        self.keys = self.Keys()

    def update(self, path, value):
        """
        Updates Erina Configuration
        """
        if path[0] == "run":
            self.run = environ(value)
            self.as_dict["run"] = value
        elif path[0] == "flags":
            self.flags = environ(value)
            self.as_dict["flags"] = value
        elif path[0] == "keys":
            self.keys.update(path[1:], value)
            self.as_dict["keys"] = self.keys.as_dict
        
class LineConfig():
    class Keys():
        def __init__(self) -> None:
            self.as_dict = storedData["Line"]["keys"]
            self.channel_access_token = environ(self.as_dict["channelAccessToken"])
            self.channel_secret = environ(self.as_dict["channelSecret"])

        def update(self, path, value):
            if path[0] == "channelAccessToken":
                self.channel_access_token = environ(value)
                self.as_dict["channelAccessToken"] = value
            elif path[0] == "channelSecret":
                self.channel_secret = environ(value)
                self.as_dict["channelSecret"] = value
            

    def __init__(self) -> None:
        self.as_dict = storedData["Line"]
        self.run = environ(self.as_dict["run"])
        self.flags = environ(self.as_dict["flags"])
        self.images_timeout = environ(self.as_dict["imagesTimeout"])
        self.keys = self.Keys()

    def update(self, path, value):
        """
        Updates Erina Configuration
        """
        if path[0] == "run":
            self.run = environ(value)
            self.as_dict["run"] = value
        elif path[0] == "imagesTimeout":
            self.images_timeout = environ(value)
            self.as_dict["imagesTimeout"] = value
        elif path[0] == "flags":
            self.flags = environ(value)
            self.as_dict["flags"] = value
        elif path[0] == "keys":
            self.keys.update(path[1:], value)
            self.as_dict["keys"] = self.keys.as_dict


class CachesConfig():
    class Keys():
        def __init__(self) -> None:
            self.as_dict = storedData["Caches"]["keys"]
            self.saucenao = environ(self.as_dict["saucenao"])
            self.tracemoe = environ(self.as_dict["tracemoe"])

        def update(self, path, value):
            if path[0] == "saucenao":
                self.saucenao = environ(value)
                self.as_dict["saucenao"] = value
            elif path[0] == "tracemoe":
                self.tracemoe = environ(value)
                self.as_dict["tracemoe"] = value

    def __init__(self) -> None:
        self.as_dict = storedData["Caches"]
        self.encoding = environ(self.as_dict["encoding"])
        self.keys = self.Keys()


    def update(self, path, value):
        """
        Updates Erina Configuration
        """
        if path[0] == "encoding":
            self.encoding = environ(value)
            self.as_dict["encoding"] = value
        elif path[0] == "keys":
            self.keys.update(path[1:], value)
            self.as_dict["keys"] = self.keys.as_dict

class DatabaseConfig():
    def __init__(self) -> None:
        self.as_dict = storedData["Database"]

    def update(self, path, value):
        pass

class HashConfig():
    def __init__(self) -> None:
        self.as_dict = storedData["Hash"]
        self.algorithm = environ(self.as_dict["algorithm"])

    def update(self, path, value):
        """
        Updates Erina Configuration
        """
        if path[0] == "algorithm":
            self.algorithm = environ(value)
            self.as_dict["algorithm"] = value

class ParserConfig():
    def __init__(self) -> None:
        self.as_dict = storedData["Parser"]
    
    def update(self, path, value):
        pass

class SearchConfig():
    class Thresholds():
        def __init__(self) -> None:
            self.as_dict = storedData["Search"]["thresholds"]
            self.erina_similarity = environ(self.as_dict["erinaSimilarity"])
            self.tracemoe_similarity = environ(self.as_dict["tracemoeSimilarity"])
            self.saucenao_similarity = environ(self.as_dict["saucenaoSimilarity"])
            self.iqdb_similarity = environ(self.as_dict["iqdbSimilarity"])


    def __init__(self) -> None:
        self.as_dict = storedData["Search"]
        self.thresholds = self.Thresholds()

    def update(self, path, value):
        """
        Updates Erina Configuration
        """
        if path[0] == "thresholds":
            self.thresholds.update(path[1:], value)
            self.as_dict["thresholds"] = self.thresholds.as_dict

class ServerConfig():
    def __init__(self) -> None:
        self.as_dict = storedData["Server"]
        self.host = environ(self.as_dict["host"])
        self.port = environ(self.as_dict["port"])
        self.public_api = environ(self.as_dict["publicAPI"])

    def update(self, path, value):
        """
        Updates Erina Configuration
        """
        if path[0] == "host":
            self.host = environ(value)
            self.as_dict["host"] = value
        elif path[0] == "port":
            self.port = environ(value)
            self.as_dict["port"] = value
        elif path[0] == "publicAPI":
            self.public_api = environ(value)
            self.as_dict["publicAPI"] = value
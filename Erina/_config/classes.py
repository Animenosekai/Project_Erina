"""
ErinaConfig Python Parser

© Anime no Sekai
Erina Project — 2020
"""
from Erina._config.files import configFile
storedData = {'Erina': {'flags': ['what is this anime', "what's this anime", 'anime sauce', 'anime source', 'what anime this is', 'what anime is this', 'called this anime', 'name of this anime', "what's that anime", 'what anime is it', 'name of anime', 'sauce to that anime'], 'consoleLog': True, 'fileLog': True, 'stats': True}, 'Twitter': {'run': True, 'ignoredUsers': [], 'flags': [], 'ignoreRT': True, 'keys': {'consumerKey': None, 'consumerSecret': None, 'accessTokenKey': None, 'accessTokenSecret': None}, 'stream': {'languages': [], 'flags': []}, 'monitoring': {'accounts': [], 'checkReplies': False}}, 'Discord': {'run': True, 'flags': [], 'keys': {'token': None}}, 'Line': {'run': True, 'flags': [], 'keys': {'channelAccessToken': None, 'channelSecret': None}, 'imagesTimeout': 3600}, 'Caches': {'encoding': 'utf-8', 'keys': {'tracemoe': None, 'saucenao': None}}, 'Database': {}, 'Hash': {'algorithm': 'Average Hash'}, 'Parser': {}, 'Search': {'thresholds': {'erinaSimilarity': 100, 'tracemoeSimilarity': 90, 'saucenaoSimilarity': 90, 'iqdbSimilarity': 90}}, 'Server': {'host': '127.0.0.1', 'port': 5000, 'disableConsoleMessages': True}}
tempData = configFile.read()
for element in tempData:
    storedData[element] = tempData[element]

class ErinaConfig():
    """
    Erina General Configuration
    """
    def __init__(self) -> None:
        self.as_dict = storedData["Erina"]
        self.flags = self.as_dict["flags"]
        self.console_log = self.as_dict["consoleLog"]
        self.file_log = self.as_dict["fileLog"]
        self.stats = self.as_dict["stats"]

    def update(self, path, value):
        """
        Updates Erina Configuration
        """
        if path[0] == "flags":
            self.flags = value
            self.as_dict["flags"] = value
        elif path[0] == "consoleLog":
            self.console_log = value
            self.as_dict["consoleLog"] = value
        elif path[0] == "fileLog":
            self.file_log = value
            self.as_dict["fileLog"] = value
        elif path[0] == "stats":
            self.console_log = value
            self.as_dict["stats"] = value
        

class TwitterConfig():
    class MonitorMode():
        def __init__(self) -> None:
            self.as_dict = storedData["Twitter"]["monitoring"]
            self.accounts = self.as_dict["accounts"]
            if len(self.accounts) > 0:
                self.enabled = True
            else:
                self.enabled = False
            self.check_replies = self.as_dict["checkReplies"]

        def update(self, path, value):
            if path[0] == "accounts":
                self.accounts = value
                self.as_dict["accounts"] = value
                if len(self.accounts) > 0:
                    self.enabled = True
                else:
                    self.enabled = False
            elif path[0] == "checkReplies":
                self.check_replies = value
                self.as_dict["checkReplies"] = value
            
    class StreamConfig():
        def __init__(self) -> None:
            self.as_dict = storedData["Twitter"]["stream"]
            self.languages = self.as_dict["languages"]
            self.flags = self.as_dict["flags"]

        def update(self, path, value):
            if path[0] == "languages":
                self.languages = value
                self.as_dict["languages"] = value
            elif path[0] == "flags":
                self.flags = value
                self.as_dict["flags"] = value


    class Keys():
        def __init__(self) -> None:
            self.as_dict = storedData["Twitter"]["keys"]
            self.consumer_key = self.as_dict["consumerKey"]
            self.consumer_secret = self.as_dict["consumerSecret"]
            self.access_token_key = self.as_dict["accessTokenKey"]
            self.access_token_secret = self.as_dict["accessTokenSecret"]

        def update(self, path, value):
            if path[0] == "consumerKey":
                self.consumer_key = value
                self.as_dict["consumerKey"] = value
            elif path[0] == "consumerSecret":
                self.consumer_secret = value
                self.as_dict["consumerSecret"] = value
            elif path[0] == "accessTokenKey":
                self.access_token_key = value
                self.as_dict["accessTokenKey"] = value
            elif path[0] == "accessTokenSecret":
                self.access_token_secret = value
                self.as_dict["accessTokenSecret"] = value

    def __init__(self) -> None:
        self.as_dict = storedData["Twitter"]
        self.run = self.as_dict["run"]
        self.ignored_users = self.as_dict["ignoredUsers"]
        self.flags = self.as_dict["flags"]
        self.ignore_rt = self.as_dict["ignoreRT"]
        self.keys = self.Keys()
        self.stream = self.StreamConfig()
        self.monitoring = self.MonitorMode()
    
    def update(self, path, value):
        """
        Updates Erina Configuration
        """
        if path[0] == "run":
            self.run = value
            self.as_dict["run"] = value
        elif path[0] == "ignoredUsers":
            self.ignored_users = value
            self.as_dict["ignoredUsers"] = value
        elif path[0] == "flags":
            self.flags = value
            self.as_dict["flags"] = value
        elif path[0] == "ignoreRT":
            self.ignore_rt = value
            self.as_dict["ignoreRT"] = value
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
            self.token = self.as_dict["token"]

        def update(self, path, value):
            if path[0] == "token":
                self.token = value
                self.as_dict["token"] = value
            
    def __init__(self) -> None:
        self.as_dict = storedData["Discord"]
        self.run = self.as_dict["run"]
        self.flags = self.as_dict["flags"]
        self.keys = self.Keys()

    def update(self, path, value):
        """
        Updates Erina Configuration
        """
        if path[0] == "run":
            self.run = value
            self.as_dict["run"] = value
        elif path[0] == "flags":
            self.flags = value
            self.as_dict["flags"] = value
        elif path[0] == "keys":
            self.keys.update(path[1:], value)
            self.as_dict["keys"] = self.keys.as_dict
        
class LineConfig():
    class Keys():
        def __init__(self) -> None:
            self.as_dict = storedData["Line"]["keys"]
            self.channel_access_token = self.as_dict["channelAccessToken"]
            self.channel_secret = self.as_dict["channelSecret"]

        def update(self, path, value):
            if path[0] == "channelAccessToken":
                self.channel_access_token = value
                self.as_dict["channelAccessToken"] = value
            elif path[0] == "channelSecret":
                self.channel_secret = value
                self.as_dict["channelSecret"] = value
            

    def __init__(self) -> None:
        self.as_dict = storedData["Line"]
        self.run = self.as_dict["run"]
        self.flags = self.as_dict["flags"]
        self.images_timeout = self.as_dict["imagesTimeout"]
        self.keys = self.Keys()

    def update(self, path, value):
        """
        Updates Erina Configuration
        """
        if path[0] == "run":
            self.run = value
            self.as_dict["run"] = value
        elif path[0] == "imagesTimeout":
            self.images_timeout = value
            self.as_dict["imagesTimeout"] = value
        elif path[0] == "flags":
            self.flags = value
            self.as_dict["flags"] = value
        elif path[0] == "keys":
            self.keys.update(path[1:], value)
            self.as_dict["keys"] = self.keys.as_dict


class CachesConfig():
    class Keys():
        def __init__(self) -> None:
            self.as_dict = storedData["Caches"]["keys"]
            self.saucenao = self.as_dict["saucenao"]
            self.tracemoe = self.as_dict["tracemoe"]

        def update(self, path, value):
            if path[0] == "saucenao":
                self.saucenao = value
                self.as_dict["saucenao"] = value
            elif path[0] == "tracemoe":
                self.tracemoe = value
                self.as_dict["tracemoe"] = value

    def __init__(self) -> None:
        self.as_dict = storedData["Caches"]
        self.encoding = self.as_dict["encoding"]
        self.keys = self.Keys()


    def update(self, path, value):
        """
        Updates Erina Configuration
        """
        if path[0] == "encoding":
            self.encoding = value
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
        self.algorithm = self.as_dict["algorithm"]

    def update(self, path, value):
        """
        Updates Erina Configuration
        """
        if path[0] == "algorithm":
            self.algorithm = value
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
            self.erina_similarity = self.as_dict["erinaSimilarity"]
            self.tracemoe_similarity = self.as_dict["tracemoeSimilarity"]
            self.saucenao_similarity = self.as_dict["saucenaoSimilarity"]
            self.iqdb_similarity = self.as_dict["iqdbSimilarity"]


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
        self.host = self.as_dict["host"]
        self.port = self.as_dict["port"]
        self.disable_console_messages = self.as_dict["disableConsoleMessages"]

    def update(self, path, value):
        """
        Updates Erina Configuration
        """
        if path[0] == "host":
            self.host = value
            self.as_dict["host"] = value
        elif path[0] == "port":
            self.port = value
            self.as_dict["port"] = value
        elif path[0] == "disableConsoleMessages":
            self.disable_console_messages = value
            self.as_dict["disableConsoleMessages"] = value
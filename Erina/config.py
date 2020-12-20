"""
Erina Project Configuration File

Erina Project
© Anime no Sekai - 2020
"""
from Erina._config import classes
from Erina._config.files import configFile, defaultFile

Erina = classes.ErinaConfig()
Twitter = classes.TwitterConfig()
Discord = classes.DiscordConfig()
Line = classes.LineConfig()
Caches = classes.CachesConfig()
Database = classes.DatabaseConfig()
Hash = classes.HashConfig()
Parser = classes.ParserConfig()
Search = classes.SearchConfig()
Server = classes.ServerConfig()

def export():
    """
    Exports the current configuration
    """
    exportResult = {}
    exportResult["Erina"] = Erina.as_dict
    exportResult["Twitter"] = Twitter.as_dict
    exportResult["Discord"] = Discord.as_dict
    exportResult["Line"] = Line.as_dict
    exportResult["Caches"] = Caches.as_dict
    exportResult["Database"] = Database.as_dict
    exportResult["Hash"] = Hash.as_dict
    exportResult["Parser"] = Parser.as_dict
    exportResult["Search"] = Search.as_dict
    exportResult["Server"] = Server.as_dict
    return exportResult

def update(path, value):
    """
    Updates the configuration
    """
    path = str(path).split("/")
    category = path[0]
    if category == "Erina":
        Erina.update(path[1:], value)
    elif category == "Twitter":
        Twitter.update(path[1:], value)
    elif category == "Discord":
        Discord.update(path[1:], value)
    elif category == "Line":
        Line.update(path[1:], value)
    elif category == "Caches":
        Caches.update(path[1:], value)
    elif category == "Database":
        Database.update(path[1:], value)
    elif category == "Hash":
        Hash.update(path[1:], value)
    elif category == "Parser":
        Parser.update(path[1:], value)
    elif category == "Search":
        Search.update(path[1:], value)
    elif category == "Server":
        Server.update(path[1:], value)


    configFile.write(export())

def default():
    """
    Backs up the configuration to the default values
    """
    global Erina
    global Twitter
    global Discord
    global Line
    global Caches
    global Database
    global Hash
    global Parser
    global Search
    global Server

    defaultData = defaultFile.read()
    configFile.write(defaultData)
    
    classes.storedData = {'Erina': {'flags': ['what is this anime', "what's this anime", 'anime sauce', 'anime source', 'what anime this is', 'what anime is this', 'called this anime', 'name of this anime', "what's that anime", 'what anime is it', 'name of anime', 'sauce to that anime'], 'consoleLog': True, 'fileLog': True, 'stats': True}, 'Twitter': {'run': True, 'ignoredUsers': [], 'flags': [], 'ignoreRT': True, 'keys': {'consumerKey': None, 'consumerSecret': None, 'accessTokenKey': None, 'accessTokenSecret': None}, 'stream': {'languages': ["en"], 'flags': []}, 'monitoring': {'accounts': [], 'checkReplies': False}}, 'Discord': {'run': True, 'flags': [], 'keys': {'token': None}}, 'Line': {'run': True, 'flags': [], 'keys': {'channelAccessToken': None, 'channelSecret': None}, 'imagesTimeout': 3600}, 'Caches': {'encoding': 'utf-8', 'keys': {'tracemoe': None, 'saucenao': None}}, 'Database': {}, 'Hash': {'algorithm': 'Average Hash'}, 'Parser': {}, 'Search': {'thresholds': {'erinaSimilarity': 100, 'tracemoeSimilarity': 90, 'saucenaoSimilarity': 90, 'iqdbSimilarity': 90}}, 'Server': {'host': '127.0.0.1', 'port': 5000, 'disableConsoleMessages': True}}
    classes.tempData = configFile.read()
    for element in classes.tempData:
        classes.storedData[element] = classes.tempData[element]
    
    Erina = classes.ErinaConfig()
    Twitter = classes.TwitterConfig()
    Discord = classes.DiscordConfig()
    Line = classes.LineConfig()
    Caches = classes.CachesConfig()
    Database = classes.DatabaseConfig()
    Hash = classes.HashConfig()
    Parser = classes.ParserConfig()
    Search = classes.SearchConfig()
    Server = classes.ServerConfig()
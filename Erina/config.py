"""
Erina Project Configuration File

You can add your API Keys and Configure Erina with this file.

Erina Project
© Anime no Sekai - 2020
"""
import json
from Erina.env_information import erina_dir
from Erina._config import classes

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

    with open(erina_dir + "/Erina/_config/config.json", "w", encoding="utf-8") as configFile:
        json.dump(export(), configFile, ensure_ascii=False, indent=4)

def default():
    """
    Backs up the configuration to the default values
    """
    with open(erina_dir + "/Erina/_config/default.json", "w", encoding="utf-8") as defaultFile:
        data = json.load(defaultFile)
    with open(erina_dir + "/Erina/_config/config.json", "w", encoding="utf-8") as configFile:
        json.dump(data, configFile, ensure_ascii=False, indent=4)
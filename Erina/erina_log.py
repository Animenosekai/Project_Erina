"""
Logging utility for Erina

Erina Project
© Anime no Sekai - 2020
"""

import json
import lifeeasy
from Erina import config

def resetstats():
    """
    Resetting the stats.
    """
    with open('ErinaStats.json', 'w') as jsonFile:
        json.dump({"launch": [], "twitter": {"stream_hit": 0, "hit": 0, "media_hit": 0, "successful_hit": 0, "successful_parent_hit": 0, "mention_hit": 0, "asking_mention_hit": 0}, "line": {"image_reception": [], "source_search": [], "successful_source_search": [], "anime_info_request": [], "successful_anime_info": [], "anime_description_request": [], "successful_anime_description": [], "number_of_stored_images": 0}, "discord": {"ready": 0, "anime_info_request": [], "anime_info_successful": 0, "anime_description_request": [], "anime_description_successful": 0, "helpcenter_request": 0, "erinastats_request": 0, "erinadev_request": 0, "erinainvite_request": 0, "erinadonate_request": 0, "source_search_request": 0, "source_search": [], "successful_search_request": 0}, "database": {"number_of_manami_auto_update": 0, "manami_database_access": 0, "manamai_database_entry_lookup": 0, "erina_database_access": 0, "erina_database_entry_lookup": 0}, "search": {"aniliistid_search": [], "title_search": [], "hash_search": []}, "caches": {"anilist_caching": [], "anilist_search_caching": [], "tracemoe_caching": [], "erina_caching": [], "saucenao_caching": [], "iqdb_caching": []}, "api": {"line_images": 0, "erina_stats": 0, "anime_search": 0, "nosleep": 0}, "hash": [], "base64": 0, "error": []}, jsonFile, indent=2, sort_keys=True)

def logerror(text):
    """
    Logging Errors.
    """
    if config.Erina.console_log:
        print('[Error] ' + text)
    if config.Erina.file_log:
        lifeeasy.write_file('ErinaLogs.txt', lifeeasy.today() + ' ' + lifeeasy.current_time() + "   [Error] " + text + '\n', append=True)
    if config.Erina.stats:
        with open("ErinaStats.json", "r") as jsonFile:
            data = json.load(jsonFile)
        errors_list = data["error"]
        errors_list.append({f"{str(lifeeasy.today())} {str(lifeeasy.current_time())}": text})
        data["error"] = errors_list
        with open("ErinaStats.json", "w") as jsonFile:
            json.dump(data, jsonFile, indent=2, sort_keys=True, ensure_ascii=False)

def loglaunch(text):
    """
    Logging Launch Events.
    """
    if config.Erina.console_log:
        if text != '':
            print("[Erina] " + text)
    if config.Erina.file_log:
        if text == '':
            lifeeasy.write_file('ErinaLogs.txt', '\n', append=True)
            lifeeasy.write_file('ErinaLogs.txt', '\n', append=True)
            lifeeasy.write_file('ErinaLogs.txt', '\n', append=True)
            lifeeasy.write_file('ErinaLogs.txt', lifeeasy.today() + ' ' + lifeeasy.current_time() + "   ########## STARTING ########## " + text + '\n', append=True)
            if config.Erina.stats:
                with open("ErinaStats.json", "r") as jsonFile:
                    data = json.load(jsonFile)
                launch_list = data["launch"]
                launch_list.append({"twitter": config.run_twitter_client, "discord": config.run_discord_client, "line": config.run_line_client})
                data["launch"] = launch_list
                with open("ErinaStats.json", "w") as jsonFile:
                    json.dump(data, jsonFile, indent=2, sort_keys=True, ensure_ascii=False)
        else:
            lifeeasy.write_file('ErinaLogs.txt', lifeeasy.today() + ' ' + lifeeasy.current_time() + "   [Erina] " + text + '\n', append=True)


def logtwitter(text, add_to_stream_hit=False, add_to_hit=False, add_to_media_hit=False, add_to_successful_hit=False, add_to_successful_parent_hit=False, add_to_mention_hit=False, add_to_asking_mention_hit=False):
    """
    Logging Twitter Messages.
    """
    if text != '':
        if config.Erina.console_log:
            print("[ErinaTwitter] " + text)
        if config.Erina.file_log:
            lifeeasy.write_file('ErinaLogs.txt', lifeeasy.today() + ' ' + lifeeasy.current_time() + "   [ErinaTwitter] " + text + '\n', append=True)
    if config.Erina.stats:
        with open("ErinaStats.json", "r") as jsonFile:
            data = json.load(jsonFile)
        if add_to_stream_hit:
            data["twitter"]['stream_hit'] += 1
        if add_to_hit:
            data["twitter"]['hit'] += 1
        if add_to_media_hit:
            data["twitter"]['media_hit'] += 1
        if add_to_successful_hit:
            data["twitter"]['successful_hit'] += 1
        if add_to_successful_parent_hit:
            data["twitter"]['successful_parent_hit'] += 1
        if add_to_mention_hit:
            data["twitter"]['mention_hit'] += 1
        if add_to_asking_mention_hit:
            data["twitter"]['asking_mention_hit'] += 1
        with open("ErinaStats.json", "w") as jsonFile:
            json.dump(data, jsonFile, indent=2, sort_keys=True, ensure_ascii=False)

def logsearch(text, search_type='', value=''):
    """
    Logging Search Queries.
    """
    if config.Erina.console_log:
        print("[ErinaSearch] " + text)
    if config.Erina.file_log:
        lifeeasy.write_file('ErinaLogs.txt', lifeeasy.today() + ' ' + lifeeasy.current_time() + "   [ErinaSearch] " + text + '\n', append=True)
    if config.Erina.stats:
        with open("ErinaStats.json", "r") as jsonFile:
            data = json.load(jsonFile)
        if search_type == 'anilistid':
            data_list = data["search"]['aniliistid_search']
            data_list.append(value)
            data["search"]['aniliistid_search'] = data_list
        if search_type == 'title':
            data_list = data["search"]['title_search']
            data_list.append(value)
            data["search"]['title_search'] = data_list
        if search_type == 'hash':
            data_list = data["search"]['hash_search']
            data_list.append(value)
            data["search"]['hash_search'] = data_list
        with open("ErinaStats.json", "w") as jsonFile:
            json.dump(data, jsonFile, indent=2, sort_keys=True, ensure_ascii=False)

def logline(text, stattype='', value=None):
    """
    Logging Line Actions
    """
    if config.Erina.console_log:
        if text != '':
            print("[ErinaLine] " + text)
    if config.Erina.file_log:
        if text != '':
            lifeeasy.write_file('ErinaLogs.txt', lifeeasy.today() + ' ' + lifeeasy.current_time() + "   [ErinaLine] " + text + '\n', append=True)
    if config.Erina.stats:
        with open("ErinaStats.json", "r") as jsonFile:
            data = json.load(jsonFile)
        if stattype == 'image_reception':
            data_list = data["line"]['image_reception']
            data_list.append(value)
            data["line"]['image_reception'] = data_list
        if stattype == 'source_search':
            data_list = data["line"]['source_search']
            data_list.append(value)
            data["line"]['source_search'] = data_list
        if stattype == 'successful_source_search':
            data_list = data["line"]['successful_source_search']
            data_list.append(value)
            data["line"]['successful_source_search'] = data_list
        if stattype == 'anime_info_request':
            data_list = data["line"]['anime_info_request']
            data_list.append(value)
            data["line"]['anime_info_request'] = data_list
        if stattype == 'successful_anime_info':
            data_list = data["line"]['successful_anime_info']
            data_list.append(value)
            data["line"]['successful_anime_info'] = data_list
        if stattype == 'anime_description_request':
            data_list = data["line"]['anime_description_request']
            data_list.append(value)
            data["line"]['anime_description_request'] = data_list
        if stattype == 'successful_anime_description':
            data_list = data["line"]['successful_anime_description']
            data_list.append(value)
            data["line"]['successful_anime_description'] = data_list
        if stattype == 'number_of_stored_images':
            data["api"]['number_of_stored_images'] += value
        if stattype == 'set_number_of_stored_images':
            data["api"]['number_of_stored_images'] = value
        with open("ErinaStats.json", "w") as jsonFile:
            json.dump(data, jsonFile, indent=2, sort_keys=True, ensure_ascii=False)

def logapi(text, apitype=''):
    """
    Logging API Actions
    """
    if config.Erina.console_log:
        print("[API] " + text)
    if config.Erina.file_log:
        lifeeasy.write_file('ErinaLogs.txt', lifeeasy.today() + ' ' + lifeeasy.current_time() + "   [API] " + text + '\n', append=True)
    if config.Erina.stats:
        with open("ErinaStats.json", "r") as jsonFile:
            data = json.load(jsonFile)
        if apitype == 'line_images':
            data["api"]['line_images'] += 1
        if apitype == 'erina_stats':
            data["api"]['erina_stats'] += 1
        if apitype == 'anime_search':
            data["api"]['anime_search'] += 1
        if apitype == 'nosleep':
            data["api"]['nosleep'] += 1
        with open("ErinaStats.json", "w") as jsonFile:
            json.dump(data, jsonFile, indent=2, sort_keys=True, ensure_ascii=False)

def loghash(text, hash_string=''):
    """
    Logging Hash Actions
    """
    if config.Erina.console_log:
        print("[ErinaHash] " + text)
    if config.Erina.file_log:
        lifeeasy.write_file('ErinaLogs.txt', lifeeasy.today() + ' ' + lifeeasy.current_time() + "   [ErinaHash] " + text + '\n', append=True)
    if config.Erina.stats:
        if hash_string != '':
            with open("ErinaStats.json", "r") as jsonFile:
                data = json.load(jsonFile)
            hashes_list = data["hash"]
            hashes_list.append(hash_string)
            data["hash"] = hashes_list
            with open("ErinaStats.json", "w") as jsonFile:
                json.dump(data, jsonFile, indent=2, sort_keys=True, ensure_ascii=False)
        elif hash_string == 'base64':
            with open("ErinaStats.json", "r") as jsonFile:
                data = json.load(jsonFile)
            data["base64"] += 1
            with open("ErinaStats.json", "w") as jsonFile:
                json.dump(data, jsonFile, indent=2, sort_keys=True, ensure_ascii=False)


def logdiscord(text='', stattype='', value=''):
    """
    Logging Discord Actions
    """
    if config.Erina.console_log:
        if text != '':
            print("[ErinaDiscord] " + text)
    if config.Erina.file_log:
        if text != '':
            lifeeasy.write_file('ErinaLogs.txt', lifeeasy.today() + ' ' + lifeeasy.current_time() + "   [ErinaDiscord] " + text + '\n', append=True)

    if config.Erina.stats:
        with open("ErinaStats.json", "r") as jsonFile:
            data = json.load(jsonFile)

        if stattype == 'ready':
            data["discord"]['ready'] += 1

        if stattype == 'anime_info_request':
            datalist = data["discord"]['anime_info_request']
            datalist.append(value)
            data["discord"]['anime_info_request'] = datalist
        if stattype == 'anime_info_successful':
            data["discord"]['anime_info_successful'] += 1

        if stattype == 'anime_description_request':
            datalist = data["discord"]['anime_description_request']
            datalist.append(value)
            data["discord"]['anime_description_request'] = datalist
        if stattype == 'anime_description_successful':
            data["discord"]['anime_description_successful'] += 1

        if stattype == 'helpcenter_request':
            data["discord"]['helpcenter_request'] += 1
        if stattype == 'erinastats_request':
            data["discord"]['erinastats_request'] += 1
        if stattype == 'erinadev_request':
            data["discord"]['erinadev_request'] += 1
        if stattype == 'erinainvite_request':
            data["discord"]['erinainvite_request'] += 1
        if stattype == 'erinadonate_request':
            data["discord"]['erinadonate_request'] += 1
        
        if stattype == 'source_search_request':
            data["discord"]['source_search_request'] += 1
        if stattype == 'source_search':
            datalist = data["discord"]['source_search']
            datalist.append(value)
            data["discord"]['source_search'] = datalist
        if stattype == 'successful_search_request':
            data["discord"]['successful_search_request'] += 1

        with open("ErinaStats.json", "w") as jsonFile:
            json.dump(data, jsonFile, indent=2, sort_keys=True, ensure_ascii=False)

def logdatabase(text='', stattype='', value=0):
    """
    Logging Database Actions
    """
    if config.Erina.console_log:
        if text != '':
            print("[ErinaDB] " + text)
    if config.Erina.file_log:
        if text != '':
            lifeeasy.write_file('ErinaLogs.txt', lifeeasy.today() + ' ' + lifeeasy.current_time() + "   [ErinaDB] " + text + '\n', append=True)
    if config.Erina.stats:
        with open("ErinaStats.json", "r") as jsonFile:
            data = json.load(jsonFile)
        if stattype == 'manami_auto_update':
            data["database"]['number_of_manami_auto_update'] += 1
        if stattype == 'manami_database_access':
            data["database"]['manami_database_access'] += 1
        if stattype == 'manamai_database_entry_lookup':
            data["database"]['manamai_database_entry_lookup'] += value
        
        if stattype == 'erina_database_access':
            data["database"]['erina_database_access'] += 1
        if stattype == 'erina_database_entry_lookup':
            data["database"]['erina_database_entry_lookup'] += value

        with open("ErinaStats.json", "w") as jsonFile:
            json.dump(data, jsonFile, indent=2, sort_keys=True, ensure_ascii=False)

def logcaches(text, stattype='', value=''):
    """
    Logging ErinaCaches Actions
    """
    if config.Erina.console_log:
        print("[ErinaCaches] " + text)
    if config.Erina.file_log:
        lifeeasy.write_file('ErinaLogs.txt', lifeeasy.today() + ' ' + lifeeasy.current_time() + "   [ErinaCaches] " + text + '\n', append=True)
    if config.Erina.stats:
        with open("ErinaStats.json", "r") as jsonFile:
            data = json.load(jsonFile)
        if stattype == 'anilist':
            datalist = data["caches"]["anilist_caching"]
            datalist.append(value)
            data["caches"]["anilist_caching"] = datalist
        if stattype == 'anilist_search':
            datalist = data["caches"]["anilist_search_caching"]
            datalist.append(value)
            data["caches"]["anilist_search_caching"] = datalist
        if stattype == 'tracemoe':
            datalist = data["caches"]["tracemoe_caching"]
            datalist.append(value)
            data["caches"]["tracemoe_caching"] = datalist
        if stattype == 'saucenao':
            datalist = data["caches"]["saucenao_caching"]
            datalist.append(value)
            data["caches"]["saucenao_caching"] = datalist
        if stattype == 'iqdb':
            datalist = data["caches"]["iqdb_caching"]
            datalist.append(value)
            data["caches"]["iqdb_caching"] = datalist
        if stattype == 'erina':
            datalist = data["caches"]["erina_caching"]
            datalist.append(value)
            data["caches"]["erina_caching"] = datalist
        with open("ErinaStats.json", "w") as jsonFile:
            json.dump(data, jsonFile, indent=2, sort_keys=True, ensure_ascii=False)
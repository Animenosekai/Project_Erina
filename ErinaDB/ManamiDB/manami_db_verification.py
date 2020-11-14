"""
Manami Database update API for the Erina Project

@author: Anime no Sekai
Erina Project - 2020
"""
import re
import json
import datetime
import time

import requests

import env_information
from ErinaDB.ManamiDB.manami_db_data import Database

#import erina_log

manami_database_path = env_information.erina_dir + "/ErinaDB/ManamiDB/"


def convert_to_int(element):
    element = str(element).split('.')[0]
    element = re.sub("[^0-9]", "", str(element))
    if element != '':
        return int(element)
    else:
        return 0


def verify_manami_adb():
    """
    Checks for a new version of the database on GitHub
    """
    start_time = time.time()
    with open(manami_database_path + 'current_release.txt') as current_release_file:
        current_release_week = str(current_release_file.read()).replace(" ", '').replace("\n", '')
    iso_calendar = datetime.date.today().isocalendar()
    current_week = str(iso_calendar[0]) + '-' + str(iso_calendar[1])
    if current_release_week != current_week:
        """
        erina_log.logdatabase('[ManamiDB] New ADB release found!')
        erina_log.logdatabase('[ManamiDB] ADB auto-update...', stattype='manami_auto_update')
        """
        print("new adb")
        manami_adb = json.loads(requests.get('https://raw.githubusercontent.com/manami-project/anime-offline-database/master/anime-offline-database.json').text)
        data = {}
        for anime in manami_adb["data"]:
            link = None
            anilist_id = None
            for sourceLink in anime["sources"]:
                if sourceLink.find("anilist.co") != -1:
                    link = sourceLink
            if link is not None:
                anilist_id = convert_to_int(link[link.rfind("/"):])
                data[anilist_id] = [ str(anime["title"]).lower() ]
                data[anilist_id].extend([str(title).lower() for title in anime["synonyms"]])
            else:
                continue
        with open(manami_database_path + 'manami_database_data.json', 'w', encoding="utf-8") as newFile:
            json.dump(data, newFile, ensure_ascii=False)
        with open(manami_database_path + 'current_release.txt', 'w', encoding="utf-8") as newReleaseFile:
            newReleaseFile.write(current_week)
        Database.updateData(data)
    else:
        #erina_log.logdatabase('[ManamiDB] less than a week from last check.')
        print("less than a week")
    end_time = time.time()
    print(end_time - start_time)
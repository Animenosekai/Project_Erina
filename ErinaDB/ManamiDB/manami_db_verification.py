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
from safeIO import TextFile

from Erina.env_information import erina_dir
from ErinaDB.ManamiDB.manami_db_data import Database

#import erina_log

manami_database_path = erina_dir + "/ErinaDB/ManamiDB/"
currentReleaseFile = TextFile(manami_database_path + 'current_release.txt')

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

    ## Checking if new week
    current_release_week = currentReleaseFile.read().replace(" ", '').replace("\n", '')
    iso_calendar = datetime.date.today().isocalendar()
    current_week = str(iso_calendar[0]) + '-' + str(iso_calendar[1])
    
    if current_release_week != current_week: # If new week
        manami_adb = json.loads(requests.get('https://raw.githubusercontent.com/manami-project/anime-offline-database/master/anime-offline-database.json').text)
        data = {}
        for anime in manami_adb["data"]:
            link = None
            anilist_id = None
            for sourceLink in anime["sources"]:
                if sourceLink.find("anilist.co") != -1:
                    link = sourceLink
            if link is not None: # parser the data
                anilist_id = convert_to_int(link[link.rfind("/"):])
                data[anilist_id] = [ str(anime["title"]).lower().replace(" ", '') ]
                data[anilist_id].extend([str(title).lower().replace(" ", '') for title in anime["synonyms"]])
            else:
                continue
        # write out the data
        TextFile(manami_database_path + 'manami_database_data.json').write(data)
        currentReleaseFile.write(current_week)
        Database.updateData(data)
    else: # not new week
        print("less than a week")
    print(time.time() - start_time)
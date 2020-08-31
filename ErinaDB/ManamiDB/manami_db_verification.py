"""
Manami Database update API for the Erina Project

@author: Anime no Sekai
Erina Project - 2020
"""
import sys
sys.path.append('...')

import json
import lifeeasy

import env_information
import erina_log

manami_database_path = env_information.erina_dir + "/ErinaDB/ManamiDB/"


def verify_manami_adb():
    """
    Checks for a new version of the database on GitHub
    """
    current_adb_release_file = open(manami_database_path + 'current_release.txt')
    line = current_adb_release_file.readline()
    current_week = str(lifeeasy.today_raw().isocalendar()[0]) + '-' + str(lifeeasy.today_raw().isocalendar()[1])
    current_adb_release_file.close()
    if line != current_week:
        erina_log.logdatabase('[ManamiDB] New ADB release found!')
        erina_log.logdatabase('[ManamiDB] ADB auto-update...', stattype='manami_auto_update')
        manami_adb_request = lifeeasy.request('https://raw.githubusercontent.com/manami-project/anime-offline-database/master/anime-offline-database.json', 'get')
        manami_adb_file = open(manami_database_path + 'manami_database_data.py', 'w')
        manami_adb_file.write('"""\n')
        manami_adb_file.write('Manami Project - Anime Database\n')
        manami_adb_file.write('\n')
        manami_adb_file.write('© Manami Project 2020\n')
        manami_adb_file.write('"""\n')
        manami_adb_file.write('\n')
        manami_adb_file.write('\n')
        manami_adb_file.write('def database():\n')
        manami_adb_file.write(f'    data = {str(json.loads(manami_adb_request.text))}\n')
        manami_adb_file.write(f'    return(data)')
        manami_adb_file.close()
        current_adb_release_file = open(manami_database_path + 'current_release.txt', 'w')
        current_adb_release_file.write(current_week)
        current_adb_release_file.close()
    else:
        erina_log.logdatabase('[ManamiDB] less than a week from last check.')
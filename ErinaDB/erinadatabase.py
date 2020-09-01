"""
Anime Database API for the Erina Project

@author: Anime no Sekai
Erina Project - 2020
"""
import sys
sys.path.append('..')

import env_information
import erina_log
from .ManamiDB import manami_db_verification

def erina_database():
    """
    Returns Erina Database Path
    """
    return env_information.erina_dir + '/ErinaDB/ErinaDatabase/'

def manami_database():
    """
    Verifies and Returns the Manami Project Database
    """
    from .ManamiDB import manami_database_data
    erina_log.logdatabase(text='', stattype='manami_database_access')
    manami_db_verification.verify_manami_adb()
    return manami_database_data.database()
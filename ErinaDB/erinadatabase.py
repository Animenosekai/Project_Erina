"""
Anime Database API for the Erina Project

@author: Anime no Sekai
Erina Project - 2020
"""
from Erina.env_information import erina_dir
from ErinaDB.ManamiDB import manami_db_verification
from ErinaDB.ManamiDB.manami_db_data import Database

def erina_database():
    """
    Returns Erina Database Path
    """
    return erina_dir + '/ErinaDB/ErinaDatabase/'

def manami_database():
    """
    Verifies and Returns the Manami Project Database
    """
    manami_db_verification.verify_manami_adb()
    return Database.data
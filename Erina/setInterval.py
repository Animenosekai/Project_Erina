from filecenter import files_in_dir
from time import sleep
from threading import Thread
from Erina.erina_log import checkForLogsTimeout
from ErinaLine.utils.Images import checkImages
from ErinaDB.ManamiDB.manami_db_verification import verify_manami_adb
from Erina.env_information import erina_dir
from Erina.erina_stats import erina
from Erina.erina_stats import StatsAppend

caches_path = [erina_dir + "/ErinaCaches/AniList_Cache", erina_dir + "/ErinaCaches/Erina_Cache", erina_dir + "/ErinaCaches/IQDB_Cache", erina_dir + "/ErinaCaches/SauceNAO_Cache", erina_dir + "/ErinaCaches/TraceMOE_Cache"]

def checkForTimeout():
    """
    Checks infinitely for timeouts
    """
    while True:
        checkForLogsTimeout()
        checkImages()
        sleep(10) # Checks every 10 seconds

def checkForUpdate():
    """
    Checks infinitely for any update
    """
    while True:
        verify_manami_adb()
        numberOfCaches = 0
        for path in caches_path:
            numberOfCaches += len(files_in_dir(path))
        StatsAppend(erina.cacheFilesCount, numberOfCaches)
        sleep(86400) # Checks every day


Thread(target=checkForTimeout, daemon=True).start()
Thread(target=checkForUpdate, daemon=True).start()
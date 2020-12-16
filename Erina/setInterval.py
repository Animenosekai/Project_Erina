from time import sleep
from threading import Thread
from Erina.erina_log import checkForLogsTimeout
from ErinaLine.utils.Images import checkImages
from ErinaDB.ManamiDB.manami_db_verification import verify_manami_adb

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
        sleep(86400) # Checks every day


Thread(target=checkForTimeout, daemon=True).start()
Thread(target=checkForUpdate, daemon=True).start()
"""
Erina Line Images Checker for the Erina Project

@author: Anime no Sekai
Erina Project - 2020
"""
import time

import filecenter

from Erina.config import Line as LineConfig
from Erina.erina_log import log
import Erina.env_information as env_information
from Erina.erina_stats import StatsAppend
from Erina.erina_stats import line as LineStats

images_path = env_information.erina_dir + '/ErinaLine/images/'
current_images_dict = {}

def check(user_id):
    '''
    Add an entry to check.
    '''
    global current_images_dict
    current_images_dict[user_id] = time.time()
    StatsAppend(LineStats.storedImages, len(filecenter.files_in_dir(images_path)))

def checkImages():
    '''
    Timeout checking function.
    '''
    global current_images_dict
    number_of_deleted_files = 0 # logging purposes
    for entry in current_images_dict:
        if time.time() - current_images_dict[entry] > LineConfig.images_timeout:
            if filecenter.delete(images_path + entry + '.erina_image') == 0:
                current_images_dict.pop(entry, None)
                number_of_deleted_files += 1 # logging purposes
    ### LOGGING
    if number_of_deleted_files > 0:
        if number_of_deleted_files == 1:
            log("ErinaLine", "[Image Checker] Deleted 1 entry")
        else:
            log("ErinaLine", f'[Image Checker] Deleted {str(number_of_deleted_files)} entries')
        StatsAppend(LineStats.storedImages, len(filecenter.files_in_dir(images_path)))
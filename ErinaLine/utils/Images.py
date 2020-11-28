"""
Erina Line Images Checker for the Erina Project

@author: Anime no Sekai
Erina Project - 2020
"""
import time

import filecenter

import config
import erina_log
import env_information

images_path = env_information.erina_dir + '/ErinaLine/images/'
current_images_dict = {}

def check(user_id):
    '''
    Add an entry to check.
    '''
    global current_images_dict
    current_images_dict[user_id] = time.time()

def start_check():
    '''
    Timeout checking function.
    '''
    global current_images_dict
    while True:
        number_of_deleted_files = 0 # logging purposes
        for entry in current_images_dict:
            if time.time() - current_images_dict[entry] > config.line_images_deletion_time:
                if filecenter.delete(images_path + entry + '.erina_image') == 0:
                    current_images_dict.pop(entry, None)
                    number_of_deleted_files += 1 # logging purposes
        ### LOGGING
        if number_of_deleted_files != 0:
            if number_of_deleted_files == 1:
                erina_log.logline(f'[Image Checker] Deleted 1 entry.', stattype='number_of_stored_images', value=-1)
            else:
                erina_log.logline(f'[Image Checker] Deleted {str(number_of_deleted_files)} entries.', stattype='number_of_stored_images', value=-number_of_deleted_files)
        
        time.sleep(5)
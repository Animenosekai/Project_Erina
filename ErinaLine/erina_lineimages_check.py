"""
Erina Line Images Checker for the Erina Project

@author: Anime no Sekai
Erina Project - 2020
"""
import sys
sys.path.append('..')

import time
import filecenter
import env_information
import erina_log
import config

images_path = env_information.erina_dir + '/ErinaLine/images/'
current_images_dict = {}

def add_to_check(user_id):
    '''
    Add an entry to check.
    '''
    global current_images_dict
    current_images_dict[user_id] = time.time()
    erina_log.logline('[Image Checker] Entry added!', stattype='number_of_stored_images', value=1)

def start_check():
    '''
    Timeout checking function.
    '''
    global current_images_dict
    erina_log.logline('[Image Checker] Starting to check images...')
    erina_log.logline(text='', stattype='set_number_of_stored_images', value=len(filecenter.files_in_dir(images_path))-1)

    while True:
        number_of_deleted_files = 0
        for entry in current_images_dict:
            if time.time() - current_images_dict[entry] > config.line_images_deletion_time:
                exit_number = filecenter.delete(images_path + entry + '.erina_image')
                if exit_number == 0:
                    current_images_dict.pop(entry, None)
                    number_of_deleted_files += 1
        if number_of_deleted_files != 0:
            if number_of_deleted_files == 1:
                erina_log.logline(f'[Image Checker] Deleted 1 entry.', stattype='number_of_stored_images', value=-1)
            else:
                erina_log.logline(f'[Image Checker] Deleted {str(number_of_deleted_files)} entries.', stattype='number_of_stored_images', value=-number_of_deleted_files)
        time.sleep(5)
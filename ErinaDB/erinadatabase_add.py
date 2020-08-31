"""
Anime Episodes Hashing for ErinaDB for the Erina Project

@author: Anime no Sekai
Erina Project - 2020
"""

import threading
import sys
from time import process_time
from datetime import datetime
from datetime import timedelta

import cv2
import filecenter
import lifeeasy
from PIL import Image
import imagehash

from . import erina_aniep
import env_information
from ErinaCaches import erinacache

lifeeasy.clear()
erinadb_path = env_information.erina_dir + '/ErinaDB/'
erina_database_path = erinadb_path + 'ErinaDatabase/'
erina_add_animes_path = erinadb_path + 'Animes/'

anime = ''
fps_dict = {}
frames_stats_dict = {}
queue = 0

def add_animes_to_database(auto_analyze=True):
    global anime
    global fps_dict
    global frames_stats_dict
    global queue

    for file in filecenter.files_in_dir(erina_add_animes_path):
        if file == '.DS_Store':
            continue
        if file == '.gitkeep':
            continue
        if filecenter.type_from_extension(filecenter.extension_from_base(file)) == 'Folder':
            anime = file

            if anime == '':
                print('No anime folder found.')
                quit()

            if '-a' in sys.argv or '--auto' in sys.argv or auto_analyze == True:
                anilist_filename = erinacache.anilist_search_caching(anime)
                anilist_id = anilist_filename.replace('.erina', '')
                season = '1'
            else:
                print('What is the AniList ID for ' + anime + '?')
                anilist_id = input('> ')
                print('Which season is it?')
                season = input('> ')



            def analyze_episode(episode):
                """
                Internal Function that is ran by multiple thread to analyze each frame of an anime episode and create a file with its hash.
                Erina Project
                © Anime no Sekai - 2020
                """

                global fps_dict
                global frames_stats_dict
                global queue

                queue += 1
                episode_number = erina_aniep.episode_from_filename(episode, anime)
                
                frames_stats_dict[episode_number] = {'frame': 0, 'total_frames': 0, 'status': 'Starting'}

                video = cv2.VideoCapture(erina_add_animes_path + anime + '/' + episode)

                frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
                framerate = video.get(cv2.CAP_PROP_FPS)
                duration = frame_count/framerate

                success, image = video.read()
                
                count = 0
                fps = 0
                start_loop_fps = 0
                end_loop_fps = 0
                start_loop_time = process_time()
                from_dict = {}
                first_frame_dict = {}

                new_database_path = erina_database_path + anime + '/' + episode_number
                if filecenter.isdir(new_database_path) == False:
                    filecenter.make_dir(new_database_path)
                
                skip = False
                while success:
                    if skip == False:
                        hashing_image = Image.fromarray(image)
                        image_hash = imagehash.average_hash(hashing_image)

                        second = count/framerate

                        try:
                            from_second = from_dict[str(image_hash)]
                            at_second = (float(from_second) + second) / 2
                        except:
                            from_dict[str(image_hash)] = second
                            from_second = second
                            at_second = second

                        try:
                            first_frame = first_frame_dict[str(image_hash)]
                        except:
                            first_frame_dict[str(image_hash)] = count
                            first_frame = count
                                
                        database_content = []
                        database_content.append('AniList ID: ' + anilist_id)
                        database_content.append('Anime: ' + anime)
                        database_content.append('Season: ' + season)
                        database_content.append('Episode: ' + episode_number)
                        database_content.append('First Frame: ' + str(first_frame))
                        database_content.append('Last Frame: ' + str(count))
                        database_content.append('From: ' + str(from_second))
                        database_content.append('From (formatted): ' + str(timedelta(seconds=from_second)))
                        database_content.append('To: ' + str(second))
                        database_content.append('To (formatted): ' + str(timedelta(seconds=second)))
                        database_content.append('At: ' + str(at_second))
                        database_content.append('At (formatted): ' + str(timedelta(seconds=at_second)))
                        database_content.append('Hash: ' + str(image_hash))
                        database_content.append('Hashing Algorithm: Average Hash (aHash)')
                        database_content.append('Filename: ' + episode)
                        database_content.append('Episode Framerate: ' + str(framerate))
                        database_content.append('Episode Duration: ' + str(duration))
                        database_content.append('Episode Duration (formatted): ' + str(timedelta(seconds=duration)))
                        database_content.append('Episode Frame Count: ' + str(frame_count))
                        database_content.append('')
                        database_content.append('Analyze Date: ' + str(datetime.timestamp(datetime.today())))
                        database_content.append('Analyze Date (formatted): ' + lifeeasy.today() + ' at ' + lifeeasy.current_time())
                        
                        lifeeasy.write_file(str(image_hash) + '.erina', database_content, new_database_path)

                    frames_stats_dict[episode_number] = {'frame': count, 'total_frames': frame_count, 'status': 'Active'}
                    
                    count += 1

                    end_loop_fps += 1
                    end_loop_time = process_time()
                    if end_loop_time - start_loop_time > 1:
                        fps = int(end_loop_fps - start_loop_fps)
                        fps_dict[episode_number] = fps
                        start_loop_time = process_time()
                        start_loop_fps = end_loop_fps

                    if skip == True:
                        skip = False
                        success, image = video.read()
                    else:
                        skip = True
                        success = video.grab()
                queue -= 1
                frames_stats_dict[episode_number] = {'frame': count, 'total_frames': frame_count, 'status': 'Done'}
                fps_dict.pop(episode_number, None)


            start_time = process_time()
            for episode in filecenter.files_in_dir(erina_add_animes_path + anime):
                if filecenter.type_from_extension(filecenter.extension_from_base(episode)) != 'Video':
                    continue
                else:
                    print('Opening new thread...')
                    thread = threading.Thread(target=analyze_episode, args=(episode,))
                    thread.daemon = True
                    thread.start()

            stop_command_output = False

            def console_output():
                '''
                Internal Function used to display statistics during processing the images.\n
                Might be disabled and thus main function analyze_episode could be optimized for better performance but I prefer seeing what's going on. 
                '''
                total_fps = 0
                total_frames = 'N/A'
                total_frames_frame = 0
                total_frames_frames = 0
                for element in fps_dict:
                    total_fps += fps_dict[element]
                single_thread_stats = ''
                for element in frames_stats_dict:
                    total_frames_frame += frames_stats_dict[element]['frame']
                    total_frames_frames += frames_stats_dict[element]['total_frames']
                    try:
                        try:
                            thread_percentage = int(frames_stats_dict[element]['frame']) * 100 / int(frames_stats_dict[element]['total_frames'])
                            thread_percentage = round(thread_percentage, 1)
                        except:
                            thread_percentage = 'n/a'
                        try:
                            frames_per_second = str(fps_dict[element])
                        except:
                            frames_per_second = 'n/a'
                        single_thread_stats = single_thread_stats + 'Episode ' + str(element) + ': Frame ' + str(frames_stats_dict[element]['frame']) + '/' + str(int(frames_stats_dict[element]['total_frames'])) + ' (' + str(thread_percentage) + '%) ・ Analyze Speed: ' + frames_per_second + 'FPS ・ Status: ' + frames_stats_dict[element]['status'] + '\n'
                    except:
                        try:
                            thread_percentage = int(frames_stats_dict[element]['frame']) * 100 / int(frames_stats_dict[element]['total_frames'])
                            thread_percentage = round(thread_percentage, 1)
                        except:
                            thread_percentage = 'n/a'
                        single_thread_stats = single_thread_stats + 'Episode ' + str(element) + ': Frame ' + str(frames_stats_dict[element]['frame']) + '/' + str(int(frames_stats_dict[element]['total_frames'])) + ' (' + str(thread_percentage) + '%) ・ Analyze Speed: 0FPS ・ Status: Starting\n'

                try:
                    total_frames_percentage = total_frames_frame * 100 / total_frames_frames
                    total_frames_percentage = round(total_frames_percentage, 2)
                except:
                    total_frames_percentage = 'n/a'
                total_frames = str(total_frames_frame) + '/' + str(int(total_frames_frames))

                lifeeasy.sleep(0.1)
                lifeeasy.clear()
                try:
                    remaining_frames = total_frames_frames - total_frames_frame
                    remaining_time = remaining_frames / int(total_fps)
                    eta = str(timedelta(seconds=remaining_time))
                except:
                    eta = 'N/A'
                print(f'Anime: {anime}\nFrame: {total_frames} ({str(total_frames_percentage)}%)\nAnalyze Speed: {str(total_fps)}FPS\nRemaining Time (ETA): {eta[:-7]}\n\nActive Threads\nーーーーーーーーーーーー\n{single_thread_stats}\nErina Project\n©Anime no Sekai - 2020')
                if stop_command_output == False:
                    thread = threading.Thread(target=console_output)
                    thread.daemon = True
                    thread.start()

            console_output()

            lifeeasy.sleep(3)

            while queue != 0:
                lifeeasy.sleep(1)

            stop_command_output = True

            lifeeasy.sleep(3)

            print('')
            end_time = process_time()
            print('Total time: ' + str(end_time - start_time) + ' seconds')

            if '-a' not in sys.argv and '--auto' not in sys.argv and auto_analyze == False:
                print('')
                print(f'Caching AniList API with the ID {str(anilist_id)}...')
                erinacache.anilist_caching(int(anilist_id))
            print(f'{anime} has been added to the database')

if __name__ == '__main__':
    add_animes_to_database(auto_analyze=False)
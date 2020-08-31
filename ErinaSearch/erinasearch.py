"""
Anime Search API for the Erina Project

@author: Anime no Sekai
Erina Project - 2020
"""
import sys
sys.path.append('.')
sys.path.append('..')

import json
from io import BytesIO
from base64 import b64decode
import lifeeasy
import filecenter
import imagehash

import env_information
import erina_log
import config
from ErinaSearch import erina_dbread
from ErinaSearch import result_python_translation
from ErinaDB import erinadatabase
from ErinaCaches import erinacache, iqdb_api
from ErinaHash import erinahash

anilist_cache_path = env_information.erina_dir + '/ErinaCaches/AniList_Cache/'
erina_cache_path = env_information.erina_dir + '/ErinaCaches/Erina_Cache/'
erina_db_path = env_information.erina_dir + '/ErinaDB/ErinaDatabase/'
tracemoe_cache_path = env_information.erina_dir + '/ErinaCaches/TraceMoe_Cache/'
saucenao_cache_path = env_information.erina_dir + '/ErinaCaches/SauceNAO_Cache/'
iqdb_cache_path = env_information.erina_dir + '/ErinaCaches/IQDB_Cache/'
manami_db_path = env_information.erina_dir + '/ErinaDB/ManamiDB/'

def search_anime_by_anilist_id(anilist_id, anilist_priority=False):
    """
    Let you search through Erina's database and other database (Manami Projects' anime_offline_database and AniList API) with the AniList ID of the Anime!\n
    © Anime no Sekai - 2020
    Project Erina
    """
    erina_log.logsearch(f'Searching the anime by his AniList ID... ({str(anilist_id)})', search_type='anilistid', value=str(anilist_id))
    search_result = {}
    search_result['found_from_anilist_cache'] = False
    search_result['found_from_manami'] = False
    search_result['found_from_anilist_api'] = False
    if anilist_priority:
        erinacache.anilist_caching(anilist_id)
    if filecenter.exists(anilist_cache_path + str(anilist_id) + '.erina'):
        search_result['found_from_anilist_cache'] = True
        search_result['result'] = erina_dbread.read_anilist_cache_data(str(anilist_id) + '.erina')
    else:
        mapping_request = lifeeasy.request('https://relations.yuna.moe/api/ids?source=anilist&id=' + str(anilist_id), 'get')
        if mapping_request.status_code == 200:
            id_mapping = json.loads(mapping_request.text)
            iteration = 0
            for entry in erinadatabase.manami_database()['data']:
                iteration += 1
                if 'https://anilist.co/anime/' + str(anilist_id) in entry['sources']:
                    search_result['found_from_manami'] = True
                    search_result['result'] = entry
                    break
                elif id_mapping['anidb'] is not None and 'https://anidb.net/anime/' + str(id_mapping['anidb']) in entry['sources']:
                    search_result['found_from_manami'] = True
                    search_result['result'] = entry
                    break
                elif id_mapping['myanimelist'] is not None and 'https://myanimelist.net/anime/' + str(id_mapping['myanimelist']) in entry['sources']:
                    search_result['found_from_manami'] = True
                    search_result['result'] = entry
                    break
                elif id_mapping['kitsu'] is not None and 'https://kitsu.io/anime/' + str(id_mapping['kitsu']) in entry['sources']:
                    search_result['found_from_manami'] = True
                    search_result['result'] = entry
                    break
            erina_log.logdatabase(stattype='manamai_database_entry_lookup', value=iteration)
                
        else:
            iteration = 0
            for entry in erinadatabase.manami_database()['data']:
                iteration += 1
                if 'https://anilist.co/anime/' + str(anilist_id) in entry['sources']:
                    search_result['found_from_manami'] = True
                    search_result['result'] = entry
                    break
            erina_log.logdatabase(stattype='manamai_database_entry_lookup', value=iteration)
        if not search_result['found_from_manami']:
            search_result['found_from_anilist_api'] = True
            erinacache.anilist_caching(anilist_id)
            search_result['result'] = erina_dbread.read_anilist_cache_data(str(anilist_id) + '.erina')
    return search_result

def search_anime_by_title(title_string, anilist_priority=False):
    """
    Let you search through Erina's database and other database (Manami Projects' anime_offline_database and AniList API) with the title of the Anime!\n
    © Anime no Sekai - 2020
    Project Erina
    """
    erina_log.logsearch(f'Searching the anime by his title... ({title_string})', search_type='title', value=str(title_string))
    search_result = {}
    search_result['found_from_anilist_cache'] = False
    search_result['found_from_manami'] = False
    search_result['found_from_anilist_api'] = False
    for file in filecenter.files_in_dir(anilist_cache_path):
        anilist_result = erina_dbread.read_anilist_cache_data(file, silent_search=True)
        try:
            if anilist_result['title'] == title_string:
                search_result['found_from_anilist_cache'] = True
                search_result['result'] = anilist_result
                break
            elif anilist_result['title_romaji'] == title_string:
                search_result['found_from_anilist_cache'] = True
                search_result['result'] = anilist_result
                break
            elif anilist_result['title_english'] == title_string:
                search_result['found_from_anilist_cache'] = True
                search_result['result'] = anilist_result
                break
            elif anilist_result['title_native'] == title_string:
                search_result['found_from_anilist_cache'] = True
                search_result['result'] = anilist_result
                break
            else:
                if title_string in anilist_result['alternative_titles']:
                    search_result['found_from_anilist_cache'] = True
                    search_result['result'] = anilist_result
                    break
        except:
            continue
    if anilist_priority or config.anilist_priority:
        if not search_result['found_from_anilist_cache']: 
            new_cache_filename = erinacache.anilist_search_caching(title_string)
            if new_cache_filename: 
                search_result['result'] = erina_dbread.read_anilist_cache_data(new_cache_filename)
                search_result['found_from_anilist_cache'] = True
            if not search_result['found_from_anilist_cache']:
                iteration = 0
                for entry in erinadatabase.manami_database()['data']:
                    iteration += 1
                    if title_string in entry['synonyms']:
                        search_result['found_from_manami'] = True
                        search_result['result'] = entry
                        break
                    elif title_string == entry['title']:
                        search_result['found_from_manami'] = True
                        search_result['result'] = entry
                        break
                erina_log.logdatabase(stattype='manamai_database_entry_lookup', value=iteration)
    else:
        if not search_result['found_from_anilist_cache']:
            iteration = 0
            for entry in erinadatabase.manami_database()['data']:
                iteration += 1
                if title_string in entry['synonyms']:
                    search_result['found_from_manami'] = True
                    search_result['result'] = entry
                    break
                elif title_string == entry['title']:
                    search_result['found_from_manami'] = True
                    search_result['result'] = entry
                    break
            erina_log.logdatabase(stattype='manamai_database_entry_lookup', value=iteration)
            if not search_result['found_from_manami']:
                new_cache_filename = erinacache.anilist_search_caching(title_string)
                search_result['result'] = erina_dbread.read_anilist_cache_data(new_cache_filename)
    return search_result

def search_anime_by_hash(image_hash, image_url='', image_base64='', anilist_priority=False):
    """
    Let you search through Erina's database and other database (Manami Projects' anime_offline_database and AniList API) with the hash of an image/scene from an anime (average hash/aHash from the image_hash python module)\n
    © Anime no Sekai - 2020
    Project Erina
    """
    erina_log.logsearch(f'Searching the image by his hash... ({str(image_hash)})', search_type='hash', value=str(image_hash))
    search_result = {}
    search_result['erina_cache'] = False
    search_result['erina_database'] = False
    
    search_result['tracemoe_cache'] = False
    search_result['saucenao_cache'] = False
    search_result['iqdb_cache'] = False

    search_result['tracemoe_api'] = False
    search_result['saucenao_api'] = False
    search_result['iqdb_api'] = False
    
    search_result['low_similarity'] = False
    search_result['no_result'] = False

    def search_anime_in_erina_cache():
        result = {}
        if filecenter.isfile(erina_cache_path + str(image_hash) + '.erina'):
            result['erina_cache'] = True
            result['erina_cache_result'] = erina_dbread.read_erina_cache_data(str(image_hash) + '.erina')
            result['similarity'] = result['erina_cache_result']['similarity']
            result['erina_result'] = erina_dbread.read_erina_database_data(result['erina_cache_result']['database_path'])
            result['search_result'] = search_anime_by_anilist_id(result['erina_result']['anilist_id'], anilist_priority)
        return result

    def search_anime_in_erina_database():
        result = {}
        result['erina_database'] = False
        if config.erina_database_similarity_threshold > 98.4375:
            erina_log.logdatabase('', stattype='erina_database_access')
            iteration = 0
            for anime in filecenter.files_in_dir(erina_db_path):
                if anime == '.DS_Store':
                    continue
                elif anime == 'keep_this_dir.txt':
                    continue
                else:
                    for folder in filecenter.files_in_dir(erina_db_path + anime):
                        iteration += 1
                        if anime == '.DS_Store':
                            continue
                        if filecenter.isfile(erina_db_path + anime + '/' + folder + '/' + str(image_hash) + '.erina'):
                            result['erina_database'] = True
                            result['erina_result'] = erina_dbread.read_erina_database_data(anime + '/' + folder + '/' + str(image_hash) + '.erina')
                            result['similarity'] = 100
                            result['search_result'] = search_anime_by_anilist_id(result['erina_result']['anilist_id'], anilist_priority)
                            result['numer_of_file_searched'] = iteration
                            result['erina_path'] = erina_db_path + anime + '/' + folder + '/' + str(image_hash) + '.erina'
                            break
                    if result['erina_database']:
                        break
                if result['erina_database']:
                    break
            erina_log.logdatabase('', stattype='erina_database_entry_lookup', value=iteration)
        else:
            erina_log.logdatabase('', stattype='erina_database_access')
            iteration = 0
            distance_dict = {}
            for anime in filecenter.files_in_dir(erina_db_path):
                if anime == '.DS_Store':
                    continue
                elif anime == 'keep_this_dir.txt':
                    continue
                else:
                    for folder in filecenter.files_in_dir(erina_db_path + anime):
                        if folder == '.DS_Store':
                            continue
                        for file in filecenter.files_in_dir(erina_db_path + anime + '/' + folder):
                            iteration += 1
                            if file == '.DS_Store':
                                continue
                            current_hash_hex = file.replace('.erina', '')
                            current_hash = imagehash.hex_to_hash(current_hash_hex)
                            hamming_distance = current_hash - image_hash
                            if hamming_distance == 1:
                                result['similarity'] = (1 - (1 / 64)) * 100
                                result['numer_of_file_searched'] = iteration
                                result['erina_database'] = True
                                result['erina_result'] = erina_dbread.read_erina_database_data(anime + '/' + folder + '/' + file)
                                result['erina_database_path'] = anime + '/' + folder + '/' + file
                                result['search_result'] = search_anime_by_anilist_id(result['erina_result']['anilist_id'], anilist_priority)
                                break
                            else:
                                distance_dict[anime + '/' + folder + '/' + file] = hamming_distance
                    if result['erina_database']:
                        break
                if result['erina_database']:
                    break
            erina_log.logdatabase('', stattype='erina_database_entry_lookup', value=iteration)
            if not result['erina_database']:
                threshold = int((config.erina_database_similarity_threshold * 64)/100)
                similarities = list(range(2, len(list(range(threshold, 64)))))
                for distance in similarities:
                    for element in distance_dict:
                        iteration += 1
                        if distance_dict[element] == distance:
                            result['similarity'] = (1 - (distance / 64)) * 100
                            result['numer_of_file_searched'] = iteration
                            result['erina_database_path'] = element
                            result['erina_database'] = True
                            result['erina_result'] = erina_dbread.read_erina_database_data(element)
                            result['search_result'] = search_anime_by_anilist_id(result['erina_result']['anilist_id'], anilist_priority)
                            break
                    if result['erina_database']:
                        break
        if not result['erina_database']:
            return {}
        else:
            return result

    def search_anime_in_tracemoe_cache():
        result = {}
        result['tracemoe_cache'] = False
        if filecenter.isfile(tracemoe_cache_path + str(image_hash) + '.erina'):
            result['tracemoe_cache'] = True
            result['tracemoe_result'] = erina_dbread.read_tracemoe_cache_data(str(image_hash) + '.erina')
            if result['tracemoe_result']['error']:
                return {}
            """
            if float(result['tracemoe_result']['similarity']) < config.tracemoe_similarity_threshold:
                return {}
            """
            result['search_result'] = search_anime_by_anilist_id(result['tracemoe_result']['anilist_id'], anilist_priority)
            result['similarity'] = result['tracemoe_result']['similarity']
        if not result['tracemoe_cache']:
            return {}
        else:
            return result

    def search_anime_in_saucenao_cache():
        result = {}
        result['saucenao_cache'] = False
        result['search_result'] = {'error': 'no anime found'}
        result['is_anime'] = False
        if filecenter.isfile(saucenao_cache_path + str(image_hash) + '.erina'):
            result['saucenao_cache'] = True
            result['saucenao_result'] = erina_dbread.read_saucenao_cache_data(str(image_hash) + '.erina')
            if result['saucenao_result']['error']:
                return {}
            """
            if float(result['saucenao_result']['similarity']) < config.saucenao_similarity_threshold:
                return {}
            """
            result['is_anime'] = result['saucenao_result']['is_anime']
            if result['saucenao_result']['is_anime']:
                result['search_result'] = search_anime_by_title(result['saucenao_result']['title'])
            result['similarity'] = result['saucenao_result']['similarity']
        if not result['saucenao_cache']:
            return {}
        else:
            return result

    def search_anime_in_tracemoe_api():
        result = {}
        try:
            if image_url != '':
                if config.tracemoe_api_key == '':
                    trace_moe_request = lifeeasy.request('https://trace.moe/api/search?url=' + image_url, 'get')
                else:
                    trace_moe_request = lifeeasy.request('https://trace.moe/api/search?url=' + image_url + '&token=' + config.tracemoe_api_key, 'get')
                """
                #### TO ADD WHEN SAUCENAO IS SUPPORTED
                if float(json.loads(trace_moe_request.text)['docs'][0]['similarity']) < config.tracemoe_similarity_threshold:
                    return {}
                """
                erinacache.tracemoe_caching(str(image_hash), json.loads(trace_moe_request.text))
                result['tracemoe_result'] = erina_dbread.read_tracemoe_cache_data(str(image_hash) + '.erina')
                result['search_result'] = search_anime_by_anilist_id(result['tracemoe_result']['anilist_id'], anilist_priority)
                result['similarity'] = result['tracemoe_result']['similarity']
                result['tracemoe_api'] = True
            elif image_base64 != '':
                base64 = image_base64[2:]
                base64 = base64[:-1]
                if config.tracemoe_api_key == '':
                    trace_moe_request = lifeeasy.request(url='https://trace.moe/api/search', method='post', json_body={'image': base64})
                else:
                    trace_moe_request = lifeeasy.request(url='https://trace.moe/api/search?token=' + config.tracemoe_api_key, method='post', json_body={'image': base64})
                erinacache.tracemoe_caching(str(image_hash), json.loads(trace_moe_request.text))
                result['tracemoe_result'] = erina_dbread.read_tracemoe_cache_data(str(image_hash) + '.erina')
                result['search_result'] = search_anime_by_anilist_id(result['tracemoe_result']['anilist_id'], anilist_priority)
                result['similarity'] = result['tracemoe_result']['similarity']
                result['tracemoe_api'] = True
        except:
            return {}
        return result


    def search_anime_in_saucenao_api():
        result = {}
        result['is_anime'] = False
        result['is_manga'] = False
        result['search_result'] = {'error': 'no anime found'}
        if image_url != '':
            erinacache.saucenao_caching(str(image_hash), image_url=image_url)
        elif image_base64 != '':
            base64 = image_base64[2:]
            base64 = base64[:-1]
            erinacache.saucenao_caching(str(image_hash), file=BytesIO(b64decode(base64)))
        else:
            return {}
        result['saucenao_api'] = True
        result['saucenao_result'] = erina_dbread.read_saucenao_cache_data(str(image_hash) + '.erina')
        '''
        if float(result['saucenao_result']['similarity']) < config.saucenao_similarity_threshold:
            return {}
        '''
        result['is_anime'] = result['saucenao_result']['is_anime']
        if result['saucenao_result']['is_anime']:
            result['search_result'] = search_anime_by_title(result['saucenao_result']['title'])
        result['similarity'] = result['saucenao_result']['similarity']
        return result

    def search_anime_in_iqdb_api():
        result = {}
        result['iqdb_api'] = False
        if image_url != '':
            iqdb_result = iqdb_api.search_iqdb(str(image_hash), image_url=image_url)
        elif image_base64 != '':
            base64 = image_base64[2:]
            base64 = base64[:-1]
            iqdb_result = iqdb_api.search_iqdb(str(image_hash), file_io=BytesIO(b64decode(base64)))
        else:
            return {}

        if 'error' in iqdb_result:
            return {}
        result['iqdb_api'] = True
        result['iqdb_result'] = result_python_translation.verify_dict(iqdb_result)
        result['similarity'] = result['iqdb_result']['similarity']
        return result

    def search_anime_in_iqdb_cache():
        result = {}
        result['iqdb_cache'] = False
        if filecenter.isfile(iqdb_cache_path + str(image_hash) + '.erina'):
            result['iqdb_cache'] = True
            result['iqdb_result'] = erina_dbread.read_iqdb_cache_data(str(image_hash) + '.erina')
            if result['iqdb_result']['error']:
                return {}
            result['similarity'] = result['iqdb_result']['similarity']
        if not result['iqdb_cache']:
            return {}
        else:
            return result

    available_apis = ['tracemoe', 'saucenao', 'iqdb']

    erina_cache_result = search_anime_in_erina_cache()
    if erina_cache_result == {} or erina_cache_result['similarity'] < config.erina_database_similarity_threshold:

        erina_database_result = search_anime_in_erina_database()
        if erina_database_result == {} or erina_database_result['similarity'] < config.erina_database_similarity_threshold:

            tracemoe_cache_result = search_anime_in_tracemoe_cache()
            if tracemoe_cache_result == {} or tracemoe_cache_result['similarity'] < config.tracemoe_similarity_threshold:

                saucenao_cache_result = search_anime_in_saucenao_cache()
                if saucenao_cache_result == {} or saucenao_cache_result['similarity'] < config.saucenao_similarity_threshold:
                    
                    iqdb_cache_result = search_anime_in_iqdb_cache()
                    if iqdb_cache_result == {} or iqdb_cache_result['similarity'] < config.iqdb_similarity_threshold:
                        
                        tracemoe_api_result = search_anime_in_tracemoe_api()
                        if tracemoe_api_result == {} or tracemoe_api_result['similarity'] < config.tracemoe_similarity_threshold:
                            if tracemoe_api_result == {}:
                                available_apis.remove('tracemoe')
                            
                            saucenao_api_result = search_anime_in_saucenao_api()
                            if saucenao_api_result == {} or saucenao_api_result['similarity'] < config.saucenao_similarity_threshold:
                                if saucenao_api_result == {}:
                                    available_apis.remove('saucenao')
                            
                                iqdb_api_result = search_anime_in_iqdb_api()
                                if iqdb_api_result == {} or iqdb_api_result['similarity'] < config.iqdb_similarity_threshold:
                                    if iqdb_api_result == {}:
                                        available_apis.remove('iqdb')
                                            
                                    #### UNDER THE DEFINED SIMILARITY THRESHOLD
                                    search_result['low_similarity'] = True

                                    if 'tracemoe' in available_apis and 'saucenao' in available_apis and 'iqdb' in available_apis:
                                        if tracemoe_api_result['similarity'] < saucenao_api_result['similarity']:
                                            if saucenao_api_result['similarity'] < iqdb_api_result['similarity']:
                                                search_result['iqdb_api'] = iqdb_api_result['iqdb_api']
                                                search_result['iqdb_result'] = iqdb_api_result['iqdb_result']
                                                search_result['similarity'] = iqdb_api_result['similarity']
                                            else:
                                                search_result['saucenao_api'] = saucenao_api_result['saucenao_api']
                                                search_result['saucenao_result'] = saucenao_api_result['saucenao_result']
                                                search_result['search_result'] = saucenao_api_result['search_result']
                                                search_result['similarity'] = saucenao_api_result['similarity']
                                                search_result['is_anime'] = saucenao_api_result['is_anime']
                                        else:
                                            if tracemoe_api_result['similarity'] < iqdb_api_result['similarity']:
                                                search_result['iqdb_api'] = iqdb_api_result['iqdb_api']
                                                search_result['iqdb_result'] = iqdb_api_result['iqdb_result']
                                                search_result['similarity'] = iqdb_api_result['similarity']
                                            else:
                                                search_result['tracemoe_result'] = tracemoe_api_result['tracemoe_result']
                                                search_result['search_result'] = tracemoe_api_result['search_result']
                                                search_result['similarity'] = tracemoe_api_result['similarity']
                                                search_result['tracemoe_api'] = tracemoe_api_result['tracemoe_api']
                                
                                    elif 'tracemoe' in available_apis and 'saucenao' in available_apis:
                                        if tracemoe_api_result['similarity'] < saucenao_api_result['similarity']:
                                            search_result['saucenao_api'] = saucenao_api_result['saucenao_api']
                                            search_result['saucenao_result'] = saucenao_api_result['saucenao_result']
                                            search_result['search_result'] = saucenao_api_result['search_result']
                                            search_result['similarity'] = saucenao_api_result['similarity']
                                            search_result['is_anime'] = saucenao_api_result['is_anime']
                                        else:
                                            search_result['tracemoe_result'] = tracemoe_api_result['tracemoe_result']
                                            search_result['search_result'] = tracemoe_api_result['search_result']
                                            search_result['similarity'] = tracemoe_api_result['similarity']
                                            search_result['tracemoe_api'] = tracemoe_api_result['tracemoe_api']
                                    
                                    elif 'tracemoe' in available_apis and 'iqdb' in available_apis:
                                        if tracemoe_api_result['similarity'] < iqdb_api_result['similarity']:
                                            search_result['iqdb_api'] = iqdb_api_result['iqdb_api']
                                            search_result['iqdb_result'] = iqdb_api_result['iqdb_result']
                                            search_result['similarity'] = iqdb_api_result['similarity']
                                        else:
                                            search_result['tracemoe_result'] = tracemoe_api_result['tracemoe_result']
                                            search_result['search_result'] = tracemoe_api_result['search_result']
                                            search_result['similarity'] = tracemoe_api_result['similarity']
                                            search_result['tracemoe_api'] = tracemoe_api_result['tracemoe_api']
                                        
                                    elif 'saucenao' in available_apis and 'iqdb' in available_apis:
                                        if saucenao_api_result['similarity'] < iqdb_api_result['similarity']:
                                            search_result['iqdb_api'] = iqdb_api_result['iqdb_api']
                                            search_result['iqdb_result'] = iqdb_api_result['iqdb_result']
                                            search_result['similarity'] = iqdb_api_result['similarity']
                                        else:
                                            search_result['saucenao_api'] = saucenao_api_result['saucenao_api']
                                            search_result['saucenao_result'] = saucenao_api_result['saucenao_result']
                                            search_result['search_result'] = saucenao_api_result['search_result']
                                            search_result['similarity'] = saucenao_api_result['similarity']
                                            search_result['is_anime'] = saucenao_api_result['is_anime']
                                    
                                    elif 'tracemoe' in available_apis:
                                        search_result['tracemoe_result'] = tracemoe_api_result['tracemoe_result']
                                        search_result['search_result'] = tracemoe_api_result['search_result']
                                        search_result['similarity'] = tracemoe_api_result['similarity']
                                        search_result['tracemoe_api'] = tracemoe_api_result['tracemoe_api']

                                    elif 'saucenao' in available_apis:
                                        search_result['saucenao_api'] = saucenao_api_result['saucenao_api']
                                        search_result['saucenao_result'] = saucenao_api_result['saucenao_result']
                                        search_result['search_result'] = saucenao_api_result['search_result']
                                        search_result['similarity'] = saucenao_api_result['similarity']
                                        search_result['is_anime'] = saucenao_api_result['is_anime']

                                    elif 'iqdb' in available_apis:
                                        search_result['iqdb_api'] = iqdb_api_result['iqdb_api']
                                        search_result['iqdb_result'] = iqdb_api_result['iqdb_result']
                                        search_result['similarity'] = iqdb_api_result['similarity']
                                    
                                    #### IF NO RESULT ARE LEFT
                                    else:
                                        search_result['no_result'] = True

                                else:
                                    search_result['iqdb_api'] = iqdb_api_result['iqdb_api']
                                    search_result['iqdb_result'] = iqdb_api_result['iqdb_result']
                                    search_result['similarity'] = iqdb_api_result['similarity']
                            else:
                                search_result['saucenao_api'] = saucenao_api_result['saucenao_api']
                                search_result['saucenao_result'] = saucenao_api_result['saucenao_result']
                                search_result['search_result'] = saucenao_api_result['search_result']
                                search_result['similarity'] = saucenao_api_result['similarity']
                                search_result['is_anime'] = saucenao_api_result['is_anime']

                        else: # IF FOUND IN TRACEMOE API
                            search_result['tracemoe_result'] = tracemoe_api_result['tracemoe_result']
                            search_result['search_result'] = tracemoe_api_result['search_result']
                            search_result['similarity'] = tracemoe_api_result['similarity']
                            search_result['tracemoe_api'] = tracemoe_api_result['tracemoe_api']
                    
                    else: # IF FOUND IN IQDB CACHE
                        search_result['iqdb_cache'] = iqdb_cache_result['iqdb_cache']
                        search_result['iqdb_result'] = iqdb_cache_result['iqdb_result']
                        search_result['similarity'] = iqdb_cache_result['similarity']

                else: # IF FOUND IN SAUCE NAO CACHE
                    search_result['saucenao_cache'] = saucenao_cache_result['saucenao_cache']
                    search_result['saucenao_result'] = saucenao_cache_result['saucenao_result']
                    search_result['search_result'] = saucenao_cache_result['search_result']
                    search_result['similarity'] = saucenao_cache_result['similarity']
                    search_result['is_anime'] = saucenao_cache_result['is_anime']  
            
            else: # IF FOUND IN TRACEMOE CACHE
                search_result['tracemoe_cache'] = tracemoe_cache_result['tracemoe_cache']
                search_result['tracemoe_result'] = tracemoe_cache_result['tracemoe_result']
                search_result['search_result'] = tracemoe_cache_result['search_result']
                search_result['similarity'] = tracemoe_cache_result['similarity']
        
        else: # IF FOUND IN ERINA DATABASE
            search_result['erina_database'] = erina_database_result['erina_database']
            search_result['erina_result'] = erina_database_result['erina_result']
            search_result['similarity'] = erina_database_result['similarity']
            search_result['search_result'] = erina_database_result['search_result']
            search_result['numer_of_file_searched'] = erina_database_result['numer_of_file_searched']
            search_result['erina_path'] = erina_database_result['erina_path']
    
    else: # IF FOUND IN ERINA CACHE
        search_result['erina_cache'] = erina_cache_result['erina_cache']
        search_result['erina_cache_result'] = erina_cache_result['erina_cache_result']
        search_result['similarity'] = erina_cache_result['similarity']
        search_result['erina_result'] = erina_cache_result['erina_result']
        search_result['search_result'] = erina_cache_result['search_result']

    if search_result['erina_database']:
        erinacache.erina_caching(str(image_hash), search_result['erina_database_path'], search_result['similarity'])
    return search_result

def search_anime_by_image(image, anilist_priority=False):
    """
    Let you search through Erina's database and other database (Manami Projects' anime_offline_database and AniList API) with the given image/scene from an anime (average hash/aHash from the image_hash python module)\n
    © Anime no Sekai - 2020
    Project Erina
    """
    image_hash = erinahash.hash_image(image)
    search_result = search_anime_by_hash(image_hash=image_hash, anilist_priority=anilist_priority)
    return search_result

def search_anime_by_imageurl(image_url, anilist_priority=False):
    """
    Let you search through Erina's database and other database (Manami Projects' anime_offline_database and AniList API) with the given image/scene from an anime (average hash/aHash from the image_hash python module)\n
    © Anime no Sekai - 2020
    Project Erina
    """
    image_hash = erinahash.hash_image_from_url(image_url)
    search_result = search_anime_by_hash(image_hash=image_hash, image_url=image_url, anilist_priority=anilist_priority)
    return search_result

def search_anime_from_image_path(image_path, anilist_priority=False):
    """
    Let you search through Erina's database and other database (Manami Projects' anime_offline_database and AniList API) with the given image/scene from an anime (average hash/aHash from the image_hash python module)\n
    © Anime no Sekai - 2020
    Project Erina
    """
    image_hash = erinahash.hash_image_from_path(image_path)
    base64 = erinahash.base64_from_image(image_path)
    search_result = search_anime_by_hash(image_hash=image_hash, image_base64=str(base64), anilist_priority=anilist_priority)
    return search_result

def search_anime_by_base64(base64_data, anilist_priority=False):
    """
    Let you search through Erina's database and other database (Manami Projects' anime_offline_database and AniList API) with the given image/scene from an anime (average hash/aHash from the image_hash python module)\n
    © Anime no Sekai - 2020
    Project Erina
    """
    image_hash = erinahash.hash_image_from_base64(base64_data)
    base64 = base64_data
    search_result = search_anime_by_hash(image_hash=image_hash, image_base64=str(base64), anilist_priority=anilist_priority)
    return search_result
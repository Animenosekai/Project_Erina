"""
Caching API for the Erina Project

@author: Anime no Sekai
Erina Project - 2020
"""

import config
import erina_log
import env_information

from saucenao_api import SauceNao
from ErinaCaches.utils import anilist, tracemoe, saucenao, erina, Errors
from ErinaParser.utils import anilist_parser, tracemoe_parser, saucenao_parser, erina_parser


caches_dir_path = env_information.erina_dir + '/ErinaCaches/'
anilist_cache_path = caches_dir_path + 'AniList_Cache/'
erina_cache_path = caches_dir_path + 'Erina_Cache/'
tracemoe_cache_path = caches_dir_path + 'TraceMoe_Cache/'
saucenao_cache_path = caches_dir_path + 'SauceNAO_Cache/'

if config.saucenao_api_key != '':
    saucenao_api = SauceNao(api_key=config.saucenao_api_key, numres=1)
else:
    saucenao_api = SauceNao(numres=1)

def anilist_caching(anilist_id):
    '''
    Caches the anime associated with the given AniList ID (from AniList API)\n
    Project Erina
    © Anime no Sekai - 2020
    '''
    try:
        erina_log.logcaches(f'Caching {str(anilist_id)} from AniList API...', 'anilist', anilist_id)
        try:
            apiResponse = anilist.anilist_api(anilist_id)
        except:
            return Errors.CachingError("ANILIST_API_RESPONSE", f"An error occured while retrieving AniList API Data ({str(anilist_id)})")
        try:
            cache = anilist.anilist_json_to_cache(apiResponse)
        except:
            return Errors.CachingError("ERINA_CONVERSION", f"An error occured while converting AniList's API Data to a caching format ({str(anilist_id)})")
        try:
            with open(anilist_cache_path + cache['filename'], "w", encoding="utf-8") as newFile:
                newFile.read(cache["content"])
        except:
            return Errors.CachingError("FILE_WRITE", f"An error occured while writing out the cache data to a file ({str(anilist_id)})")
        return anilist_parser.AnilistCache(cache["content"])
    except:
        return Errors.CachingError("UNKOWN_ERROR", f"An unknown error occured while caching AniList API Data ({str(anilist_id)})")

def anilist_search_caching(query):
    '''
    Caches the first search result from the given query (from AniList API)\n
    Returns the new cache's filename\n
    Project Erina
    © Anime no Sekai - 2020
    '''
    try:
        erina_log.logcaches('Caching from AniList Search API...', 'anilist_search', str(query))
        try:
            apiResponse = anilist.anilist_api_search(query)
        except:
            return Errors.CachingError("ANILIST_SEARCH_API_RESPONSE", f"An error occured while retrieving AniList Search API Data ({str(query)})")
        try:
            cache = anilist.anilist_json_to_cache(apiResponse)
        except:
            return Errors.CachingError("ERINA_CONVERSION", f"An error occured while converting AniList's Search API Data to a caching format ({str(query)})")
        try:
            with open(anilist_cache_path + cache['filename'], "w", encoding="utf-8") as newFile:
                newFile.write(cache["content"])
        except:
            return Errors.CachingError("FILE_WRITE", f"An error occured while writing out the cache data to a file ({str(query)})")
        return anilist_parser.AnilistCache(cache["content"])
    except:
        return Errors.CachingError("UNKNOWN_ERROR", f"An unknown error occured while caching AniList Search API Data ({str(query)})")

def tracemoe_caching(image_hash, api_result):
    '''
    Caches the given Trace.moe API response\n
    Project Erina
    © Anime no Sekai - 2020
    '''
    try:
        erina_log.logcaches('Caching trace.moe data...', 'tracemoe', str(image_hash))
        try:
            cache = tracemoe.erina_from_json(api_result)
        except:
            return Errors.CachingError("ERINA_CONVERSION", f"An error occured while converting Trace.moe API Data to a caching format ({str(image_hash)})")
        try:
            with open(tracemoe_cache_path + str(image_hash) + '.erina', "r", encoding="utf-8") as newFile:
                newFile.write(cache)
        except:
            return Errors.CachingError("FILE_WRITE", f"An error occured while writing out the cache data to a file ({str(image_hash)})")
        return tracemoe_parser.TraceMOECache(cache)
    except:
        return Errors.CachingError("UNKNOWN_ERROR", f"An unknown error occured while caching trace.moe API Data ({str(image_hash)})")

def saucenao_caching(image_hash, image_url='', file=''):
    '''
    Caches the result from the given url\n
    Project Erina\n
    © Anime no Sekai - 2020
    '''
    try:
        erina_log.logcaches(f'Caching SauceNAO API data...', 'saucenao', str(image_hash))
        if image_url != '':
            try:
                api_results = saucenao_api.from_url(image_url)[0]
            except:
                return Errors.CachingError("SAUCENAO_API_RESPONSE", "An error occured while retrieving SauceNAO API Data")
        elif file != '':
            try:
                api_results = saucenao_api.from_file(file)[0]
            except:
                return Errors.CachingError("SAUCENAO_API_RESPONSE", "An error occured while retrieving SauceNAO API Data")
        else:
            return Errors.CachingError("NOTHING_PROVIDED", "No data got provided to the SauceNAO Caching API, we cannot proceed with the caching process with nothing...")
        try:
            cache = saucenao.erina_from_api(api_results)
        except:
            return Errors.CachingError("ERINA_CONVERSION", "An error occured while converting SauceNAO API Data to a caching format")
        try:
            with open(saucenao_cache_path + str(image_hash) + '.erina', "w", encoding="utf-8") as newFile:
                newFile.write(cache)
        except:
            return Errors.CachingError("FILE_WRITE", "An error occured while writing out the cache data to a file")
        return saucenao_parser.SauceNAOCache(cache)
    except:
        return Errors.CachingError("UNKNOWN", "An unknown error occured while caching SauceNAO API Data")

def erina_caching(image_hash, database_path, similarity):
    '''
    Caches an ErinaDatabase path according to the image_hash\n
    Project Erina
    © Anime no Sekai - 2020
    '''
    try:
        erina_log.logcaches('Caching Erina Database data...', 'erina', {'image_hash': str(image_hash), 'database_path': str(database_path), 'similarity': similarity})
        try:
            cache = erina.erina_from_data(str(image_hash), database_path, similarity)
        except:
            return Errors.CachingError("ERINA_CONVERSION", f"An error occured while converting Erina Database Data to a caching format ({str(database_path)})")
        try:
            with open(erina_cache_path + str(image_hash) + '.erina', "w", encoding="utf-8") as newFile:
                newFile.write(cache)
        except:
            return Errors.CachingError("FILE_WRITE", f"An error occured while writing out the cache data to a file {str(database_path)}")
        return erina_parser.ErinaCache(cache)
    except:
        return Errors.CachingError("UNKNOWN", "An unknown error occured while caching Erina Database Data")
"""
Caching API for the Erina Project

@author: Anime no Sekai
Erina Project - 2020
"""

from Erina.erina_log import log
from Erina import config
from Erina.env_information import erina_dir

import json

from safeIO import TextFile
import requests

from saucenao_api import SauceNao
from ErinaCaches.utils import anilist, tracemoe, saucenao, erina, Errors
from ErinaParser.utils import anilist_parser, tracemoe_parser, saucenao_parser, erina_parser

from Erina.erina_stats import StatsAppend
from Erina.erina_stats import external as ExternalStats

from sys import exc_info
import traceback


caches_dir_path = erina_dir + '/ErinaCaches/'
anilist_cache_path = caches_dir_path + 'AniList_Cache/'
erina_cache_path = caches_dir_path + 'Erina_Cache/'
tracemoe_cache_path = caches_dir_path + 'TraceMoe_Cache/'
saucenao_cache_path = caches_dir_path + 'SauceNAO_Cache/'

def anilist_caching(anilist_id):
    '''
    Caches the anime associated with the given AniList ID (from AniList API)\n
    Project Erina
    © Anime no Sekai - 2020
    '''
    try:
        log("ErinaCaches", f'Caching {str(anilist_id)} from AniList API...')
        try:
            apiResponse = anilist.anilist_api(anilist_id)
        except:
            return Errors.CachingError("ANILIST_API_RESPONSE", f"An error occured while retrieving AniList API Data ({str(anilist_id)})")
        if "errors" in apiResponse:
            if apiResponse["errors"][0]["status"] == 404:
                return Errors.CachingError("ANILIST_NOT_FOUND", str(anilist_id) + " has not been found")
            else:
                return Errors.CachingError("ANILIST_SERVER_ERROR", f"An error occured with the AniList API: {apiResponse['errors'][0]['message']}")
        try:
            cache = anilist.anilist_json_to_cache(apiResponse)
        except:
            return Errors.CachingError("ERINA_CONVERSION", f"An error occured while converting AniList's API Data to a caching format ({str(anilist_id)})")
        try:
            TextFile(anilist_cache_path + cache['filename'], blocking=False).write(cache["content"])
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
        log("ErinaCaches", f'Caching {str(query)} from AniList Search API...')
        try:
            apiResponse = anilist.anilist_api_search(query)
        except:
            return Errors.CachingError("ANILIST_SEARCH_API_RESPONSE", f"An error occured while retrieving AniList Search API Data ({str(query)})")
        if "errors" in apiResponse:
            if apiResponse["errors"][0]["status"] == 404:
                return Errors.CachingError("ANILIST_NOT_FOUND", str(query) + " has not been found")
            else:
                return Errors.CachingError("ANILIST_SERVER_ERROR", f"An error occured with the AniList API: {apiResponse['errors'][0]['message']}")
        try:
            cache = anilist.anilist_json_to_cache(apiResponse)
        except:
            return Errors.CachingError("ERINA_CONVERSION", f"An error occured while converting AniList's Search API Data to a caching format ({str(query)})")
        try:
            TextFile(anilist_cache_path + cache['filename'], blocking=False).write(cache["content"])
        except:
            return Errors.CachingError("FILE_WRITE", f"An error occured while writing out the cache data to a file ({str(query)})")
        return anilist_parser.AnilistCache(cache["content"])
    except:
        return Errors.CachingError("UNKNOWN_ERROR", f"An unknown error occured while caching AniList Search API Data ({str(query)})")

def tracemoe_caching(image_hash):
    '''
    Caches the given Trace.moe API response\n
    Project Erina
    © Anime no Sekai - 2020
    '''
    try:
        log("ErinaCaches", f'Caching {str(image_hash)} trace.moe data...')
        try:
            if image_hash.has_url is not None:
                if str(config.Caches.keys.tracemoe).replace(" ", "") in ["None", ""]:
                    requestResponse = json.loads(requests.get('https://trace.moe/api/search?url=' + image_hash.url).text)
                else:
                    requestResponse = json.loads(requests.get('https://trace.moe/api/search?url=' + image_hash.url + '&token=' + str(config.Caches.keys.tracemoe)).text)
            else:
                if str(config.Caches.keys.tracemoe).replace(" ", "") in ["None", ""]:
                    requestResponse = json.loads(requests.post('https://trace.moe/api/search', json={'image': image_hash.base64}))
                else:
                    requestResponse = json.loads(requests.post('https://trace.moe/api/search?token=' + str(config.Caches.keys.tracemoe), json={'image': image_hash.base64}))
        except:
            return Errors.CachingError("TRACEMOE_API_RESPONSE", "An error occured while retrieving information from the trace.moe API")
        
        StatsAppend(ExternalStats.tracemoeAPICalls)

        try:
            cache = tracemoe.erina_from_json(requestResponse)
        except:
            print(exc_info()[0])
            print(exc_info()[1])
            print(traceback.print_exception(*exc_info()))
            return Errors.CachingError("ERINA_CONVERSION", f"An error occured while converting trace.moe API Data to a caching format ({str(image_hash)})")
        try:
            TextFile(tracemoe_cache_path + str(image_hash) + '.erina', blocking=False).write(cache)
        except:
            return Errors.CachingError("FILE_WRITE", f"An error occured while writing out the cache data to a file ({str(image_hash)})")
        return tracemoe_parser.TraceMOECache(cache)
    except:
        return Errors.CachingError("UNKNOWN_ERROR", f"An unknown error occured while caching trace.moe API Data ({str(image_hash)})")

def saucenao_caching(image_hash):
    '''
    Caches the result from the given url\n
    Project Erina\n
    © Anime no Sekai - 2020
    '''
    try:
        log("ErinaCaches", f"Caching {str(image_hash)} SauceNAO data...")
        if str(config.Caches.keys.saucenao).replace(" ", "") not in ["None", ""]:
            saucenao_api = SauceNao(api_key=config.Caches.keys.saucenao, numres=1)
        else:
            saucenao_api = SauceNao(numres=1)
        if image_hash.has_url:
            try:
                api_results = saucenao_api.from_url(image_hash.url)[0]
            except:
                return Errors.CachingError("SAUCENAO_API_RESPONSE", "An error occured while retrieving SauceNAO API Data")
        else:
            try:
                api_results = saucenao_api.from_file(image_hash.ImageIO)[0]
            except:
                return Errors.CachingError("SAUCENAO_API_RESPONSE", "An error occured while retrieving SauceNAO API Data")
        
        StatsAppend(ExternalStats.saucenaoAPICalls)

        try:
            cache = saucenao.erina_from_api(api_results)
        except:
            return Errors.CachingError("ERINA_CONVERSION", "An error occured while converting SauceNAO API Data to a caching format")
        try:
            TextFile(saucenao_cache_path + str(image_hash) + '.erina', blocking=False).write(cache)
        except:
            return Errors.CachingError("FILE_WRITE", "An error occured while writing out the cache data to a file")
        return saucenao_parser.SauceNAOCache(cache)
    except:
        return Errors.CachingError("UNKNOWN", "An unknown error occured while caching SauceNAO API Data")

def erina_caching(image_hash, database_path, similarity, anilist_id):
    '''
    Caches an ErinaDatabase path according to the image_hash\n
    Project Erina
    © Anime no Sekai - 2020
    '''
    try:
        log("ErinaCaches", f'Caching {str(image_hash)} Erina Database data...')
        try:
            cache = erina.erina_from_data(str(image_hash), database_path, similarity, anilist_id)
        except:
            return Errors.CachingError("ERINA_CONVERSION", f"An error occured while converting Erina Database Data to a caching format ({str(database_path)})")
        try:
            TextFile(erina_cache_path + str(image_hash) + '.erina', blocking=False).write(cache)
        except:
            return Errors.CachingError("FILE_WRITE", f"An error occured while writing out the cache data to a file {str(database_path)}")
        return erina_parser.ErinaCache(cache)
    except:
        return Errors.CachingError("UNKNOWN", "An unknown error occured while caching Erina Database Data")



def iqdb_caching(a):
    return Errors.CachingError("NOT_IMPLEMENTED", "Not implemented yet.")
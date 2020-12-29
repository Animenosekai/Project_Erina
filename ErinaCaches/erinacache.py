"""
Caching API for the Erina Project

@author: Anime no Sekai
Erina Project - 2020
"""

from ErinaParser.utils import iqdb_parser
from bs4 import BeautifulSoup
from Erina.erina_log import log
from Erina import config
from Erina.env_information import erina_dir

import json

from safeIO import TextFile
import requests

from saucenao_api import SauceNao
from ErinaCaches.utils import anilist, tracemoe, saucenao, erina
from Erina.Errors import CachingError
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
            return CachingError("ANILIST_API_RESPONSE", f"An error occured while retrieving AniList API Data ({str(anilist_id)})")
        if "errors" in apiResponse:
            if apiResponse["errors"][0]["status"] == 404:
                return CachingError("ANILIST_NOT_FOUND", str(anilist_id) + " has not been found")
            else:
                return CachingError("ANILIST_SERVER_ERROR", f"An error occured with the AniList API: {apiResponse['errors'][0]['message']}")
        try:
            cache = anilist.anilist_json_to_cache(apiResponse)
        except:
            return CachingError("ERINA_CONVERSION", f"An error occured while converting AniList's API Data to a caching format ({str(anilist_id)})")
        try:
            TextFile(anilist_cache_path + cache['filename'], blocking=False).write(cache["content"])
        except:
            return CachingError("FILE_WRITE", f"An error occured while writing out the cache data to a file ({str(anilist_id)})")
        return anilist_parser.AnilistCache(cache["content"])
    except:
        return CachingError("UNKOWN_ERROR", f"An unknown error occured while caching AniList API Data ({str(anilist_id)})")

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
            return CachingError("ANILIST_SEARCH_API_RESPONSE", f"An error occured while retrieving AniList Search API Data ({str(query)})")
        if "errors" in apiResponse:
            if apiResponse["errors"][0]["status"] == 404:
                return CachingError("ANILIST_NOT_FOUND", str(query) + " has not been found")
            else:
                return CachingError("ANILIST_SERVER_ERROR", f"An error occured with the AniList API: {apiResponse['errors'][0]['message']}")
        try:
            cache = anilist.anilist_json_to_cache(apiResponse)
        except:
            return CachingError("ERINA_CONVERSION", f"An error occured while converting AniList's Search API Data to a caching format ({str(query)})")
        try:
            TextFile(anilist_cache_path + cache['filename'], blocking=False).write(cache["content"])
        except:
            return CachingError("FILE_WRITE", f"An error occured while writing out the cache data to a file ({str(query)})")
        return anilist_parser.AnilistCache(cache["content"])
    except:
        return CachingError("UNKNOWN_ERROR", f"An unknown error occured while caching AniList Search API Data ({str(query)})")

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
            return CachingError("TRACEMOE_API_RESPONSE", "An error occured while retrieving information from the trace.moe API")
        
        StatsAppend(ExternalStats.tracemoeAPICalls)

        try:
            cache = tracemoe.erina_from_json(requestResponse)
        except:
            print(exc_info()[0])
            print(exc_info()[1])
            print(traceback.print_exception(*exc_info()))
            return CachingError("ERINA_CONVERSION", f"An error occured while converting trace.moe API Data to a caching format ({str(image_hash)})")
        try:
            TextFile(tracemoe_cache_path + str(image_hash) + '.erina', blocking=False).write(cache)
        except:
            return CachingError("FILE_WRITE", f"An error occured while writing out the cache data to a file ({str(image_hash)})")
        return tracemoe_parser.TraceMOECache(cache)
    except:
        return CachingError("UNKNOWN_ERROR", f"An unknown error occured while caching trace.moe API Data ({str(image_hash)})")

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
                return CachingError("SAUCENAO_API_RESPONSE", "An error occured while retrieving SauceNAO API Data")
        else:
            try:
                api_results = saucenao_api.from_file(image_hash.ImageIO)[0]
            except:
                return CachingError("SAUCENAO_API_RESPONSE", "An error occured while retrieving SauceNAO API Data")
        
        StatsAppend(ExternalStats.saucenaoAPICalls)

        try:
            cache = saucenao.erina_from_api(api_results)
        except:
            traceback.print_exc()
            return CachingError("ERINA_CONVERSION", "An error occured while converting SauceNAO API Data to a caching format")
        try:
            TextFile(saucenao_cache_path + str(image_hash) + '.erina', blocking=False).write(cache)
        except:
            return CachingError("FILE_WRITE", "An error occured while writing out the cache data to a file")
        return saucenao_parser.SauceNAOCache(cache)
    except:
        return CachingError("UNKNOWN", "An unknown error occured while caching SauceNAO API Data")

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
            return CachingError("ERINA_CONVERSION", f"An error occured while converting Erina Database Data to a caching format ({str(database_path)})")
        try:
            TextFile(erina_cache_path + str(image_hash) + '.erina', blocking=False).write(cache)
        except:
            return CachingError("FILE_WRITE", f"An error occured while writing out the cache data to a file {str(database_path)}")
        return erina_parser.ErinaCache(cache)
    except:
        return CachingError("UNKNOWN", "An unknown error occured while caching Erina Database Data")



def iqdb_caching(image_hash):
    """
    Searches and caches IQDB for anime/manga related images.

    Erina Project - 2020\n
    © Anime no Sekai
    """
    try:
        log("ErinaCaches", 'Searching for IQDB Data...')
        
        ### If a file is given, send the file to iqdb.
        try:
            if image_hash.has_url:
                IQDBresponse = requests.get(f'https://iqdb.org/?url={image_hash.url}')
                StatsAppend(ExternalStats.iqdbCalls, "New Call")
            else:
                IQDBresponse = requests.post('https://iqdb.org/', files={'file': ('image_to_search',  image_hash.ImageIO) })
                StatsAppend(ExternalStats.iqdbCalls, "New Call")
        except:
            return CachingError("IQDB_RESPONSE", "An error occured while retrieving IQDB Data")

        ### If the image format is not supported by IQDB
        if 'Not an image or image format not supported' in IQDBresponse.text:
            return CachingError("IQDB_FORMAT_NOT_SUPPORTED", "The given image's format is not supported by IQDB")


    ###### IQDB SCRAPING
        try:
            iqdb = BeautifulSoup(IQDBresponse.text, 'html.parser')

        ##### Search for the IQDB result
            try:
                tables = iqdb.find_all('table')
                search_result = tables[1].findChildren("th")[0].get_text()
            except:
                return CachingError("IQDB_CLIENT_ERROR", f"An error occured while searching for the results: {exc_info()[0]}")

        ##### Verify if the result is relevant or not
            iqdb_tags = []
            if search_result == 'No relevant matches':
                return CachingError("IQDB_NO_RELEVANT_MATCH", "No relevant matches was found with IQDB")
            else:
                try:
                    ### Getting the tags from IQDB
                    alt_string = tables[1].findChildren("img")[0]['alt']
                    iqdb_tags = alt_string.split('Tags: ')[1].split(' ')
                except:
                    iqdb_tags = []
            
            #### Getting the Database URL from IQDB
            try:
                url = tables[1].find_all('td', attrs={'class': 'image'})[0].findChildren('a')[0]['href']
                url = 'https://' + url.split('//')[1]
            except:
                url = 'No URL'

            #### Getting the result image size
            try:
                size = tables[1].find_all('tr')[3].get_text().split(' [')[0]
            except:
                size = 'Unknown'

            #### Getting the image rating (if it is NSFW or not) 
            if tables[1].find_all('tr')[3].get_text().split()[1].replace('[', '').replace(']', '').replace(' ', '') == 'Safe':
                is_safe = True
            else:
                is_safe = False

            #### Getting the similarity
            try:
                similarity = tables[1].find_all('tr')[4].get_text().replace('% similarity', '')
            except:
                similarity = '0'


        ############ FUNCTION DEFINITION FOR RESULTS SCRAPING
            database = "Unknown"
            if url.find('gelbooru.') != -1:
                database = 'Gelbooru'
            
            elif url.find('danbooru.') != -1:
                database = 'Danbooru'

            elif url.find('zerochan.') != -1:
                database = 'Zerochan'

            elif url.find('konachan.') != -1:
                database = 'Konachan'

            elif url.find('yande.re') != -1:
                database = 'Yande.re'

            elif url.find('anime-pictures.') != -1:
                database = 'Anime-Pictures'

            elif url.find('e-shuushuu') != -1:
                database = 'E-Shuushuu'
        except:
            return CachingError("IQDB_PARSING", "An error occured while parsing the data from IQDB")

        try:
            #### Adding the results to the main result variable
            newCacheFile = TextFile(erina_dir + "/ErinaCaches/IQDB_Cache/" + str(image_hash) + ".erina")
            newCacheFile.append("   --- IQDB CACHE ---   \n")
            newCacheFile.append('\n')
            
            newCacheFile.append('IQDB Tags: ' + ":::".join(iqdb_tags) + "\n")
            newCacheFile.append('URL: ' + str(url) + "\n")
            newCacheFile.append('Size: ' + str(size)  + "\n")
            newCacheFile.append('isSafe: ' + str(is_safe) + "\n")
            newCacheFile.append('Similarity: ' + str(similarity) + "\n")
            newCacheFile.append('Database: ' + str(database) + "\n")
            return iqdb_parser.IQDBCache(newCacheFile.read())
        except:
            return CachingError("FILE_WRITE", f"An error occured while writing out the cache data to a file")
    except:
        return CachingError("UNKNOWN", "An unknown error occured while caching IQDB Data")
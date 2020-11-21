import os
import operator

from base64 import b64decode
from io import BytesIO

import numpy

import config
from env_information import erina_dir
from ErinaParser import parser
from ErinaSearch.utils import anilist_id_search
from ErinaSearch.utils import title_search
from ErinaCaches import erinacache
from ErinaParser.utils.tracemoe_parser import TraceMOECache
from ErinaParser.utils.saucenao_parser import SauceNAOCache
from ErinaParser.utils.iqdb_parser import IQDBCache
from ErinaParser.utils.Errors import ParserError
from ErinaCaches.utils.Errors import CachingError

class ImageSearchResult():
    def __init__(self, detectionResut, similarity, animeResult, low_similarity=False) -> None:
        self.detectionResult = detectionResut
        self.simialrity = similarity
        self.animeResult = animeResult
        self.low_similarity = low_similarity
    
    def as_dict(self):
        return {
            "detectionResult": self.detectionResult.as_dict(),
            "similarity": self.simialrity,
            "animeResult": self.animeResult.as_dict(),
            "lowSimilarity": self.low_similarity
        }

def hamming_distance(hash1, hash2):
    """
    From the imagehash library
    """
    def hex_to_hash(hexstr):
        hash_size = int(numpy.sqrt(len(hexstr)*4))
        binary_array = '{:0>{width}b}'.format(int(hexstr, 16), width = hash_size * hash_size)
        bit_rows = [binary_array[i:i+hash_size] for i in range(0, len(binary_array), hash_size)]
        return numpy.array([[bool(int(d)) for d in row] for row in bit_rows])
    return numpy.count_nonzero(hex_to_hash(hash1).flatten() != hex_to_hash(hash2).flatten())


anilist_cache_path = erina_dir + '/ErinaCaches/AniList_Cache/'
erina_cache_path = erina_dir + '/ErinaCaches/Erina_Cache/'
erina_db_path = erina_dir + '/ErinaDB/ErinaDatabase/'
tracemoe_cache_path = erina_dir + '/ErinaCaches/TraceMoe_Cache/'
saucenao_cache_path = erina_dir + '/ErinaCaches/SauceNAO_Cache/'
iqdb_cache_path = erina_dir + '/ErinaCaches/IQDB_Cache/'
manami_db_path = erina_dir + '/ErinaDB/ManamiDB/'



def search_anime_by_hash(image_hash, image_url='', image_base64='', anilist_priority=False):
    """
    Let you search through Erina's database and other database (Manami Projects' anime_offline_database and AniList API) with the hash of an image/scene from an anime (average hash/aHash from the image_hash python module)\n
    © Anime no Sekai - 2020
    Project Erina
    """
    erina_log.logsearch(f'Searching the image by his hash... ({str(image_hash)})', search_type='hash', value=str(image_hash))
    
    def search_anime_in_erina_database():
        if config.erina_database_similarity_threshold > 98.4375:
            erina_log.logdatabase('', stattype='erina_database_access')
            for anime in os.listdir(erina_db_path):
                if anime in ['.DS_Store', ".gitkeep"]:
                    continue
                else:
                    for folder in os.listdir(erina_db_path + anime):
                        if anime == '.DS_Store':
                            continue
                        if os.path.isfile(erina_db_path + anime + '/' + folder + '/' + str(image_hash) + '.erina'):
                            return parser.ErinaFile("erina_database", anime + '/' + folder + '/' + str(image_hash) + '.erina').content, 100, anime + '/' + folder + '/' + str(image_hash) + '.erina'
            erina_log.logdatabase('', stattype='erina_database_entry_lookup', value=iteration)
        else:
            erina_log.logdatabase('', stattype='erina_database_access')
            distance_dict = {}
            for anime in os.listdir(erina_db_path):
                if anime in ['.DS_Store', ".gitkeep"]:
                    continue
                else:
                    for folder in os.listdir(erina_db_path + anime):
                        if folder == '.DS_Store':
                            continue
                        for file in os.listdir(erina_db_path + anime + '/' + folder):
                            if file == '.DS_Store':
                                continue
                            distance = hamming_distance(file.replace('.erina', ''), str(image_hash))
                            if distance == 1:
                                return parser.ErinaFile("erina_database", anime + '/' + folder + '/' + file).content, (1 - (1 / 64)) * 100, anime + '/' + folder + '/' + str(image_hash) + '.erina'
                            else:
                                distance_dict[anime + '/' + folder + '/' + file] = distance
            erina_log.logdatabase('', stattype='erina_database_entry_lookup', value=iteration)
            threshold = int((config.erina_database_similarity_threshold * 64)/100)
            similarities = list(range(2, len(list(range(threshold, 64)))))
            for distance in similarities:
                for element in distance_dict:
                    if distance_dict[element] == distance:
                        return parser.ErinaFile("erina_database", element).content, (1 - (distance / 64)) * 100, anime + '/' + folder + '/' + str(image_hash) + '.erina'
        return None, None, None


    ##########################
    #     CACHE SEARCHING    #
    ##########################

    def search_anime_in_erina_cache():
        if os.path.isfile(f"{str(erina_dir)}/{str(image_hash)}.erina"):
            return parser.ErinaFile("erina_cache", f"{str(image_hash)}.erina").content
        return None

    def search_anime_in_tracemoe_cache():
        if os.path.isfile(tracemoe_cache_path + str(image_hash) + '.erina'):
            return parser.ErinaFile("tracemoe_cache", str(image_hash) + '.erina').content
        return None

    def search_anime_in_saucenao_cache():
        if os.path.isfile(saucenao_cache_path + str(image_hash) + '.erina'):
            return parser.ErinaFile("saucenao_cache", str(image_hash) + ".erina").content
        return None

    def search_anime_in_iqdb_cache():
        if os.path.isfile(iqdb_cache_path + str(image_hash) + '.erina'):
            return parser.ErinaFile("iqdb_cache", str(image_hash) + '.erina').content
        return None

    ##########################
    #      API SEARCHING     #
    ##########################

    def search_anime_in_tracemoe_api():
        if image_url != '':
            return erinacache.tracemoe_caching(str(image_hash), image_url=image_url)
        elif image_base64 != '':
            return erinacache.tracemoe_caching(str(image_hash), base64=image_base64)
        return erinacache.tracemoe_caching(str(image_hash))

    def search_anime_in_saucenao_api():
        if image_url != '':
            return erinacache.saucenao_caching(str(image_hash), image_url=image_url)
        elif image_base64 != '':
            return erinacache.saucenao_caching(str(image_hash), file=BytesIO(b64decode(image_base64)))
        return erinacache.saucenao_caching(str(image_hash))

    def search_anime_in_iqdb_api():
        if image_url != '':
            return iqdb_api.search_iqdb(str(image_hash), image_url=image_url)
        elif image_base64 != '':
            return iqdb_api.search_iqdb(str(image_hash), file_io=BytesIO(b64decode(image_base64)))
        return iqdb_api.search()

    similaritiesDict = {}

    erina_cache_result = search_anime_in_erina_cache()
    if erina_cache_result is None or isinstance(erina_cache_result, ParserError) or erina_cache_result.similarity < config.erina_database_similarity_threshold:

        erina_database_result, erina_database_similarity, erina_database_path = search_anime_in_erina_database()
        if erina_database_result is None or isinstance(erina_database_result, ParserError) or erina_database_similarity < config.erina_database_similarity_threshold:
            
            tracemoe_cache_result = search_anime_in_tracemoe_cache()
            if tracemoe_cache_result is None or isinstance(tracemoe_cache_result, ParserError) or tracemoe_cache_result.similarity < config.tracemoe_similarity_threshold:

                saucenao_cache_result = search_anime_in_saucenao_cache()
                if saucenao_cache_result is None or isinstance(saucenao_cache_result, ParserError) or saucenao_cache_result.similarity < config.saucenao_similarity_threshold:
                    
                    iqdb_cache_result = search_anime_in_iqdb_cache()
                    if iqdb_cache_result is None or isinstance(iqdb_cache_result, ParserError) or iqdb_cache_result.similarity < config.iqdb_similarity_threshold:
                        
                        tracemoe_api_result = search_anime_in_tracemoe_api()
                        if isinstance(tracemoe_api_result, CachingError) or tracemoe_api_result.similarity < config.tracemoe_similarity_threshold:
                            if not isinstance(tracemoe_api_result, CachingError) and tracemoe_api_result.similarity is not None:
                                similaritiesDict[tracemoe_api_result] = tracemoe_api_result.similarity
            
                            saucenao_api_result = search_anime_in_saucenao_api()
                            if isinstance(saucenao_api_result, CachingError) or saucenao_api_result.similarity < config.saucenao_similarity_threshold:
                                if not isinstance(saucenao_api_result, CachingError) and saucenao_api_result.similarity is not None:
                                    similaritiesDict[saucenao_api_result] = saucenao_api_result.similarity

                                iqdb_api_result = search_anime_in_iqdb_api()
                                if isinstance(iqdb_api_result, CachingError) or iqdb_api_result.similarity < config.iqdb_similarity_threshold:
                                    if not isinstance(iqdb_api_result, CachingError) and iqdb_api_result.similarity is not None:
                                        similaritiesDict[iqdb_api_result] = iqdb_api_result.similarity

                                    #### UNDER THE DEFINED SIMILARITY THRESHOLD

                                    bestResult = max(similaritiesDict.iteritems(), key=operator.itemgetter(1))[0]
                                    
                                    if isinstance(bestResult, TraceMOECache):
                                        return ImageSearchResult(tracemoe_cache_result, tracemoe_cache_result.similarity, anilist_id_search(tracemoe_cache_result.anilist_id), low_similarity=True)
                                    elif isinstance(bestResult, SauceNAOCache):
                                        return ImageSearchResult(saucenao_cache_result, saucenao_cache_result.similarity, (title_search(saucenao_cache_result.title) if saucenao_cache_result.is_anime else None), low_similarity=True)
                                    elif isinstance(bestResult, IQDBCache):
                                        return ImageSearchResult(iqdb_cache_result, iqdb_cache_result.similarity, None, low_similarity=True)
                                    else: #### IF NO RESULT ARE LEFT
                                        return None

                                else: # IF FOUND IN IQDB API
                                    return ImageSearchResult(iqdb_api_result, iqdb_api_result.similarity, None)
                                    
                            else: # IF FOUND IN SAUCENAO API
                                return ImageSearchResult(saucenao_api_result, saucenao_api_result.similarity, (title_search(saucenao_api_result.title) if saucenao_api_result.is_anime else None))

                        else: # IF FOUND IN TRACEMOE API
                            return ImageSearchResult(tracemoe_api_result, tracemoe_api_result.similarity, anilist_id_search(tracemoe_api_result.anilist_id))
                    
                    else: # IF FOUND IN IQDB CACHE
                        return ImageSearchResult(iqdb_cache_result, iqdb_cache_result.similarity, None)

                else: # IF FOUND IN SAUCE NAO CACHE
                    if saucenao_cache_result.is_anime:
                        return ImageSearchResult(saucenao_cache_result, saucenao_cache_result.similarity, (title_search(saucenao_cache_result.title) if saucenao_cache_result.is_anime else None))
            
            else: # IF FOUND IN TRACEMOE CACHE
                return ImageSearchResult(tracemoe_cache_result, tracemoe_cache_result.similarity, anilist_id_search(tracemoe_cache_result.anilist_id))
        
        else: # IF FOUND IN ERINA DATABASE
            erinacache.erina_caching(str(image_hash), erina_database_path, erina_database_similarity, erina_database_result.anilist_id)
            return ImageSearchResult(erina_database_result, erina_database_similarity, anilist_id_search(erina_database_result.anilist_id))
            
    else: # IF FOUND IN ERINA CACHE
        return ImageSearchResult(parser.ErinaFile("erina_database", erina_cache_result.path), erina_cache_result.similarity, anilist_id_search(erina_cache_result.anilist_id))

    return None
from ErinaSearch.utils.Errors import SearchingError
import os
import operator

import numpy

from Erina.config import Search as SearchConfig
from Erina.env_information import erina_dir
from ErinaParser import parser
from ErinaSearch.utils import anilist_id_search
from ErinaSearch.utils import title_search
from ErinaCaches import erinacache
from ErinaParser.utils.tracemoe_parser import TraceMOECache
from ErinaParser.utils.saucenao_parser import SauceNAOCache
from ErinaParser.utils.iqdb_parser import IQDBCache
from ErinaParser.utils.Errors import ParserError
from ErinaCaches.utils.Errors import CachingError
from ErinaHash.utils.Errors import HashingError

from Erina.erina_stats import db as DatabaseStats
from Erina.erina_stats import StatsAppend
class ImageSearchResult():
    def __init__(self, detectionResut, similarity, animeResult, low_similarity=False) -> None:
        self.detectionResult = detectionResut
        self.similarity = similarity
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



def search_anime_by_hash(image_hash):
    """
    Let you search through Erina's database and other database (Manami Projects' anime_offline_database and AniList API) with the hash of an image/scene from an anime (average hash/aHash from the image_hash python module)\n
    © Anime no Sekai - 2020
    Project Erina
    """
    if isinstance(image_hash, HashingError): # If there is no error
        return image_hash

    ##########################
    #     DATABASE SEARCH    #
    ##########################

    def search_anime_in_erina_database():
        if SearchConfig.thresholds.erina_similarity > 98.4375:
            for anime in os.listdir(erina_db_path):
                if anime in ['.DS_Store', ".gitkeep"]:
                    continue
                else:
                    for folder in os.listdir(erina_db_path + anime):
                        if anime == '.DS_Store':
                            continue
                        if os.path.isfile(erina_db_path + anime + '/' + folder + '/' + str(image_hash) + '.erina'):
                            StatsAppend(DatabaseStats.erinaDatabaseLookups, 1)
                            return parser.ErinaFile("erina_database", anime + '/' + folder + '/' + str(image_hash) + '.erina').content, 100, anime + '/' + folder + '/' + str(image_hash) + '.erina'
        else:
            
            distance_dict = {}
            iteration = 0
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
                            iteration += 1
                            distance = hamming_distance(file.replace('.erina', ''), str(image_hash))
                            if distance == 1:
                                return parser.ErinaFile("erina_database", anime + '/' + folder + '/' + file).content, (1 - (1 / 64)) * 100, anime + '/' + folder + '/' + str(image_hash) + '.erina'
                            else:
                                distance_dict[anime + '/' + folder + '/' + file] = distance
            StatsAppend(DatabaseStats.erinaDatabaseLookups, iteration)
            threshold = int((SearchConfig.thresholds.erina_similarity * 64)/100)
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
    #        SEARCHING       #
    ##########################
        
    similaritiesDict = {}
    erina_cache_result = search_anime_in_erina_cache()
    if erina_cache_result is None or isinstance(erina_cache_result, ParserError) or erina_cache_result.similarity < SearchConfig.thresholds.erina_similarity:

        erina_database_result, erina_database_similarity, erina_database_path = search_anime_in_erina_database()
        if erina_database_result is None or isinstance(erina_database_result, ParserError) or erina_database_similarity < SearchConfig.thresholds.erina_similarity:
            
            tracemoe_cache_result = search_anime_in_tracemoe_cache()
            if tracemoe_cache_result is None or isinstance(tracemoe_cache_result, ParserError) or tracemoe_cache_result.similarity < SearchConfig.thresholds.tracemoe_similarity:

                saucenao_cache_result = search_anime_in_saucenao_cache()
                if saucenao_cache_result is None or isinstance(saucenao_cache_result, ParserError) or saucenao_cache_result.similarity < SearchConfig.thresholds.saucenao_similarity:
                    
                    iqdb_cache_result = search_anime_in_iqdb_cache()
                    if iqdb_cache_result is None or isinstance(iqdb_cache_result, ParserError) or iqdb_cache_result.similarity < SearchConfig.thresholds.iqdb_similarity:
                        
                        tracemoe_api_result = erinacache.tracemoe_caching(image_hash)
                        if isinstance(tracemoe_api_result, CachingError) or tracemoe_api_result.similarity < SearchConfig.thresholds.tracemoe_similarity:
                            if not isinstance(tracemoe_api_result, CachingError) and tracemoe_api_result.similarity is not None:
                                similaritiesDict[tracemoe_api_result] = tracemoe_api_result.similarity
            
                            saucenao_api_result = erinacache.saucenao_caching(image_hash)
                            if isinstance(saucenao_api_result, CachingError) or saucenao_api_result.similarity < SearchConfig.thresholds.saucenao_similarity:
                                if not isinstance(saucenao_api_result, CachingError) and saucenao_api_result.similarity is not None:
                                    similaritiesDict[saucenao_api_result] = saucenao_api_result.similarity

                                iqdb_api_result = erinacache.iqdb_caching(image_hash)
                                if isinstance(iqdb_api_result, CachingError) or iqdb_api_result.similarity < SearchConfig.thresholds.iqdb_similarity:
                                    if not isinstance(iqdb_api_result, CachingError) and iqdb_api_result.similarity is not None:
                                        similaritiesDict[iqdb_api_result] = iqdb_api_result.similarity

                                    #### UNDER THE DEFINED SIMILARITY THRESHOLD

                                    if len(similaritiesDict) > 0:
                                        bestResult = max(similaritiesDict.items(), key=operator.itemgetter(1))[0]
                                        
                                        if isinstance(bestResult, TraceMOECache):
                                            return ImageSearchResult(tracemoe_cache_result, tracemoe_cache_result.similarity, anilist_id_search(tracemoe_cache_result.anilist_id), low_similarity=True)
                                        elif isinstance(bestResult, SauceNAOCache):
                                            return ImageSearchResult(saucenao_cache_result, saucenao_cache_result.similarity, (title_search(saucenao_cache_result.title) if saucenao_cache_result.is_anime else None), low_similarity=True)
                                        elif isinstance(bestResult, IQDBCache):
                                            return ImageSearchResult(iqdb_cache_result, iqdb_cache_result.similarity, None, low_similarity=True)
                                        else: #### IF NO RESULT ARE LEFT
                                            return SearchingError("NO_RESULT", "No result found.")
                                    
                                    else:
                                        return SearchingError("NO_RESULT", "No result found.")

                                else: # IF FOUND IN IQDB API
                                    return ImageSearchResult(iqdb_api_result, iqdb_api_result.similarity, None)
                                    
                            else: # IF FOUND IN SAUCENAO API
                                return ImageSearchResult(saucenao_api_result, saucenao_api_result.similarity, (title_search(saucenao_api_result.title) if saucenao_api_result.is_anime else None))

                        else: # IF FOUND IN TRACEMOE API
                            return ImageSearchResult(tracemoe_api_result, tracemoe_api_result.similarity, anilist_id_search(tracemoe_api_result.anilist_id))
                    
                    else: # IF FOUND IN IQDB CACHE
                        return ImageSearchResult(iqdb_cache_result, iqdb_cache_result.similarity, None)

                else: # IF FOUND IN SAUCE NAO CACHE
                    return ImageSearchResult(saucenao_cache_result, saucenao_cache_result.similarity, (title_search(saucenao_cache_result.title) if saucenao_cache_result.is_anime else None))
            
            else: # IF FOUND IN TRACEMOE CACHE
                return ImageSearchResult(tracemoe_cache_result, tracemoe_cache_result.similarity, anilist_id_search(tracemoe_cache_result.anilist_id))
        
        else: # IF FOUND IN ERINA DATABASE
            erinacache.erina_caching(str(image_hash), erina_database_path, erina_database_similarity, erina_database_result.anilist_id)
            return ImageSearchResult(erina_database_result, erina_database_similarity, anilist_id_search(erina_database_result.anilist_id))
            
    else: # IF FOUND IN ERINA CACHE
        return ImageSearchResult(parser.ErinaFile("erina_database", erina_cache_result.path), erina_cache_result.similarity, anilist_id_search(erina_cache_result.anilist_id))

    return None
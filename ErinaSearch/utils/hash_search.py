import os
import operator

import numpy

from safeIO import TextFile

from Erina.config import Search as SearchConfig
from Erina.env_information import erina_dir
from ErinaParser import parser
from ErinaSearch.utils import anilist_id_search
from ErinaSearch.utils import title_search
from ErinaCaches import erinacache
from ErinaParser.utils.tracemoe_parser import TraceMOECache
from ErinaParser.utils.saucenao_parser import SauceNAOCache
from ErinaParser.utils.iqdb_parser import IQDBCache
from Erina.Errors import isAnError
from Erina.Errors import SearchingError

from Erina.erina_stats import db as DatabaseStats
from Erina.erina_stats import StatsAppend
class ImageSearchResult():
    """
    An Image Search Result object containing the search result
    """
    def __init__(self, detectionResut, similarity, animeResult, image_hash, low_similarity=False) -> None:
        self.detectionResult = detectionResut
        self.similarity = similarity
        self.animeResult = animeResult
        self.hash = image_hash
        self.low_similarity = low_similarity
    
    def as_dict(self):
        return {
            "detectionResult": self.detectionResult.as_dict(),
            "similarity": self.similarity,
            "hash": str(self.hash),
            "animeResult": (self.animeResult.as_dict() if self.animeResult is not None else None),
            "lowSimilarity": self.low_similarity,
            "docType": "IMAGE_SEARCH"
        }

    def as_text(self):
        result = "Similarity: " + str(self.similarity) + "\nLow Similarity: " + str(self.low_similarity) + "\n"
        result += " -- Detection Result -- \n" + self.detectionResult.as_text() + "\n\n"
        result += " -- Anime Result -- \n" + self.detectionResult.as_text()

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
    if isAnError(image_hash): # If there is an error
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
            return parser.erina_parser.ErinaCache(TextFile(f"{str(erina_dir)}/{str(image_hash)}.erina").read())
        return None

    def search_anime_in_tracemoe_cache():
        if os.path.isfile(tracemoe_cache_path + str(image_hash) + '.erina'):
            return parser.tracemoe_parser.TraceMOECache(TextFile(tracemoe_cache_path + str(image_hash) + '.erina').read())
        return None

    def search_anime_in_saucenao_cache():
        if os.path.isfile(saucenao_cache_path + str(image_hash) + '.erina'):
            return parser.saucenao_parser.SauceNAOCache(TextFile(saucenao_cache_path + str(image_hash) + '.erina').read())
        return None

    def search_anime_in_iqdb_cache():
        if os.path.isfile(iqdb_cache_path + str(image_hash) + '.erina'):
            return parser.iqdb_parser.IQDBCache(TextFile(iqdb_cache_path + str(image_hash) + '.erina').read())
        return None

    ##########################
    #        SEARCHING       #
    ##########################
        
    similaritiesDict = {}
    erina_cache_result = search_anime_in_erina_cache()
    if erina_cache_result is None or isAnError(erina_cache_result) or erina_cache_result.similarity < SearchConfig.thresholds.erina_similarity:

        erina_database_result, erina_database_similarity, erina_database_path = search_anime_in_erina_database()
        if erina_database_result is None or isAnError(erina_database_result) or erina_database_similarity < SearchConfig.thresholds.erina_similarity:
            
            tracemoe_cache_result = search_anime_in_tracemoe_cache()
            if tracemoe_cache_result is None or isAnError(tracemoe_cache_result) or (tracemoe_cache_result.similarity if tracemoe_cache_result.similarity is not None else 0) < SearchConfig.thresholds.tracemoe_similarity:

                saucenao_cache_result = search_anime_in_saucenao_cache()
                if saucenao_cache_result is None or isAnError(saucenao_cache_result) or (saucenao_cache_result.similarity if saucenao_cache_result.similarity is not None else 0) < SearchConfig.thresholds.saucenao_similarity:
                    
                    iqdb_cache_result = search_anime_in_iqdb_cache()
                    if iqdb_cache_result is None or isAnError(iqdb_cache_result) or (iqdb_cache_result.similarity if iqdb_cache_result.similarity is not None else 0) < SearchConfig.thresholds.iqdb_similarity:
                        
                        tracemoe_api_result = erinacache.tracemoe_caching(image_hash)
                        if isAnError(tracemoe_api_result) or tracemoe_api_result.similarity < SearchConfig.thresholds.tracemoe_similarity:
                            if not isAnError(tracemoe_api_result) and tracemoe_api_result.similarity is not None:
                                similaritiesDict[tracemoe_api_result] = tracemoe_api_result.similarity
            
                            saucenao_api_result = erinacache.saucenao_caching(image_hash)
                            if isAnError(saucenao_api_result) or saucenao_api_result.similarity < SearchConfig.thresholds.saucenao_similarity:
                                if not isAnError(saucenao_api_result) and saucenao_api_result.similarity is not None:
                                    similaritiesDict[saucenao_api_result] = saucenao_api_result.similarity

                                iqdb_api_result = erinacache.iqdb_caching(image_hash)
                                if isAnError(iqdb_api_result) or iqdb_api_result.similarity < SearchConfig.thresholds.iqdb_similarity:
                                    if not isAnError(iqdb_api_result) and iqdb_api_result.similarity is not None:
                                        similaritiesDict[iqdb_api_result] = iqdb_api_result.similarity

                                    #### UNDER THE DEFINED SIMILARITY THRESHOLD

                                    if len(similaritiesDict) > 0:
                                        bestResult = max(similaritiesDict.items(), key=operator.itemgetter(1))[0]
                                        
                                        if isinstance(bestResult, TraceMOECache):
                                            return ImageSearchResult(bestResult, bestResult.similarity, anilist_id_search.search_anime_by_anilist_id(bestResult.anilist_id), low_similarity=True, image_hash=image_hash)
                                        elif isinstance(bestResult, SauceNAOCache):
                                            return ImageSearchResult(bestResult, bestResult.similarity, (title_search.searchAnime(bestResult.title) if bestResult.is_anime else None), low_similarity=True, image_hash=image_hash)
                                        elif isinstance(bestResult, IQDBCache):
                                            return ImageSearchResult(bestResult, bestResult.similarity, None, low_similarity=True, image_hash=image_hash)
                                        else: #### IF NO RESULT ARE LEFT
                                            return SearchingError("NO_RESULT", "No result found.")
                                    
                                    else:
                                        return SearchingError("NO_RESULT", "No result found.")

                                else: # IF FOUND IN IQDB API
                                    return ImageSearchResult(iqdb_api_result, iqdb_api_result.similarity, None, image_hash=image_hash)
                                    
                            else: # IF FOUND IN SAUCENAO API
                                return ImageSearchResult(saucenao_api_result, saucenao_api_result.similarity, (title_search.searchAnime(saucenao_api_result.title) if saucenao_api_result.is_anime else None), image_hash=image_hash)

                        else: # IF FOUND IN TRACEMOE API
                            return ImageSearchResult(tracemoe_api_result, tracemoe_api_result.similarity, anilist_id_search.search_anime_by_anilist_id(tracemoe_api_result.anilist_id), image_hash=image_hash)
                    
                    else: # IF FOUND IN IQDB CACHE
                        return ImageSearchResult(iqdb_cache_result, iqdb_cache_result.similarity, None, image_hash=image_hash)

                else: # IF FOUND IN SAUCE NAO CACHE
                    return ImageSearchResult(saucenao_cache_result, saucenao_cache_result.similarity, (title_search.searchAnime(saucenao_cache_result.title) if saucenao_cache_result.is_anime else None), image_hash=image_hash)
            
            else: # IF FOUND IN TRACEMOE CACHE
                return ImageSearchResult(tracemoe_cache_result, tracemoe_cache_result.similarity, anilist_id_search.search_anime_by_anilist_id(tracemoe_cache_result.anilist_id), image_hash=image_hash)
        
        else: # IF FOUND IN ERINA DATABASE
            erinacache.erina_caching(str(image_hash), erina_database_path, erina_database_similarity, erina_database_result.anilist_id)
            return ImageSearchResult(erina_database_result, erina_database_similarity, anilist_id_search.search_anime_by_anilist_id(erina_database_result.anilist_id), image_hash=image_hash)
            
    else: # IF FOUND IN ERINA CACHE
        return ImageSearchResult(parser.ErinaFile("erina_database", erina_cache_result.path), erina_cache_result.similarity, anilist_id_search.search_anime_by_anilist_id(erina_cache_result.anilist_id), image_hash=image_hash)

    return None
"""
Erina Anime Title Searching API for the Erina Project

© Anime no Sekai
"""

from os.path import isfile

from ErinaParser.utils.anilist_parser import AnilistCache
from ErinaParser import parser
from env_information import erina_dir
from ErinaCaches.erinacache import anilist_search_caching
from ErinaCaches.erinacache import anilist_caching
from ErinaSearch.utils import cosine_similarity

anilistCachesPath = erina_dir + "/ErinaCaches/AniList_Cache/"

def searchAnime(query):
    """
    Searches an anime by its title
    """
    query = str(query)
    cleanQuery = query.lower().replace(" ", '')
    
    anilistID, similarity = cosine_similarity.search(cleanQuery)
    if similarity > 0.95:
        if isfile(anilistCachesPath + str(anilistID) + ".erina"):
            with open(anilistCachesPath + str(anilistID) + ".erina", "r", encoding='utf-8', errors='ignore') as dataFile:
                data = dataFile.read()
            return AnilistCache(data)
        else:
            return anilist_caching(anilistID)

    return anilist_search_caching(query)
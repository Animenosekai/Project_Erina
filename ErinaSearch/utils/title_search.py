"""
Erina Anime Title Searching API for the Erina Project

© Anime no Sekai
"""

from Erina.config import Caches as CachesConfig
from os.path import isfile
from time import time

from safeIO import TextFile

from Erina.env_information import erina_dir
from ErinaSearch.utils import cosine_similarity
from ErinaCaches.erinacache import anilist_caching
from ErinaCaches.erinacache import anilist_search_caching
from ErinaParser.utils.anilist_parser import AnilistCache

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
            data = TextFile(anilistCachesPath + str(anilistID) + ".erina").read()
            anilistCacheData = AnilistCache(data)
            if time() - anilistCacheData.cache_timestamp.timestamp > CachesConfig.anilist_expiration:
                return anilist_caching(anilistID)
            else:
                return anilistCacheData
        else:
            return anilist_caching(anilistID)

    return anilist_search_caching(query)
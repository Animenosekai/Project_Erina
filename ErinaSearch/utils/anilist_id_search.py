from os.path import isfile
from time import time
from Erina.config import Caches as CachesConfig
from ErinaParser.utils.anilist_parser import AnilistCache
from Erina.env_information import erina_dir
from ErinaCaches.erinacache import anilist_caching
from safeIO import TextFile

def search_anime_by_anilist_id(anilist_id):
    """
    Let you search through Erina's database and other database (Manami Projects' anime_offline_database and AniList API) with the AniList ID of the Anime!\n
    © Anime no Sekai - 2020
    Project Erina
    """
    filename = str(anilist_id) + ".erina"
    if isfile(erina_dir + "/ErinaCaches/AniList_Cache/" + filename):
        data = TextFile(erina_dir + "/ErinaCaches/AniList_Cache/" + filename).read()
        anilistCacheData = AnilistCache(data)
        if time() - anilistCacheData.cache_timestamp.timestamp > CachesConfig.anilist_expiration:
            return anilist_caching(anilist_id)
        else:
            return anilistCacheData
    else:
        return anilist_caching(anilist_id)
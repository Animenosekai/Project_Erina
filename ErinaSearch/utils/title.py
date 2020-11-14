"""
Erina Anime Title Searching API for the Erina Project

© Anime no Sekai
"""

import os
from ErinaParser import parser
from env_information import erina_dir
from ErinaCaches.erinacache import anilist_search_caching
from ErinaCaches.utils.Errors import CachingError
from ErinaDB.ManamiDB.manami_db_data import Database

def searchAnime(query):
    """
    Searches an anime by its title
    """
    for anime in Database.data:
        if query in Database.data[anime] and f"{str(anime)}.erina" in os.listdir(erina_dir + "/ErinaCaches/AniList_Cache"):
            return parser.ErinaFile("anilist_cache", f"{str(anime)}.erina").content
    
    for cacheFile in os.listdir(erina_dir + "/ErinaCaches/AniList_Cache"):
        current = parser.ErinaFile("anilist_cache", cacheFile)
        if current.content.title == query:
            return current.content

    return anilist_search_caching(query)
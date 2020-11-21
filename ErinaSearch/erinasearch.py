"""
Anime Search API for the Erina Project

@author: Anime no Sekai
Erina Project — 2020
"""
import erina_log
from ErinaHash import erinahash
from ErinaSearch.utils import title_search, hash_search, anilist_id_search

def anilistIDSearch(anilistID):
    """
    Searches an anime from AniList Caches or AniList API
    
    Erina Project — 2020\n
    © Anime no Sekai
    """
    return anilist_id_search.search_anime_by_anilist_id(anilistID)

def searchAnime(query):
    """
    Searches an anime by its title

    Erina Project — 2020\n
    © Anime no Sekai
    """
    return title_search.searchAnime(query)

def imageSearch(image):
    """
    Searches an anime from an image (anime scene for example)

    image: Can be an URL, a path, a base64 encoded string or a PIL.Image.Image instance

    Erina Project — 2020\n
    © Anime no Sekai
    """
    return hash_search.search_anime_by_hash(erinahash.hash_image(image))
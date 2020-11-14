import os
from env_information import erina_dir
from ErinaParser import parser
import erina_log
from ErinaCaches.erinacache import anilist_caching

def search_anime_by_anilist_id(anilist_id):
    """
    Let you search through Erina's database and other database (Manami Projects' anime_offline_database and AniList API) with the AniList ID of the Anime!\n
    © Anime no Sekai - 2020
    Project Erina
    """
    erina_log.logsearch(f'Searching the anime by his AniList ID... ({str(anilist_id)})', search_type='anilistid', value=str(anilist_id))
    filename = str(anilist_id) + ".erina"
    if filename in os.listdir(erina_dir + "/ErinaCaches/AniList_Cache/"):
        return parser.ErinaFile("anilist_cache", filename).content
    else:
        return anilist_caching(anilist_id)
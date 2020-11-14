"""
Anime Search API for the Erina Project

@author: Anime no Sekai
Erina Project - 2020
"""
import sys
sys.path.append('.')
sys.path.append('..')

import json
from io import BytesIO
from base64 import b64decode
import lifeeasy
import filecenter
import imagehash

import env_information
import erina_log
import config
from ErinaSearch import erina_dbread
from ErinaSearch import result_python_translation
from ErinaDB import erinadatabase
from ErinaCaches import erinacache, iqdb_api
from ErinaHash import erinahash

anilist_cache_path = env_information.erina_dir + '/ErinaCaches/AniList_Cache/'
erina_cache_path = env_information.erina_dir + '/ErinaCaches/Erina_Cache/'
erina_db_path = env_information.erina_dir + '/ErinaDB/ErinaDatabase/'
tracemoe_cache_path = env_information.erina_dir + '/ErinaCaches/TraceMoe_Cache/'
saucenao_cache_path = env_information.erina_dir + '/ErinaCaches/SauceNAO_Cache/'
iqdb_cache_path = env_information.erina_dir + '/ErinaCaches/IQDB_Cache/'
manami_db_path = env_information.erina_dir + '/ErinaDB/ManamiDB/'

def search_anime_by_image(image, anilist_priority=False):
    """
    Let you search through Erina's database and other database (Manami Projects' anime_offline_database and AniList API) with the given image/scene from an anime (average hash/aHash from the image_hash python module)\n
    © Anime no Sekai - 2020
    Project Erina
    """
    image_hash = erinahash.hash_image(image)
    search_result = search_anime_by_hash(image_hash=image_hash, anilist_priority=anilist_priority)
    return search_result

def search_anime_by_imageurl(image_url, anilist_priority=False):
    """
    Let you search through Erina's database and other database (Manami Projects' anime_offline_database and AniList API) with the given image/scene from an anime (average hash/aHash from the image_hash python module)\n
    © Anime no Sekai - 2020
    Project Erina
    """
    image_hash = erinahash.hash_image_from_url(image_url)
    search_result = search_anime_by_hash(image_hash=image_hash, image_url=image_url, anilist_priority=anilist_priority)
    return search_result

def search_anime_from_image_path(image_path, anilist_priority=False):
    """
    Let you search through Erina's database and other database (Manami Projects' anime_offline_database and AniList API) with the given image/scene from an anime (average hash/aHash from the image_hash python module)\n
    © Anime no Sekai - 2020
    Project Erina
    """
    image_hash = erinahash.hash_image_from_path(image_path)
    base64 = erinahash.base64_from_image(image_path)
    search_result = search_anime_by_hash(image_hash=image_hash, image_base64=str(base64), anilist_priority=anilist_priority)
    return search_result

def search_anime_by_base64(base64_data, anilist_priority=False):
    """
    Let you search through Erina's database and other database (Manami Projects' anime_offline_database and AniList API) with the given image/scene from an anime (average hash/aHash from the image_hash python module)\n
    © Anime no Sekai - 2020
    Project Erina
    """
    image_hash = erinahash.hash_image_from_base64(base64_data)
    base64 = base64_data
    search_result = search_anime_by_hash(image_hash=image_hash, image_base64=str(base64), anilist_priority=anilist_priority)
    return search_result
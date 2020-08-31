"""
Hashing API for the Erina Project

@author: Anime no Sekai
Erina Project - 2020
"""
import sys
sys.path.append('..')

import base64
from io import BytesIO

import lifeeasy
import imagehash
from PIL import Image

import erina_log

def hash_image(image, algorithm='aHash'):
    """
    Hashes the given image with the chosen algorithm (average hash by default)
    © Anime no Sekai - 2020
    Project Erina
    """
    erina_log.loghash('Hashing the image')
    image_hash = ''
    if algorithm == 'aHash':
        image_hash = imagehash.average_hash(image) # Needs to be a PIL instance
    elif algorithm == 'cHash':
        image_hash = imagehash.colorhash(image)
    elif algorithm == 'dHash':
        image_hash = imagehash.dhash(image)
    elif algorithm == 'dHash_vertical':
        image_hash = imagehash.dhash_vertical(image)
    elif algorithm == 'pHash':
        image_hash = imagehash.phash(image)
    elif algorithm == 'pHash_simple':
        image_hash = imagehash.phash_simple(image)
    elif algorithm == 'wHash':
        image_hash = imagehash.whash(image)
    erina_log.loghash('Image hash is ' + str(image_hash), hash_string=str(image_hash))
    return image_hash

def hash_image_from_url(image_url, algorithm='aHash'):
    """
    Hashes the given image from the image url with the chosen algorithm (average hash by default)
    © Anime no Sekai - 2020
    Project Erina
    """
    erina_log.loghash(f'Downloading the image ({image_url})')
    image_request = lifeeasy.request(image_url, 'get')
    downloaded_image = Image.open(BytesIO(image_request.content)) # Open the downloaded image as a PIL Image instance
    return hash_image(image=downloaded_image, algorithm=algorithm)

def hash_image_from_path(image_path, algorithm='aHash'):
    """
    Hashes the given image from his path with the chosen algorithm (average hash by default)
    © Anime no Sekai - 2020
    Project Erina
    """
    image = Image.open(image_path)
    return hash_image(image=image, algorithm=algorithm)

def base64_from_image(image_path):
    """
    Converts an image to base64
    © Anime no Sekai - 2020
    Project Erina
    """
    erina_log.loghash(f'Converting to base64 ({image_path})', 'base64')
    image = open(image_path, 'rb')
    image_content = image.read()
    image.close()
    return base64.b64encode(image_content)

def hash_image_from_base64(base64_data, algorithm='aHash'):
    """
    Hashes the given image from his base64 form with the chosen algorithm (average hash by default)
    © Anime no Sekai - 2020
    Project Erina
    """
    image = Image.open(BytesIO(base64.b64decode(base64_data)))
    return hash_image(image=image, algorithm=algorithm)
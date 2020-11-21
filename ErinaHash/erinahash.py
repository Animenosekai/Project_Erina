"""
Hashing API for the Erina Project

@author: Anime no Sekai
Erina Project — 2020
"""

import base64
from io import BytesIO
from os.path import isfile

import requests
import imagehash
from PIL import Image
from ErinaHash.utils import Errors

import erina_log
import config

class HashObject():
    """
    An image hash object

    Erina Project — 2020\n
    © Anime no Sekai
    """
    def __init__(self, hashobj, ImageObj, URL=None) -> None:
        self.ImageHash = hashobj
        self.Image = ImageObj
        self.ImageIO = BytesIO()
        self.Image.save(self.ImageIO, format="JPEG")
        self.hash = str(self.ImageHash)
        self.base64 = str(base64.b64encode(self.ImageIO.getvalue()).decode("utf-8"))
        if URL is not None:
            self.has_url = True
            self.url = str(URL)
        else:
            self.has_url = False
            self.url = None
    
    def __repr__(self) -> str:
        return str(self.hash)

def hash_image(image, algorithm=None):
    """
    Hashes a given image

    image: Can be an URL, a path, a base64 encoded string or a PIL.Image.Image instance

    Erina Project — 2020\n
    © Anime no Sekai
    """
    result = None
    has_url = False

    # Needs to be a PIL instance
    if isfile(str(image)):
        image = Image.open(image)
    elif isinstance(image, Image.Image):
        image = image
    else:
        try:
            if base64.b64decode(str(image), validate=True):
                image = Image.open(BytesIO(base64.b64decode(str(image))))
            else:
                raise ValueError("b64decode returned an empty string")
        except:
            try:
                image = Image.open(BytesIO(requests.get(str(image)).content)) # Open the downloaded image as a PIL Image instance
                has_url  = True
            except:
                return Errors.HashingError("INVALID_IMAGE_TYPE", "We couldn't convert the given image to a PIL.Image.Image instance")
    
    if algorithm is None:
        algorithm = str(config.hashing_algorithm)

    algorithm = str(algorithm).lower().replace(" ", "")
    if algorithm == 'ahash' or algorithm == "a":
        result = imagehash.average_hash(image)
    elif algorithm == 'chash' or algorithm == "c":
        result = imagehash.colorhash(image)
    elif algorithm == 'dhash' or algorithm == "d":
        result = imagehash.dhash(image)
    elif algorithm == 'phash' or algorithm == "p":
        result = imagehash.phash(image)
    elif algorithm == 'wHash' or algorithm == "w":
        result = imagehash.whash(image)
    else:
        algorithm = algorithm.replace("_", "")
        if algorithm == 'dhashvertical' or algorithm == "dvertical" or algorithm == "dvert":
            result = imagehash.dhash_vertical(image)
        elif algorithm == 'phashsimple' or algorithm == "psimple":
            result = imagehash.phash_simple(image)
        else:
            return Errors.HashingError("INVALID_ALGORITHM", "We couldn't determine the hashing algorithm you wanted to use.")
    
    return HashObject(result, image, has_url)

def base64_from_image(image_path):
    """
    Converts an image to base64
    
    Erina Project — 2020\n
    © Anime no Sekai
    """
    erina_log.loghash(f'Converting to base64 ({image_path})', 'base64')
    with open(image_path, "rb") as readingFile:
        image_content = readingFile.read()
    return base64.b64encode(image_content).decode("utf-8")
"""
Image preparation for hashing test for the Erina Project

@author: Anime no Sekai
Erina Project - 2020
"""

import filecenter
import lifeeasy
from PIL import Image, ImageEnhance, ImageOps
import numpy as np
import os
import cv2


def noisy(noise_typ, image):
    '''
    Parameters
    ----------
    image : ndarray
        Input image data. Will be converted to float.
    mode : str
        One of the following strings, selecting the type of noise to add:

        'gauss'     Gaussian-distributed additive noise.
        'poisson'   Poisson-distributed noise generated from the data.
        's&p'       Replaces random pixels with 0 or 1.
        'speckle'   Multiplicative noise using out = image + n*image,where
                    n is uniform noise with specified mean & variance.

    By Shubham Pachori
    > https://stackoverflow.com/questions/22937589/how-to-add-noise-gaussian-salt-and-pepper-etc-to-image-in-python-with-opencv
    '''
    if noise_typ == "gauss":
        row,col,ch= image.shape
        mean = 0
        var = 0.1
        sigma = var**0.5
        gauss = np.random.normal(mean,sigma,(row,col,ch))
        gauss = gauss.reshape(row,col,ch)
        noisy = image + gauss
        return noisy
    elif noise_typ == "s&p":
        row,col,ch = image.shape
        s_vs_p = 0.5
        amount = 0.004
        out = np.copy(image)
        # Salt mode
        num_salt = np.ceil(amount * image.size * s_vs_p)
        coords = [np.random.randint(0, i - 1, int(num_salt))
                for i in image.shape]
        out[coords] = 1

        # Pepper mode
        num_pepper = np.ceil(amount* image.size * (1. - s_vs_p))
        coords = [np.random.randint(0, i - 1, int(num_pepper))
                for i in image.shape]
        out[coords] = 0
        return out
    elif noise_typ == "poisson":
        vals = len(np.unique(image))
        vals = 2 ** np.ceil(np.log2(vals))
        noisy = np.random.poisson(image * vals) / float(vals)
        return noisy
    elif noise_typ =="speckle":
        row,col,ch = image.shape
        gauss = np.random.randn(row,col,ch)
        gauss = gauss.reshape(row,col,ch)        
        noisy = image + image * gauss
        return noisy

print('[image pre-processing] environment preparation')
### ENV PREPARATION
if filecenter.isfile(lifeeasy.working_dir() + '/image.jpg'):
    extension = '.jpg'
elif filecenter.isfile(lifeeasy.working_dir() + '/image.png'):
    extension = '.png'
else:
    raise FileNotFoundError('No image (jpg or png) was found in the current working directory.')

if filecenter.isdir(lifeeasy.working_dir() + '/image_dataset'):
    filecenter.delete(lifeeasy.working_dir() + '/image_dataset')
filecenter.make_dir(lifeeasy.working_dir() + '/image_dataset')

print('[image pre-processing] opening original image')
### OPENING THE UNMODIFIED (original) IMAGE
original_image = Image.open("image" + extension)

###### BRIGHTNESS ENHANCEMENT
print('[image pre-processing] brightness enhancement')
brightness_enhancer = ImageEnhance.Brightness(original_image)

image_brightness_01 = brightness_enhancer.enhance(0.1)
image_brightness_01.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_brightness_01' + extension)
image_brightness_02 = brightness_enhancer.enhance(0.2)
image_brightness_02.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_brightness_02' + extension)
image_brightness_03 = brightness_enhancer.enhance(0.3)
image_brightness_03.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_brightness_03' + extension)
image_brightness_04 = brightness_enhancer.enhance(0.4)
image_brightness_04.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_brightness_04' + extension)
image_brightness_05 = brightness_enhancer.enhance(0.5)
image_brightness_05.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_brightness_05' + extension)
image_brightness_06 = brightness_enhancer.enhance(0.6)
image_brightness_06.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_brightness_06' + extension)
image_brightness_07 = brightness_enhancer.enhance(0.7)
image_brightness_07.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_brightness_07' + extension)
image_brightness_08 = brightness_enhancer.enhance(0.8)
image_brightness_08.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_brightness_08' + extension)
image_brightness_09 = brightness_enhancer.enhance(0.9)
image_brightness_09.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_brightness_09' + extension)

image_brightness_11 = brightness_enhancer.enhance(1.1)
image_brightness_11.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_brightness_11' + extension)
image_brightness_12 = brightness_enhancer.enhance(1.2)
image_brightness_12.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_brightness_12' + extension)
image_brightness_13 = brightness_enhancer.enhance(1.3)
image_brightness_13.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_brightness_13' + extension)
image_brightness_14 = brightness_enhancer.enhance(1.4)
image_brightness_14.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_brightness_14' + extension)
image_brightness_15 = brightness_enhancer.enhance(1.5)
image_brightness_15.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_brightness_15' + extension)
image_brightness_16 = brightness_enhancer.enhance(1.6)
image_brightness_16.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_brightness_16' + extension)
image_brightness_17 = brightness_enhancer.enhance(1.7)
image_brightness_17.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_brightness_17' + extension)
image_brightness_18 = brightness_enhancer.enhance(1.8)
image_brightness_18.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_brightness_18' + extension)
image_brightness_19 = brightness_enhancer.enhance(1.9)
image_brightness_19.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_brightness_19' + extension)
image_brightness_20 = brightness_enhancer.enhance(2)
image_brightness_20.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_brightness_20' + extension)

###### CONTRAST ENHANCEMENT
print('[image pre-processing] contrast enhancement')
contrast_enhancer = ImageEnhance.Contrast(original_image)

image_contrast_01 = contrast_enhancer.enhance(0.1)
image_contrast_01.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_contrast_01' + extension)
image_contrast_02 = contrast_enhancer.enhance(0.2)
image_contrast_02.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_contrast_02' + extension)
image_contrast_03 = contrast_enhancer.enhance(0.3)
image_contrast_03.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_contrast_03' + extension)
image_contrast_04 = contrast_enhancer.enhance(0.4)
image_contrast_04.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_contrast_04' + extension)
image_contrast_05 = contrast_enhancer.enhance(0.5)
image_contrast_05.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_contrast_05' + extension)
image_contrast_06 = contrast_enhancer.enhance(0.6)
image_contrast_06.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_contrast_06' + extension)
image_contrast_07 = contrast_enhancer.enhance(0.7)
image_contrast_07.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_contrast_07' + extension)
image_contrast_08 = contrast_enhancer.enhance(0.8)
image_contrast_08.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_contrast_08' + extension)
image_contrast_09 = contrast_enhancer.enhance(0.9)
image_contrast_09.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_contrast_09' + extension)

image_contrast_11 = contrast_enhancer.enhance(1.1)
image_contrast_11.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_contrast_11' + extension)
image_contrast_12 = contrast_enhancer.enhance(1.2)
image_contrast_12.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_contrast_12' + extension)
image_contrast_13 = contrast_enhancer.enhance(1.3)
image_contrast_13.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_contrast_13' + extension)
image_contrast_14 = contrast_enhancer.enhance(1.4)
image_contrast_14.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_contrast_14' + extension)
image_contrast_15 = contrast_enhancer.enhance(1.5)
image_contrast_15.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_contrast_15' + extension)
image_contrast_16 = contrast_enhancer.enhance(1.6)
image_contrast_16.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_contrast_16' + extension)
image_contrast_17 = contrast_enhancer.enhance(1.7)
image_contrast_17.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_contrast_17' + extension)
image_contrast_18 = contrast_enhancer.enhance(1.8)
image_contrast_18.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_contrast_18' + extension)
image_contrast_19 = contrast_enhancer.enhance(1.9)
image_contrast_19.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_contrast_19' + extension)
image_contrast_20 = contrast_enhancer.enhance(2)
image_contrast_20.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_contrast_20' + extension)

###### COLOR ENHANCEMENT
print('[image pre-processing] color enhancement')
color_enhancer = ImageEnhance.Color(original_image)

image_color_01 = color_enhancer.enhance(0.1)
image_color_01.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_color_01' + extension)
image_color_02 = color_enhancer.enhance(0.2)
image_color_02.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_color_02' + extension)
image_color_03 = color_enhancer.enhance(0.3)
image_color_03.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_color_03' + extension)
image_color_04 = color_enhancer.enhance(0.4)
image_color_04.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_color_04' + extension)
image_color_05 = color_enhancer.enhance(0.5)
image_color_05.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_color_05' + extension)
image_color_06 = color_enhancer.enhance(0.6)
image_color_06.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_color_06' + extension)
image_color_07 = color_enhancer.enhance(0.7)
image_color_07.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_color_07' + extension)
image_color_08 = color_enhancer.enhance(0.8)
image_color_08.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_color_08' + extension)
image_color_09 = color_enhancer.enhance(0.9)
image_color_09.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_color_09' + extension)

image_color_11 = color_enhancer.enhance(1.1)
image_color_11.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_color_11' + extension)
image_color_12 = color_enhancer.enhance(1.2)
image_color_12.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_color_12' + extension)
image_color_13 = color_enhancer.enhance(1.3)
image_color_13.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_color_13' + extension)
image_color_14 = color_enhancer.enhance(1.4)
image_color_14.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_color_14' + extension)
image_color_15 = color_enhancer.enhance(1.5)
image_color_15.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_color_15' + extension)
image_color_16 = color_enhancer.enhance(1.6)
image_color_16.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_color_16' + extension)
image_color_17 = color_enhancer.enhance(1.7)
image_color_17.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_color_17' + extension)
image_color_18 = color_enhancer.enhance(1.8)
image_color_18.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_color_18' + extension)
image_color_19 = color_enhancer.enhance(1.9)
image_color_19.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_color_19' + extension)
image_color_20 = color_enhancer.enhance(2)
image_color_20.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_color_20' + extension)

###### SHARPNESS ENHANCEMENT
print('[image pre-processing] sharpness enhancement')
sharpness_enhancer = ImageEnhance.Sharpness(original_image)

image_sharpness_01 = sharpness_enhancer.enhance(0.1)
image_sharpness_01.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_sharpness_01' + extension)
image_sharpness_02 = sharpness_enhancer.enhance(0.2)
image_sharpness_02.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_sharpness_02' + extension)
image_sharpness_03 = sharpness_enhancer.enhance(0.3)
image_sharpness_03.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_sharpness_03' + extension)
image_sharpness_04 = sharpness_enhancer.enhance(0.4)
image_sharpness_04.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_sharpness_04' + extension)
image_sharpness_05 = sharpness_enhancer.enhance(0.5)
image_sharpness_05.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_sharpness_05' + extension)
image_sharpness_06 = sharpness_enhancer.enhance(0.6)
image_sharpness_06.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_sharpness_06' + extension)
image_sharpness_07 = sharpness_enhancer.enhance(0.7)
image_sharpness_07.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_sharpness_07' + extension)
image_sharpness_08 = sharpness_enhancer.enhance(0.8)
image_sharpness_08.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_sharpness_08' + extension)
image_sharpness_09 = sharpness_enhancer.enhance(0.9)
image_sharpness_09.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_sharpness_09' + extension)

image_sharpness_11 = sharpness_enhancer.enhance(1.1)
image_sharpness_11.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_sharpness_11' + extension)
image_sharpness_12 = sharpness_enhancer.enhance(1.2)
image_sharpness_12.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_sharpness_12' + extension)
image_sharpness_13 = sharpness_enhancer.enhance(1.3)
image_sharpness_13.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_sharpness_13' + extension)
image_sharpness_14 = sharpness_enhancer.enhance(1.4)
image_sharpness_14.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_sharpness_14' + extension)
image_sharpness_15 = sharpness_enhancer.enhance(1.5)
image_sharpness_15.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_sharpness_15' + extension)
image_sharpness_16 = sharpness_enhancer.enhance(1.6)
image_sharpness_16.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_sharpness_16' + extension)
image_sharpness_17 = sharpness_enhancer.enhance(1.7)
image_sharpness_17.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_sharpness_17' + extension)
image_sharpness_18 = sharpness_enhancer.enhance(1.8)
image_sharpness_18.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_sharpness_18' + extension)
image_sharpness_19 = sharpness_enhancer.enhance(1.9)
image_sharpness_19.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_sharpness_19' + extension)
image_sharpness_20 = sharpness_enhancer.enhance(2)
image_sharpness_20.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_sharpness_20' + extension)

######## GRAYSCALE
print('[image pre-processing] grayscaling')
image_grayscale = original_image.convert('L')
image_grayscale.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_grayscale' + extension)

######## RGB CONVERT
print('[image pre-processing] rgb convert')
image_rgb = original_image.convert('RGB')
image_rgb.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_rgb' + extension)

######## CMYK CONVERT
try:
    print('[image pre-processing] cmyk convert')
    image_cmyk = original_image.convert('CMYK')
    image_cmyk.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_cmyk' + extension)
except:
    print('[error] Error while converting to CMYK')

### List of sizes
size_57_57 = (57, 57)
size_75_75 = (75, 75)
size_75_100 = (75, 100)
size_143_59 = (143, 59)
size_312_390 = (312, 390)
size_426_240 = (426, 240)
size_595_842 = (595, 842)
size_640_360 = (640, 360)
size_720_576 = (720, 576)
size_854_480 = (854, 480)
size_1024_576 = (1024, 576)
size_1280_720 = (1280, 720)
size_1440_1080 = (1440, 1080)
size_1920_1080 = (1920, 1080)
size_1998_1080 = (1998, 1080)
size_2048_858 = (2048, 858)
size_2560_1080 = (2560, 1080)
size_2560_1440 = (2560, 1440)
size_3840_2160 = (3840, 2160)

######## RESIZE
print('[image pre-processing] resizing')
image_resize_57_57 = original_image.resize(size_57_57)
image_resize_57_57.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_resize_57_57' + extension)
image_resize_75_75 = original_image.resize(size_75_75)
image_resize_75_75.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_resize_75_75' + extension)
image_resize_75_100 = original_image.resize(size_75_100)
image_resize_75_100.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_resize_75_100' + extension)
image_resize_143_59 = original_image.resize(size_143_59)
image_resize_143_59.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_resize_143_59' + extension)
image_resize_312_390 = original_image.resize(size_312_390)
image_resize_312_390.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_resize_312_390' + extension)
image_resize_426_240 = original_image.resize(size_426_240)
image_resize_426_240.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_resize_426_240' + extension)
image_resize_595_842 = original_image.resize(size_595_842)
image_resize_595_842.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_resize_595_842' + extension)
image_resize_640_360 = original_image.resize(size_640_360)
image_resize_640_360.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_resize_640_360' + extension)
image_resize_720_576 = original_image.resize(size_720_576)
image_resize_720_576.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_resize_720_576' + extension)
image_resize_854_480 = original_image.resize(size_854_480)
image_resize_854_480.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_resize_854_480' + extension)
image_resize_1024_576 = original_image.resize(size_1024_576)
image_resize_1024_576.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_resize_1024_576' + extension)
image_resize_1280_720 = original_image.resize(size_1280_720)
image_resize_1280_720.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_resize_1280_720' + extension)
image_resize_1440_1080 = original_image.resize(size_1440_1080)
image_resize_1440_1080.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_resize_1440_1080' + extension)
image_resize_1920_1080 = original_image.resize(size_1920_1080)
image_resize_1920_1080.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_resize_1920_1080' + extension)
image_resize_1998_1080 = original_image.resize(size_1998_1080)
image_resize_1998_1080.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_resize_1998_1080' + extension)
image_resize_2048_858 = original_image.resize(size_2048_858)
image_resize_2048_858.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_resize_2048_858' + extension)
image_resize_2560_1080 = original_image.resize(size_2560_1080)
image_resize_2560_1080.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_resize_2560_1080' + extension)
image_resize_2560_1440 = original_image.resize(size_2560_1440)
image_resize_2560_1440.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_resize_2560_1440' + extension)
image_resize_3840_2160 = original_image.resize(size_3840_2160)
image_resize_3840_2160.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_resize_3840_2160' + extension)

######## RESIZE SAME ASPECT RATIO
print('[image pre-processing] resizing with same aspect ratio')
image_thumbnail_57_57 = original_image.copy()
image_thumbnail_57_57.thumbnail(size_57_57)
image_thumbnail_57_57.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_thumbnail_57_57' + extension)
image_thumbnail_75_75 = original_image.copy()
image_thumbnail_75_75.thumbnail(size_75_75)
image_thumbnail_75_75.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_thumbnail_75_75' + extension)
image_thumbnail_75_100 = original_image.copy()
image_thumbnail_75_100.thumbnail(size_75_100)
image_thumbnail_75_100.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_thumbnail_75_100' + extension)
image_thumbnail_143_59 = original_image.copy()
image_thumbnail_143_59.thumbnail(size_143_59)
image_thumbnail_143_59.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_thumbnail_143_59' + extension)
image_thumbnail_312_390 = original_image.copy()
image_thumbnail_312_390.thumbnail(size_312_390)
image_thumbnail_312_390.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_thumbnail_312_390' + extension)
image_thumbnail_426_240 = original_image.copy()
image_thumbnail_426_240.thumbnail(size_426_240)
image_thumbnail_426_240.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_thumbnail_426_240' + extension)
image_thumbnail_595_842 = original_image.copy()
image_thumbnail_595_842.thumbnail(size_595_842)
image_thumbnail_595_842.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_thumbnail_595_842' + extension)
image_thumbnail_640_360 = original_image.copy()
image_thumbnail_640_360.thumbnail(size_640_360)
image_thumbnail_640_360.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_thumbnail_640_360' + extension)
image_thumbnail_720_576 = original_image.copy()
image_thumbnail_720_576.thumbnail(size_720_576)
image_thumbnail_720_576.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_thumbnail_720_576' + extension)
image_thumbnail_854_480 = original_image.copy()
image_thumbnail_854_480.thumbnail(size_854_480)
image_thumbnail_854_480.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_thumbnail_854_480' + extension)
image_thumbnail_1024_576 = original_image.copy()
image_thumbnail_1024_576.thumbnail(size_1024_576)
image_thumbnail_1024_576.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_thumbnail_1024_576' + extension)
image_thumbnail_1280_720 = original_image.copy()
image_thumbnail_1280_720.thumbnail(size_1280_720)
image_thumbnail_1280_720.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_thumbnail_1280_720' + extension)
image_thumbnail_1440_1080 = original_image.copy()
image_thumbnail_1440_1080.thumbnail(size_1440_1080)
image_thumbnail_1440_1080.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_thumbnail_1440_1080' + extension)
image_thumbnail_1920_1080 = original_image.copy()
image_thumbnail_1920_1080.thumbnail(size_1920_1080)
image_thumbnail_1920_1080.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_thumbnail_1920_1080' + extension)
image_thumbnail_1998_1080 = original_image.copy()
image_thumbnail_1998_1080.thumbnail(size_1998_1080)
image_thumbnail_1998_1080.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_thumbnail_1998_1080' + extension)
image_thumbnail_2048_858 = original_image.copy()
image_thumbnail_2048_858.thumbnail(size_2048_858)
image_thumbnail_2048_858.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_thumbnail_2048_858' + extension)
image_thumbnail_2560_1080 = original_image.copy()
image_thumbnail_2560_1080.thumbnail(size_2560_1080)
image_thumbnail_2560_1080.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_thumbnail_2560_1080' + extension)
image_thumbnail_2560_1440 = original_image.copy()
image_thumbnail_2560_1440.thumbnail(size_2560_1440)
image_thumbnail_2560_1440.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_thumbnail_2560_1440' + extension)
image_thumbnail_3840_2160 = original_image.copy()
image_thumbnail_3840_2160.thumbnail(size_3840_2160)
image_thumbnail_3840_2160.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_thumbnail_3840_2160' + extension)

######## CROPPING IMAGE
print('[image pre-processing] cropping')
cropped_image = original_image.crop((150, 200, 600, 600))
cropped_image.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_cropped' + extension)
cropped_image_1 = original_image.crop((250, 300, 700, 700))
cropped_image.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_cropped_1' + extension)
cropped_image_2 = original_image.crop((300, 400, 1200, 1200))
cropped_image.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_cropped_2' + extension)
cropped_image_3 = original_image.crop((375, 500, 1500, 1500))
cropped_image.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_cropped_3' + extension)

######## JPEG COMPRESSION
print('[image pre-processing] jpeg compression')
jpeg_quality = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
try:
    for quality in jpeg_quality:
        path = lifeeasy.working_dir() + '/image_dataset/' + 'image_jpeg_compress_' + str(quality) + '.jpg'
        original_image.save(path, quality=quality)
except:
    print('[error] Error while converting to jpg')

######## WATERMARK
print('[image pre-processing] watermark')
python_logo_110 = Image.open(lifeeasy.working_dir() + '/python_logo/python_logo_110.png')
image_watermark_110 = original_image.copy()
position = ((image_watermark_110.width - python_logo_110.width), (image_watermark_110.height - python_logo_110.height))
image_watermark_110.paste(python_logo_110, position)
image_watermark_110.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_watermark_110' + extension)
python_logo_240 = Image.open(lifeeasy.working_dir() + '/python_logo/python_logo_240.png')
image_watermark_240 = original_image.copy()
position = ((image_watermark_240.width - python_logo_240.width), (image_watermark_240.height - python_logo_240.height))
image_watermark_240.paste(python_logo_240, position)
image_watermark_240.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_watermark_240' + extension)
python_logo_480 = Image.open(lifeeasy.working_dir() + '/python_logo/python_logo_480.png')
image_watermark_480 = original_image.copy()
position = ((image_watermark_480.width - python_logo_480.width), (image_watermark_480.height - python_logo_480.height))
image_watermark_480.paste(python_logo_480, position)
image_watermark_480.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_watermark_480' + extension)
python_logo_600 = Image.open(lifeeasy.working_dir() + '/python_logo/python_logo_600.png')
image_watermark_600 = original_image.copy()
position = ((image_watermark_600.width - python_logo_600.width), (image_watermark_600.height - python_logo_600.height))
image_watermark_600.paste(python_logo_600, position)
image_watermark_600.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_watermark_600' + extension)
python_logo_768 = Image.open(lifeeasy.working_dir() + '/python_logo/python_logo_768.png')
image_watermark_768 = original_image.copy()
position = ((image_watermark_768.width - python_logo_768.width), (image_watermark_768.height - python_logo_768.height))
image_watermark_768.paste(python_logo_768, position)
image_watermark_768.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_watermark_768' + extension)
python_logo_1024 = Image.open(lifeeasy.working_dir() + '/python_logo/python_logo_1024.png')
image_watermark_1024 = original_image.copy()
position = ((image_watermark_1024.width - python_logo_1024.width), (image_watermark_1024.height - python_logo_1024.height))
image_watermark_1024.paste(python_logo_1024, position)
image_watermark_1024.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_watermark_1024' + extension)

######## WATERMARK WITH ALPHA
print('[image pre-processing] watermark with alpha')
python_logo_110 = Image.open(lifeeasy.working_dir() + '/python_logo/python_logo_110.png')
image_watermark_alpha_110 = original_image.copy()
position = ((image_watermark_alpha_110.width - python_logo_110.width), (image_watermark_alpha_110.height - python_logo_110.height))
image_watermark_alpha_110.paste(python_logo_110, position, python_logo_110)
image_watermark_alpha_110.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_watermark_alpha_110' + extension)
python_logo_240 = Image.open(lifeeasy.working_dir() + '/python_logo/python_logo_240.png')
image_watermark_alpha_240 = original_image.copy()
position = ((image_watermark_alpha_240.width - python_logo_240.width), (image_watermark_alpha_240.height - python_logo_240.height))
image_watermark_alpha_240.paste(python_logo_240, position,python_logo_240)
image_watermark_alpha_240.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_watermark_alpha_240' + extension)
python_logo_480 = Image.open(lifeeasy.working_dir() + '/python_logo/python_logo_480.png')
image_watermark_alpha_480 = original_image.copy()
position = ((image_watermark_alpha_480.width - python_logo_480.width), (image_watermark_alpha_480.height - python_logo_480.height))
image_watermark_alpha_480.paste(python_logo_480, position,python_logo_480)
image_watermark_alpha_480.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_watermark_alpha_480' + extension)
python_logo_600 = Image.open(lifeeasy.working_dir() + '/python_logo/python_logo_600.png')
image_watermark_alpha_600 = original_image.copy()
position = ((image_watermark_alpha_600.width - python_logo_600.width), (image_watermark_alpha_600.height - python_logo_600.height))
image_watermark_alpha_600.paste(python_logo_600, position,python_logo_600)
image_watermark_alpha_600.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_watermark_alpha_600' + extension)
python_logo_768 = Image.open(lifeeasy.working_dir() + '/python_logo/python_logo_768.png')
image_watermark_alpha_768 = original_image.copy()
position = ((image_watermark_alpha_768.width - python_logo_768.width), (image_watermark_alpha_768.height - python_logo_768.height))
image_watermark_alpha_768.paste(python_logo_768, position,python_logo_768)
image_watermark_alpha_768.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_watermark_alpha_768' + extension)
python_logo_1024 = Image.open(lifeeasy.working_dir() + '/python_logo/python_logo_1024.png')
image_watermark_alpha_1024 = original_image.copy()
position = ((image_watermark_alpha_1024.width - python_logo_1024.width), (image_watermark_alpha_1024.height - python_logo_1024.height))
image_watermark_alpha_1024.paste(python_logo_1024, position,python_logo_1024)
image_watermark_alpha_1024.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_watermark_alpha_1024' + extension)

######### NOISE
numpy_array_image = np.asarray(original_image)
print('[image pre-processing] noise - gaussian')
gaussian_array = noisy('gauss', numpy_array_image)
gaussian = Image.fromarray((gaussian_array * 255).astype(np.uint8))
gaussian.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_gaussian' + extension)

print('[image pre-processing] noise - salt and pepper')
salt_and_pepper_array = noisy('s&p', numpy_array_image)
salt_and_pepper = Image.fromarray((salt_and_pepper_array * 255).astype(np.uint8))
salt_and_pepper.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_salt_and_pepper' + extension)

print('[image pre-processing] noise - poisson')
poisson_array = noisy('poisson', numpy_array_image)
poisson = Image.fromarray((poisson_array * 255).astype(np.uint8))
poisson.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_poisson' + extension)

print('[image pre-processing] noise - speckle')
speckle_array = noisy('speckle', numpy_array_image)
speckle = Image.fromarray((speckle_array * 255).astype(np.uint8))
speckle.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_speckle' + extension)


######## INVERTING
print('[image pre-processing] inverting')
image_inverted = ImageOps.invert(original_image)
image_inverted.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_inverted' + extension)

image_inverted = ImageOps.invert(salt_and_pepper)
image_inverted.save(lifeeasy.working_dir() + '/image_dataset/' + 'image_salt_and_pepper_inverted' + extension)
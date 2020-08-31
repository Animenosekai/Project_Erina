"""
Image hashing test for the Erina Project

@author: Anime no Sekai
Erina Project - 2020
"""

import filecenter
import lifeeasy
import imagehash
from PIL import Image
from time import process_time

results = {}
results_hash = {}

#algorithm = 'aHash'
#algorithm = 'cHash'
#algorithm = 'dHash'
#algorithm = 'dHash_vertical'
#algorithm = 'pHash'
#algorithm = 'pHash_simple'
#algorithm = 'wHash'

algorithms = ['aHash', 'cHash', 'dHash', 'dHash_vertical', 'pHash', 'pHash_simple', 'wHash']

print('[hash test] Hashing...')
for algorithm in algorithms:
    print('Algorithm: ' + algorithm)
    start_total_process_time = process_time()
    for image in filecenter.files_in_dir(lifeeasy.working_dir() + '/image_dataset'):
        print('[hash test] Image: ' + image)
        start_total_image_process_time = process_time()
        testing_image = Image.open(lifeeasy.working_dir() + '/image_dataset/' + image)
        start_image_hash_process_time = process_time()
        if algorithm == 'aHash':
            image_hash = imagehash.average_hash(testing_image) # Needs to be a PIL instance
        elif algorithm == 'cHash':
            image_hash = imagehash.colorhash(testing_image)
        elif algorithm == 'dHash':
            image_hash = imagehash.dhash(testing_image)
        elif algorithm == 'dHash_vertical':
            image_hash = imagehash.dhash_vertical(testing_image)
        elif algorithm == 'pHash':
            image_hash = imagehash.phash(testing_image)
        elif algorithm == 'pHash_simple':
            image_hash = imagehash.phash_simple(testing_image)
        elif algorithm == 'wHash':
            image_hash = imagehash.whash(testing_image)

        end_total_image_process_time = process_time()

        results_hash[image] = str(image_hash)

        results[image] = {'hash': image_hash, 'hash_string': str(image_hash), 'start_total_image_process_time': start_image_hash_process_time, 'start_image_hash_process_time': start_image_hash_process_time, 'end_total_image_process_time': end_total_image_process_time, 'image_process_time': end_total_image_process_time - start_total_image_process_time, 'image_hash_process_time': end_total_image_process_time - start_image_hash_process_time}

    end_total_process_time = process_time()

    results['start_total_process_time'] = start_total_process_time
    results['end_total_process_time'] =  end_total_process_time
    results['total_process_time'] = end_total_process_time - start_total_process_time

    print('[hash test] Writing the results...')
    lifeeasy.write_file('results' + algorithm + '.txt', [str(results), '', str(results_hash)])
    print('[hash test] Done!')
    print('[hash test] Total process time: ' + str(results['total_process_time']) + ' sec')
    print('')
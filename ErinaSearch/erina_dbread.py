"""
Anime Database Reading/Parsing API for the Erina Project


NOT USED ANYMORE --> Migrated to ErinaParser

KEPT FOR FUTURE ERINAPARSER UPDATES

@author: Anime no Sekai
Erina Project - 2020
"""
import Erina.env_information as env_information
from ErinaSearch import result_python_translation

anilist_cache_path = env_information.erina_dir + '/ErinaCaches/AniList_Cache/'
erina_cache_path = env_information.erina_dir + '/ErinaCaches/Erina_Cache/'
erina_database_path = env_information.erina_dir + '/ErinaDB/ErinaDatabase/'
tracemoe_cache_path = env_information.erina_dir + '/ErinaCaches/TraceMoe_Cache/'
saucenao_cache_path = env_information.erina_dir + '/ErinaCaches/SauceNAO_Cache/'
iqdb_cache_path = env_information.erina_dir + '/ErinaCaches/IQDB_Cache/'


def read_iqdb_cache_data(filename):
    """
    Converts IQDB Caches data into a Python Dictionary\n
    © Anime no Sekai - 2020\n
    Project Erina
    """
    cache_result = {}
    cache_result['error'] = False
    database_results_keys = ['gelbooru_results', 'danbooru_results', 'zerochan_results', 'konachan_results', 'yandere_results', 'anime_pictures_results', 'eshuushuu_results']
    for key in database_results_keys:
        cache_result[key] = {}
    def remove_other_databases(database_result_key):
        for key in database_results_keys:
            if key == database_result_key:
                continue
            else:
                cache_result.pop(key, None)
    try:
        cache_file = open(iqdb_cache_path + filename)
        line = cache_file.readline()
        while line != '' :
            current_line = line.replace('\n', '')
            if current_line[:10] == 'IQDB Tags:':
                cache_result['iqdb_tags'] = current_line[11:]
            elif current_line[:4] == 'URL:':
                cache_result['url'] = current_line[5:]
            elif current_line[:5] == 'Size:':
                cache_result['size'] = current_line[6:]
            elif current_line[:7] == 'isSafe:':
                cache_result['is_safe'] = current_line[8:]
            elif current_line[:11] == 'Similarity:':
                cache_result['similarity'] = current_line[12:]
            elif current_line[:9] == 'Database:':
                cache_result['database'] = current_line[10:]
                if cache_result['database'] == 'gelbooru':
                    remove_other_databases('gelbooru_results')
                elif cache_result['database'] == 'danbooru':
                    remove_other_databases('danbooru_results')
                elif cache_result['database'] == 'zerochan':
                    remove_other_databases('zerochan_results')
                elif cache_result['database'] == 'konachan':
                    remove_other_databases('konachan_results')
                elif cache_result['database'] == 'yandere':
                    remove_other_databases('yandere_results')
                elif cache_result['database'] == 'anime_pictures':
                    remove_other_databases('anime_pictures_results')
                elif cache_result['database'] == 'e_shuushuu':
                    remove_other_databases('e_shuushuu_results')
                        
            ##### GELBOORU
            elif current_line[:20] == 'Gelbooru Characters:':
                data_str = current_line[21:]
                data = data_str.split(':::')
                cache_result['gelbooru_results']['characters'] = data
            elif current_line[:20] == 'Gelbooru Copyrights:':
                data_str = current_line[21:]
                data = data_str.split(':::')
                cache_result['gelbooru_results']['copyrights'] = data
            elif current_line[:19] == 'Gelbooru Metadatas:':
                data_str = current_line[20:]
                data = data_str.split(':::')
                cache_result['gelbooru_results']['metadatas'] = data
            elif current_line[:14] == 'Gelbooru Tags:':
                data_str = current_line[15:]
                data = data_str.split(':::')
                cache_result['gelbooru_results']['tags'] = data
            elif current_line[:12] == 'Gelbooru ID:':
                cache_result['gelbooru_results']['id'] = current_line[13:]
            elif current_line[:14] == 'Gelbooru Size:':
                cache_result['gelbooru_results']['size'] = current_line[15:]
            elif current_line[:16] == 'Gelbooru Source:':
                cache_result['gelbooru_results']['source'] = current_line[17:]
            elif current_line[:16] == 'Gelbooru Rating:':
                cache_result['gelbooru_results']['rating'] = current_line[17:]
            elif current_line[:14] == 'Gelbooru Date:':
                cache_result['gelbooru_results']['date'] = current_line[15:]
            elif current_line[:18] == 'Gelbooru Uploader:':
                cache_result['gelbooru_results']['uploader'] = current_line[19:]
            elif current_line[:15] == 'Gelbooru Score:':
                cache_result['gelbooru_results']['score'] = current_line[16:]

            ##### DANBOORU
            elif current_line[:17] == 'Danbooru Artists:':
                data_str = current_line[18:]
                data = data_str.split(':::')
                cache_result['danbooru_results']['artists'] = data
            elif current_line[:20] == 'Danbooru Characters:':
                data_str = current_line[21:]
                data = data_str.split(':::')
                cache_result['danbooru_results']['characters'] = data
            elif current_line[:20] == 'Danbooru Copyrights:':
                data_str = current_line[21:]
                data = data_str.split(':::')
                cache_result['danbooru_results']['copyrights'] = data
            elif current_line[:19] == 'Danbooru Metadatas:':
                data_str = current_line[20:]
                data = data_str.split(':::')
                cache_result['danbooru_results']['metadatas'] = data
            elif current_line[:14] == 'Danbooru Tags:':
                data_str = current_line[15:]
                data = data_str.split(':::')
                cache_result['danbooru_results']['tags'] = data
            elif current_line[:12] == 'Danbooru ID:':
                cache_result['danbooru_results']['id'] = current_line[13:]
            elif current_line[:18] == 'Danbooru Uploader:':
                cache_result['danbooru_results']['uploader'] = current_line[19:]
            elif current_line[:14] == 'Danbooru Date:':
                cache_result['danbooru_results']['date'] = current_line[15:]
            elif current_line[:22] == 'Danbooru Content Size:':
                cache_result['danbooru_results']['content_size'] = current_line[23:]
            elif current_line[:16] == 'Danbooru Format:':
                cache_result['danbooru_results']['format'] = current_line[17:]
            elif current_line[:14] == 'Danbooru Size:':
                cache_result['danbooru_results']['size'] = current_line[15:]
            elif current_line[:16] == 'Danbooru Source:':
                cache_result['danbooru_results']['source'] = current_line[17:]
            elif current_line[:16] == 'Danbooru Rating:':
                cache_result['danbooru_results']['rating'] = current_line[17:]
            elif current_line[:15] == 'Danbooru Score:':
                cache_result['danbooru_results']['score'] = current_line[16:]
            elif current_line[:19] == 'Danbooru Favorites:':
                cache_result['danbooru_results']['favorites'] = current_line[20:]
            elif current_line[:16] == 'Danbooru Status:':
                cache_result['danbooru_results']['status'] = current_line[17:]

            ##### ZEROCHAN
            elif current_line[:12] == 'Zerochan ID:':
                cache_result['zerochan_results']['id'] = current_line[13:]
            elif current_line[:18] == 'Zerochan Uploader:':
                cache_result['zerochan_results']['uploader'] = current_line[19:]
            elif current_line[:21] == 'Zerochan Content URL:':
                cache_result['zerochan_results']['content_url'] = current_line[22:]
            elif current_line[:19] == 'Zerochan Thumbnail:':
                cache_result['zerochan_results']['thumbnail'] = current_line[20:]
            elif current_line[:16] == 'Zerochan Format:':
                cache_result['zerochan_results']['format'] = current_line[17:]
            elif current_line[:19] == 'Zerochan Post Date:':
                cache_result['zerochan_results']['post_date'] = current_line[20:]
            elif current_line[:14] == 'Zerochan Name:':
                cache_result['zerochan_results']['name'] = current_line[15:]
            elif current_line[:15] == 'Zerochan Width:':
                cache_result['zerochan_results']['width'] = current_line[16:]
            elif current_line[:16] == 'Zerochan Height:':
                cache_result['zerochan_results']['height'] = current_line[17:]
            elif current_line[:22] == 'Zerochan Content Size:':
                cache_result['zerochan_results']['content_size'] = current_line[23:]
            elif current_line[:17] == 'Zerochan Mangaka:':
                cache_result['zerochan_results']['mangaka'] = current_line[18:]
            elif current_line[:16] == 'Zerochan Series:':
                cache_result['zerochan_results']['series'] = current_line[17:]
            elif current_line[:19] == 'Zerochan Character:':
                cache_result['zerochan_results']['character'] = current_line[20:]
            elif current_line[:16] == 'Zerochan Source:':
                cache_result['zerochan_results']['source'] = current_line[17:]

            ##### KONACHAN
            elif current_line[:20] == 'Konachan Copyrights:':
                data_str = current_line[21:]
                data = data_str.split(':::')
                cache_result['konachan_results']['copyrights'] = data
            elif current_line[:16] == 'Konachan Styles:':
                data_str = current_line[17:]
                data = data_str.split(':::')
                cache_result['konachan_results']['styles'] = data
            elif current_line[:20] == 'Konachan Artists:':
                data_str = current_line[21:]
                data = data_str.split(':::')
                cache_result['konachan_results']['artists'] = data
            elif current_line[:20] == 'Konachan Characters:':
                data_str = current_line[21:]
                data = data_str.split(':::')
                cache_result['konachan_results']['characters'] = data
            elif current_line[:14] == 'Konachan Tags:':
                data_str = current_line[15:]
                data = data_str.split(':::')
                cache_result['konachan_results']['tags'] = data
            elif current_line[:22] == 'Konachan Favorited By:':
                data_str = current_line[23:]
                data = data_str.split(':::')
                cache_result['konachan_results']['favorited_by'] = data
            elif current_line[:12] == 'Konachan ID:':
                cache_result['konachan_results']['id'] = current_line[13:]
            elif current_line[:14] == 'Konachan Size:':
                cache_result['konachan_results']['size'] = current_line[15:]
            elif current_line[:16] == 'Konachan Source:':
                cache_result['konachan_results']['source'] = current_line[17:]
            elif current_line[:16] == 'Konachan Rating:':
                cache_result['konachan_results']['rating'] = current_line[17:]
            elif current_line[:14] == 'Konachan Date:':
                cache_result['konachan_results']['date'] = current_line[15:]
            elif current_line[:18] == 'Konachan Uploader:':
                cache_result['konachan_results']['uploader'] = current_line[19:]
            elif current_line[:15] == 'Konachan Score:':
                cache_result['konachan_results']['score'] = current_line[16:]

            ##### YANDERE
            elif current_line[:19] == 'Yandere Copyrights:':
                data_str = current_line[20:]
                data = data_str.split(':::')
                cache_result['yandere_results']['copyrights'] = data
            elif current_line[:15] == 'Yandere Styles:':
                data_str = current_line[16:]
                data = data_str.split(':::')
                cache_result['yandere_results']['styles'] = data
            elif current_line[:19] == 'Yandere Artists:':
                data_str = current_line[20:]
                data = data_str.split(':::')
                cache_result['yandere_results']['artists'] = data
            elif current_line[:19] == 'Yandere Characters:':
                data_str = current_line[20:]
                data = data_str.split(':::')
                cache_result['yandere_results']['characters'] = data
            elif current_line[:13] == 'Yandere Tags:':
                data_str = current_line[14:]
                data = data_str.split(':::')
                cache_result['yandere_results']['tags'] = data
            elif current_line[:21] == 'Yandere Favorited By:':
                data_str = current_line[22:]
                data = data_str.split(':::')
                cache_result['yandere_results']['favorited_by'] = data
            elif current_line[:11] == 'Yandere ID:':
                cache_result['yandere_results']['id'] = current_line[12:]
            elif current_line[:13] == 'Yandere Size:':
                cache_result['yandere_results']['size'] = current_line[14:]
            elif current_line[:15] == 'Yandere Source:':
                cache_result['yandere_results']['source'] = current_line[16:]
            elif current_line[:15] == 'Yandere Rating:':
                cache_result['yandere_results']['rating'] = current_line[16:]
            elif current_line[:13] == 'Yandere Date:':
                cache_result['yandere_results']['date'] = current_line[14:]
            elif current_line[:17] == 'Yandere Uploader:':
                cache_result['yandere_results']['uploader'] = current_line[18:]
            elif current_line[:14] == 'Yandere Score:':
                cache_result['yandere_results']['score'] = current_line[15:]

            ##### ANIME-PICTURES
            elif current_line[:18] == 'Anime-Pictures ID:':
                cache_result['anime_pictures_results']['id'] = current_line[19:]
            elif current_line[:24] == 'Anime-Pictures Uploader:':
                cache_result['anime_pictures_results']['uploader'] = current_line[25:]
            elif current_line[:33] == 'Anime-Pictures Last Editing User:':
                cache_result['anime_pictures_results']['last_editing_user'] = current_line[34:]
            elif current_line[:25] == 'Anime-Pictures Post Date:':
                cache_result['anime_pictures_results']['post_date'] = current_line[26:]
            elif current_line[:30] == 'Anime-Pictures Published Date:':
                cache_result['anime_pictures_results']['published_date'] = current_line[31:]
            elif current_line[:30] == 'Anime-Pictures Download Count:':
                cache_result['anime_pictures_results']['download_count'] = current_line[31:]
            elif current_line[:20] == 'Anime-Pictures Size:':
                cache_result['anime_pictures_results']['size'] = current_line[21:]
            elif current_line[:28] == 'Anime-Pictures Aspect Ratio:':
                cache_result['anime_pictures_results']['aspect_ratio'] = current_line[29:]
            elif current_line[:28] == 'Anime-Pictures Content Size:':
                cache_result['anime_pictures_results']['content_size'] = current_line[29:]
            elif current_line[:32] == 'Anime-Pictures Artefacts Degree:':
                cache_result['anime_pictures_results']['artefacts_degree'] = current_line[33:]
            elif current_line[:29] == 'Anime-Pictures Smooth Degree:':
                cache_result['anime_pictures_results']['smoothness_degree'] = current_line[30:]
            elif current_line[:26] == 'Anime-Pictures Complexity:':
                cache_result['anime_pictures_results']['complexity'] = current_line[27:]
            elif current_line[:25] == 'Anime-Pictures Copyright:':
                cache_result['anime_pictures_results']['copyright'] = current_line[26:]
            elif current_line[:22] == 'Anime-Pictures Artist:':
                cache_result['anime_pictures_results']['artist'] = current_line[23:]
            elif current_line[:29] == 'Anime-Pictures Average Color:':
                data_str = current_line[30:]
                data = data_str.split(':::')
                cache_result['anime_pictures_results']['average_color'] = data
            elif current_line[:26] == 'Anime-Pictures References:':
                data_str = current_line[27:]
                data = data_str.split(':::')
                cache_result['anime_pictures_results']['references'] = data
            elif current_line[:23] == 'Anime-Pictures Objects:':
                data_str = current_line[24:]
                data = data_str.split(':::')
                cache_result['anime_pictures_results']['objects'] = data
            elif current_line[:30] == 'Anime-Pictures Similar Images:':
                data_str = current_line[31:]
                data = data_str.split(':::')
                cache_result['anime_pictures_results']['similar_images_id'] = data
            elif current_line[:28] == 'Anime-Pictures Artist Links:':
                data_str = current_line[29:]
                data = data_str.split(':::')
                cache_result['anime_pictures_results']['artist_links'] = data

            ##### E-SHUUSHUU
            elif current_line[:28] == 'E-Shuushuu Posting Uploader:':
                cache_result['e_shuushuu_results']['uploader'] = current_line[29:]
            elif current_line[:29] == 'E-Shuushuu Posting Post Date:':
                cache_result['e_shuushuu_results']['post_date'] = current_line[30:]
            elif current_line[:28] == 'E-Shuushuu Posting Filename:':
                cache_result['e_shuushuu_results']['filename'] = current_line[29:]
            elif current_line[:37] == 'E-Shuushuu Posting Original Filename:':
                cache_result['e_shuushuu_results']['original_filename'] = current_line[38:]
            elif current_line[:32] == 'E-Shuushuu Posting Content Size:':
                cache_result['e_shuushuu_results']['content_size'] = current_line[33:]
            elif current_line[:24] == 'E-Shuushuu Posting Size:':
                cache_result['e_shuushuu_results']['size'] = current_line[25:]
            elif current_line[:29] == 'E-Shuushuu Posting Favorites:':
                cache_result['e_shuushuu_results']['favorites'] = current_line[30:]
            elif current_line[:32] == 'E-Shuushuu Posting Image Rating:':
                cache_result['e_shuushuu_results']['rating'] = current_line[33:]
            elif current_line[:16] == 'E-Shuushuu Tags:':
                data_str = current_line[17:]
                data = data_str.split(':::')
                cache_result['e_shuushuu_results']['tags'] = data
            elif current_line[:19] == 'E-Shuushuu Sources:':
                data_str = current_line[20:]
                data = data_str.split(':::')
                cache_result['e_shuushuu_results']['sources'] = data
            elif current_line[:22] == 'E-Shuushuu Characters:':
                data_str = current_line[23:]
                data = data_str.split(':::')
                cache_result['e_shuushuu_results']['characters'] = data
            elif current_line[:19] == 'E-Shuushuu Artists:':
                data_str = current_line[20:]
                data = data_str.split(':::')
                cache_result['e_shuushuu_results']['artists'] = data

            elif current_line[:16] == 'Cache Timestamp:':
                cache_result['cache_timestamp'] = current_line[17:]
            elif current_line[:28] == 'Cache Timestamp (formatted):':
                cache_result['cache_timestamp_formatted'] = current_line[29:]
            line = cache_file.readline()
        
        cache_file.close()
    except:
        cache_result['error'] = True
        cache_result['error_details'] = '<iqdb_cache_data_parsing>'
    return result_python_translation.verify_dict(cache_result)
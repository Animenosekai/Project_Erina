"""
Anime Database Reading/Parsing API for the Erina Project

@author: Anime no Sekai
Erina Project - 2020
"""
import sys
sys.path.append('.')
sys.path.append('..')

import env_information
import erina_log
from ErinaSearch import result_python_translation

anilist_cache_path = env_information.erina_dir + '/ErinaCaches/AniList_Cache/'
erina_cache_path = env_information.erina_dir + '/ErinaCaches/Erina_Cache/'
erina_database_path = env_information.erina_dir + '/ErinaDB/ErinaDatabase/'
tracemoe_cache_path = env_information.erina_dir + '/ErinaCaches/TraceMoe_Cache/'
saucenao_cache_path = env_information.erina_dir + '/ErinaCaches/SauceNAO_Cache/'
iqdb_cache_path = env_information.erina_dir + '/ErinaCaches/IQDB_Cache/'

def read_anilist_cache_data(filename, silent_search=False):
    """
    Converts AniList Caches data into a Python Dictionary
    © Anime no Sekai - 2020
    Project Erina
    """
    if not silent_search:
        erina_log.logsearch(f'Reading AniList cache data... ({filename})')
    cache_result = {}
    cache_result['error'] = False
    try:
        cache_result['streaming_links'] = []
        cache_result['external_links'] = []
        cache_result['studios'] = []
        cache_result['tags'] = []
        cache_result['relations'] = []
        cache_result['characters'] = []
        cache_result['staff'] = []
        cache_result['recommendations'] = []
        iteration = 0
        cache_file = open(anilist_cache_path + filename)
        line = cache_file.readline()
        while line != '' :
            current_line = line.replace('\n', '')
            if current_line[:11] == 'AniList ID:':
                cache_result['anilist_id'] = current_line[12:]
            elif current_line[:15] == 'MyAnimeList ID:':
                cache_result['myanimelist_id'] = current_line[16:]
            elif current_line[:13] == 'Romaji Title:':
                cache_result['title'] = current_line[14:]
                cache_result['title_romaji'] = current_line[14:]
            elif current_line[:14] == 'English Title:':
                cache_result['title_english'] = current_line[15:]
            elif current_line[:13] == 'Native Title:':
                cache_result['title_native'] = current_line[14:]
            elif current_line[:5] == 'Type:':
                cache_result['type'] = current_line[6:]
            elif current_line[:7] == 'Format:':
                cache_result['format'] = current_line[8:]
            elif current_line[:7] == 'Status:':
                cache_result['status'] = current_line[8:]
            elif current_line[:12] == 'Description:':
                cache_result['description'] = current_line[13:]
            elif current_line[:7] == 'Season:':
                cache_result['season'] = current_line[8:]
            elif current_line[:5] == 'Year:':
                cache_result['year'] = current_line[6:]
            elif current_line[:9] == 'Episodes:':
                cache_result['episodes'] = current_line[10:]
            elif current_line[:17] == 'Average Duration:':
                cache_result['average_duration'] = current_line[18:]
            elif current_line[:27] == 'First Episode Release Date:':
                cache_result['first_episode_release_date'] = current_line[28:]
            elif current_line[:35] == '[First Episode Release Date - Year]':
                cache_result['first_episode_release_date_year'] = current_line[36:]
            elif current_line[:36] == '[First Episode Release Date - Month]':
                cache_result['first_episode_release_date_month'] = current_line[37:]
            elif current_line[:34] == '[First Episode Release Date - Day]':
                cache_result['first_episode_release_date_day'] = current_line[35:]
            elif current_line[:26] == 'Last Episode Release Date:':
                cache_result['last_episode_release_date'] = current_line[27:]
            elif current_line[:34] == '[Last Episode Release Date - Year]':
                cache_result['last_episode_release_date_year'] = current_line[35:]
            elif current_line[:35] == '[Last Episode Release Date - Month]':
                cache_result['last_episode_release_date_month'] = current_line[36:]
            elif current_line[:33] == '[Last Episode Release Date - Day]':
                cache_result['last_episode_release_date_day'] = current_line[34:]
            elif current_line[:8] == 'Country:':
                cache_result['country'] = current_line[9:]
            elif current_line[:18] == 'Source Media Type:':
                cache_result['source_media_type'] = current_line[19:]
            elif current_line[:9] == 'Licensed?':
                cache_result['is_licensed'] = result_python_translation.verify_if_boolean(current_line[10:])
            elif current_line[:7] == 'Hentai?':
                cache_result['is_hentai'] = result_python_translation.verify_if_boolean(current_line[8:])
            elif current_line[:16] == 'Twitter Hashtag:':
                cache_result['twitter_hashtag'] = current_line[17:]
            elif current_line[:14] == 'Average Score:':
                cache_result['average_score'] = current_line[15:]
            elif current_line[:12] == 'Cover Image:':
                cache_result['cover_image'] = current_line[13:]
            elif current_line[:20] == 'Average Cover Color:':
                cache_result['average_cover_color'] = current_line[21:]
            elif current_line[:13] == 'Banner Image:':
                cache_result['banner_image'] = current_line[14:]
            elif current_line[:8] == 'Trailer:':
                cache_result['trailer'] = current_line[9:]
            elif current_line[:6] == 'Title:':
                cache_result['title'] = current_line[7:]
            elif current_line[:7] == 'Genres:':
                genres_str = current_line[8:]
                genres = genres_str.split(':::')
                cache_result['genres'] = genres
            elif current_line[:21] == 'Alternative Title(s):':
                alternatives_str = current_line[22:]
                alternatives = alternatives_str.split(':::')
                cache_result['alternative_titles'] = alternatives
            elif current_line[:8] == '[STUDIO]':
                studio_str = current_line[9:]
                studio_str_list = []
                studio_str_partitionned = studio_str.partition('｜｜｜')
                studio_str_list.append(studio_str_partitionned[0])
                studio_str_partitionned = studio_str_partitionned[2].partition('｜｜｜')
                studio_str_list.append(studio_str_partitionned[0])
                studio_str_partitionned = studio_str_partitionned[2].partition('｜｜｜')
                studio_str_list.append(studio_str_partitionned[0])
                studio_str_list.append(studio_str_partitionned[2])
                studio_dict = {'name': studio_str_list[2],'is_main': result_python_translation.verify_if_boolean(studio_str_list[0]), 'is_animation_studio': result_python_translation.verify_if_boolean(studio_str_list[3]), 'anilist_id': studio_str_list[1]}
                cache_result['studios'].append(studio_dict)
            elif current_line[:5] == '[TAG]':
                tag_str = current_line[6:]
                tag_str_list = []
                tag_str_partitionned = tag_str.partition('｜｜｜') 
                tag_str_list.append(tag_str_partitionned[0])
                tag_str_partitionned = tag_str_partitionned[2].partition('｜｜｜')
                tag_str_list.append(tag_str_partitionned[0])
                tag_str_partitionned = tag_str_partitionned[2].partition('｜｜｜')
                tag_str_list.append(tag_str_partitionned[0])
                tag_str_partitionned = tag_str_partitionned[2].partition('｜｜｜')
                tag_str_list.append(tag_str_partitionned[0])
                tag_str_list.append(tag_str_partitionned[2])
                tag_dict = {'name': tag_str_list[0], 'rank': tag_str_list[1], 'is_anime_spoiler': result_python_translation.verify_if_boolean(tag_str_list[2]), 'is_adult': result_python_translation.verify_if_boolean(tag_str_list[3]), 'category': tag_str_list[4]}
                cache_result['tags'].append(tag_dict)
            elif current_line[:10] == '[RELATION]':
                relation_str = current_line[11:]
                relation_str_list = []
                relation_str_partitionned = relation_str.partition('｜｜｜')
                relation_str_list.append(relation_str_partitionned[0])
                relation_str_partitionned = relation_str_partitionned[2].partition('｜｜｜')
                relation_str_list.append(relation_str_partitionned[0])
                relation_str_list.append(relation_str_partitionned[2])
                relation_dict = {'relation_type': relation_str_list[0], 'anilist_id': relation_str_list[1], 'title': relation_str_list[2]}
                cache_result['relations'].append(relation_dict)
            elif current_line[:11] == '[CHARACTER]':
                character_str = current_line[12:]
                character_str_list = []
                character_str_partitionned = character_str.partition('｜｜｜')
                character_str_list.append(character_str_partitionned[0])
                character_str_partitionned = character_str_partitionned[2].partition('｜｜｜')
                character_str_list.append(character_str_partitionned[0])
                character_str_partitionned = character_str_partitionned[2].partition('｜｜｜')
                character_str_list.append(character_str_partitionned[0])
                character_str_list.append(character_str_partitionned[2])
                character_dict = {'role': character_str_list[0], 'anilist_id': character_str_list[1], 'full_name': character_str_list[2], 'native_name': character_str_list[3]}
                cache_result['characters'].append(character_dict)
            elif current_line[:7] == '[STAFF]':
                staff_str = current_line[8:]
                staff_str_list = []
                staff_str_partitionned = staff_str.partition('｜｜｜')
                staff_str_list.append(staff_str_partitionned[0])
                staff_str_partitionned = staff_str_partitionned[2].partition('｜｜｜')
                staff_str_list.append(staff_str_partitionned[0])
                staff_str_partitionned = staff_str_partitionned[2].partition('｜｜｜')
                staff_str_list.append(staff_str_partitionned[0])
                staff_str_list.append(staff_str_partitionned[2])
                staff_dict = {'role': staff_str_list[0], 'anilist_id': staff_str_list[1], 'full_name': staff_str_list[2], 'native_name': staff_str_list[3]}
                cache_result['staff'].append(staff_dict)
            elif current_line[:16] == '[RECOMMENDATION]':
                recommendation_str = current_line[17:]
                recommendation_str_list = []
                recommendation_str_partitionned = recommendation_str.partition('｜｜｜')
                recommendation_str_list.append(recommendation_str_partitionned[0])
                recommendation_str_list.append(recommendation_str_partitionned[2])
                recommendation_dict = {'anilist_id': recommendation_str_list[0], 'title': recommendation_str_list[1]}
                cache_result['recommendations'].append(recommendation_dict)
            elif current_line[:16] == '[streaming link]':
                iteration += 1
                line_partition_link = current_line[17:].partition(': http')
                link = 'http' + line_partition_link[2]
                if link.find('www.crunchyroll.com') != -1:
                    before_link_partition = line_partition_link[0].partition(' - ')
                    episode = before_link_partition[0].replace('Episode ', '')
                    episode_title = before_link_partition[2]
                    full_title = line_partition_link[0]
                else:
                    episode = str(iteration)
                    episode_title = line_partition_link[0]
                    full_title = line_partition_link[0]
                current_streaming_link = {'link': link, 'episode': episode, 'episode_title': episode_title, 'full_title': full_title}
                cache_result['streaming_links'].append(current_streaming_link)
            elif current_line[:15] == '[external link]':
                line_partition = current_line[16:].partition(': http')
                current_external_link = {'site': line_partition[0], 'url': 'http' + line_partition[2]}
                cache_result['external_links'].append(current_external_link)
            elif current_line[:16] == 'Cache Timestamp:':
                cache_result['cache_timestamp'] = current_line[17:]
            elif current_line[:28] == 'Cache Timestamp (formatted):':
                cache_result['cache_timestamp_formatted'] = current_line[29:]
            line = cache_file.readline()
        cache_file.close()
    except:
        erina_log.logerror('[ErinaSearch] Error while reading AniList Cache Data')
        cache_result['error'] = True
        cache_result['error_details'] = '<anilist_cache_data_parsing>'
    return result_python_translation.verify_dict(cache_result)

def read_tracemoe_cache_data(filename):
    """
    Converts TraceMOE Caches data into a Python Dictionary
    © Anime no Sekai - 2020
    Project Erina
    """
    erina_log.logsearch(f'Reading trace.moe cache data... ({filename})')
    cache_result = {}
    cache_result['error'] = False
    try:
        cache_file = open(tracemoe_cache_path + filename)
        line = cache_file.readline()
        while line != '' :
            current_line = line.replace('\n', '')
            if current_line[:11] == 'AniList ID:':
                cache_result['anilist_id'] = current_line[12:]
            elif current_line[:6] == 'Title:':
                cache_result['title'] = current_line[7:]
            elif current_line[:7] == 'Season:':
                cache_result['season'] = current_line[8:]
            elif current_line[:8] == 'Episode:':
                cache_result['episode'] = current_line[9:]
            elif current_line[:13] == 'Title Romaji:':
                cache_result['title_romaji'] = current_line[14:]
            elif current_line[:6] == 'Anime:':
                cache_result['anime'] = current_line[7:]
            elif current_line[:15] == 'MyAnimeList ID:':
                cache_result['myanimelist_id'] = current_line[16:]
            elif current_line[:8] == 'isAdult:':
                cache_result['is_adult'] = result_python_translation.verify_if_boolean(current_line[9:])
            elif current_line[:9] == 'Filename:':
                cache_result['filename'] = current_line[10:]
            elif current_line[:5] == 'From:':
                cache_result['from'] = current_line[6:]
            elif current_line[:3] == 'To:':
                cache_result['to'] = current_line[4:]
            elif current_line[:3] == 'At:':
                cache_result['at'] = current_line[4:]
            elif current_line[:17] == 'From (formatted):':
                cache_result['from_formatted'] = current_line[18:]
            elif current_line[:15] == 'To (formatted):':
                cache_result['to_formatted'] = current_line[16:]
            elif current_line[:15] == 'At (formatted):':
                cache_result['at_formatted'] = current_line[16:]
            elif current_line[:22] == 'Similarity/Confidence:':
                cache_result['similarity'] = float(current_line[23:])
            elif current_line[:11] == 'TokenThumb:':
                cache_result['tokenthumb'] = current_line[12:]
            elif current_line[:13] == 'Title Native:':
                cache_result['title_native'] = current_line[14:]
            elif current_line[:14] == 'Title Chinese:':
                cache_result['title_chinese'] = current_line[15:]
            elif current_line[:14] == 'Title English:':
                cache_result['title_english'] = current_line[15:]
            elif current_line[:9] == 'Synonyms:':
                synonyms_str = current_line[10:]
                synonyms = synonyms_str.split(':::')
                cache_result['synonyms'] = synonyms
            elif current_line[:17] == 'Synonyms Chinese:':
                synonyms_chinese_str = current_line[18:]
                synonyms_chinese = synonyms_chinese_str.split(':::')
                cache_result['synonyms_chinese'] = synonyms_chinese
            elif current_line[:16] == 'Cache Timestamp:':
                cache_result['cache_timestamp'] = current_line[17:]
            elif current_line[:28] == 'Cache Timestamp (formatted):':
                cache_result['cache_timestamp_formatted'] = current_line[29:]
            line = cache_file.readline()
        cache_file.close()
    except:
        erina_log.logerror('[ErinaSearch] Error while reading TraceMOE Cache Data')
        cache_result['error'] = True
        cache_result['error_details'] = '<tracemoe_cache_data_parsing>'
    return result_python_translation.verify_dict(cache_result)

def read_saucenao_cache_data(filename):
    """
    Converts SauceNAO Cache data into a Python Dictionary
    © Anime no Sekai - 2020
    Project Erina
    """
    erina_log.logsearch(f'Reading SauceNAO Cache data... ({str(filename)})')
    cache_result = {}
    cache_result['error'] = False
    cache_result['is_anime'] = False
    cache_result['is_manga'] = False
    try:
        cache_file = open(saucenao_cache_path + filename)
        line = cache_file.readline()
        while line != '':
            current_line = line.replace('\n', '')
            if current_line[:11] == 'Similarity:':
                cache_result['similarity'] = float(current_line[12:])
            elif current_line[:9] == 'Index ID:':
                cache_result['index_id'] = current_line[10:]
            elif current_line[:11] == 'Index Name:':
                cache_result['index_name'] = current_line[12:]
            elif current_line[:6] == 'Title:':
                cache_result['title'] = current_line[7:]
            elif current_line[:4] == 'URL:':
                cache_result['url'] = current_line[5:]
            elif current_line[:7] == 'Author:':
                cache_result['author'] = current_line[8:]
            elif current_line[:10] == 'Thumbnail:':
                cache_result['thumbnail'] = current_line[11:]
            elif current_line[:8] == 'isManga:':
                cache_result['is_manga'] = current_line[9:]
            elif current_line[:5] == 'Part:':
                cache_result['part'] = current_line[6:]
            elif current_line[:8] == 'isAnime:':
                cache_result['is_anime'] = current_line[9:]
            elif current_line[:8] == 'Episode:':
                cache_result['episode'] = current_line[9:]
            elif current_line[:5] == 'Year:':
                cache_result['year'] = current_line[6:]
            elif current_line[:15] == 'Estimated Time:':
                cache_result['estimated_time'] = current_line[16:]
            elif current_line[:16] == 'Cache Timestamp:':
                cache_result['cache_timestamp'] = current_line[17:]
            elif current_line[:28] == 'Cache Timestamp (formatted):':
                cache_result['cache_timestamp_formatted'] = current_line[29:]
            line = cache_file.readline()
        
        cache_file.close()
    except:
        erina_log.logerror('[ErinaSearch] Error while reading SauceNAO Cache Data')
        cache_result['error'] = True
        cache_result['error_details'] = '<saucenao_cache_data_parsing>'
    return result_python_translation.verify_dict(cache_result)

def read_iqdb_cache_data(filename):
    """
    Converts IQDB Caches data into a Python Dictionary\n
    © Anime no Sekai - 2020\n
    Project Erina
    """
    erina_log.logsearch(f'Reading IQDB cache data... ({filename})')
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
        erina_log.logerror('[ErinaSearch] Error while reading IQDB Cache Data')
        cache_result['error'] = True
        cache_result['error_details'] = '<iqdb_cache_data_parsing>'
    return result_python_translation.verify_dict(cache_result)




def read_erina_cache_data(filename):
    """
    Converts Erina Database Cache data into a Python Dictionary
    © Anime no Sekai - 2020
    Project Erina
    """
    erina_log.logsearch(f'Reading Erina Database Cache data... ({filename})')
    cache_result = {}
    cache_result['error'] = False
    try:
        cache_file = open(erina_cache_path + filename)
        line = cache_file.readline()
        while line != '' :
            current_line = line.replace('\n', '')
            if current_line[:5] == 'Path:':
                cache_result['database_path'] = current_line[6:]
            elif current_line[:5] == 'Hash:':
                cache_result['hash'] = current_line[6:]
            elif current_line[:11] == 'Similarity:':
                cache_result['similarity'] = float(current_line[12:])
            elif current_line[:16] == 'Cache Timestamp:':
                cache_result['cache_timestamp'] = current_line[17:]
            elif current_line[:28] == 'Cache Timestamp (formatted):':
                cache_result['cache_timestamp_formatted'] = current_line[29:]
            line = cache_file.readline()
        cache_file.close()
    except:
        erina_log.logerror('[ErinaSearch] Error while reading Erina Cache data')
        cache_result['error'] = True
        cache_result['error_details'] = '<erina_cache_data_parsing>'
    return result_python_translation.verify_dict(cache_result)


def read_erina_database_data(database_path):
    """
    Converts Erina Database data into a Python Dictionary
    © Anime no Sekai - 2020
    Project Erina
    """
    erina_log.logsearch(f'Reading Erina Database data... ({database_path})')
    cache_result = {}
    cache_result['error'] = False
    try:
        cache_file = open(erina_database_path + database_path)
        line = cache_file.readline()
        while line != '' :
            current_line = line.replace('\n', '')
            if current_line[:11] == 'AniList ID:':
                cache_result['anilist_id'] = current_line[12:]
            elif current_line[:6] == 'Anime:':
                cache_result['anime'] = current_line[7:]
            elif current_line[:7] == 'Season:':
                cache_result['season'] = current_line[8:]
            elif current_line[:8] == 'Episode:':
                cache_result['episode'] = current_line[9:]
            elif current_line[:12] == 'First Frame:':
                cache_result['first_frame'] = current_line[13:]
            elif current_line[:11] == 'Last Frame:':
                cache_result['last_frame'] = current_line[12:]
            elif current_line[:5] == 'From:':
                cache_result['from'] = current_line[6:]
            elif current_line[:17] == 'From (formatted):':
                cache_result['from_formatted'] = current_line[18:]
            elif current_line[:3] == 'To:':
                cache_result['to'] = current_line[4:]
            elif current_line[:15] == 'To (formatted):':
                cache_result['to_formatted'] = current_line[16:]
            elif current_line[:3] == 'At:':
                cache_result['at'] = current_line[4:]
            elif current_line[:15] == 'At (formatted):':
                cache_result['at_formatted'] = current_line[16:]
            elif current_line[:5] == 'Hash:':
                cache_result['hash'] = current_line[6:]
            elif current_line[:18] == 'Hashing Algorithm:':
                cache_result['hashing_algorithm'] = current_line[19:]
            elif current_line[:9] == 'Filename:':
                cache_result['filename'] = current_line[10:]
            elif current_line[:18] == 'Episode Framerate:':
                cache_result['episode_framerate'] = current_line[19:]
            elif current_line[:17] == 'Episode Duration:':
                cache_result['episode_duration'] = current_line[18:]
            elif current_line[:29] == 'Episode Duration (formatted):':
                cache_result['episode_duration_formatted'] = current_line[30:]
            elif current_line[:20] == 'Episode Frame Count:':
                cache_result['episode_frame_count'] = current_line[21:]
            elif current_line[:13] == 'Analyze Date:':
                cache_result['analyze_date'] = current_line[14:]
            elif current_line[:25] == 'Analyze Date (formatted):':
                cache_result['analyze_date_formatted'] = current_line[26:]
            line = cache_file.readline()
        cache_file.close()
    except:
        erina_log.logerror('[ErinaSearch] Error while reading Erina Database Data')
        cache_result['error'] = True
        cache_result['error_details'] = '<erina_database_parsing>'
    return result_python_translation.verify_dict(cache_result)
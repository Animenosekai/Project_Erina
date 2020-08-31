"""
Caching API for the Erina Project

@author: Anime no Sekai
Erina Project - 2020
"""
import sys
sys.path.append('..')

import json
from datetime import datetime
from datetime import timedelta

import lifeeasy
from saucenao_api import SauceNao
from saucenao_api.containers import BookSauce, VideoSauce
import env_information
import erina_log
import config

caches_dir_path = env_information.erina_dir + '/ErinaCaches/'
anilist_cache_path = caches_dir_path + 'AniList_Cache/'
erina_cache_path = caches_dir_path + 'Erina_Cache/'
tracemoe_cache_path = caches_dir_path + 'TraceMoe_Cache/'
saucenao_cache_path = caches_dir_path + 'SauceNAO_Cache/'

if config.saucenao_api_key != '':
    saucenao_api = SauceNao(api_key=config.saucenao_api_key, numres=1)
else:
    saucenao_api = SauceNao(numres=1)


def create_erina_list(list_to_stringify):
    """
    Creates a list string for Erina Cache files
    """
    final_string = ''
    for data in list_to_stringify:
        if final_string == '':
            final_string = str(data)
            continue
        else:
            final_string += ':::' + str(data)
    return final_string

def anilist_api(anilist_id):
    """
    Internal Function for the cache API of Erina to request from the AniList API (GraphQL)
    """
    # query is the response structure requested to the GraphQL AniList API (→ See GraphQL and AniList API documentation to learn more about this data structure)
    query = '''
    query ($id: Int) {
    Media(id: $id, type: ANIME) {
            id
            idMal
            title {
                romaji
                english
                native
            }
            type
            format
            status
            description(asHtml: false)
            season
            seasonYear
            episodes
            duration
            startDate {
                year
                month
                day
            }
            endDate {
                year
                month
                day
            }
            countryOfOrigin
            source
            isLicensed
            isAdult
            hashtag
            genres
            synonyms
            averageScore
            trailer {
                id
                site
            }
            studios {
                edges {
                    isMain
                    node {
                        id
                        name
                        isAnimationStudio
                    }
                }
            }
            coverImage {
                extraLarge
                color
            }
            bannerImage
            streamingEpisodes {
                title
                url
                site
            }
            externalLinks {
                site
                url
            }
            tags {
                name
                rank
                isMediaSpoiler
                isAdult
                category
            }
            relations {
                edges {
                    relationType
                    node {
                        id
                        title {
                            romaji
                        }
                    }
                }
            }
            characters(sort: ROLE) {
            edges {
                role
                node {
                    id
                    name {
                        full
                        native
                    }
                }
            }
            }
            staff(sort: ROLE) {
            edges {
                role
                node {
                    id
                    name {
                        full
                        native
                    }
                }
            }
            }
            recommendations {
                nodes {
                    mediaRecommendation {
                        id
                        title {
                            romaji
                        }
                    }
                }
            }
        }
    }
    '''
    variables = {
        'id': anilist_id
    }
    response = lifeeasy.request(url='https://graphql.anilist.co', method='post', json_body={'query': query, 'variables': variables})
    return json.loads(response.text.replace('null', '""'))['data']['Media']

def anilist_api_search(query_string):
    """
    Internal Function for the cache API of Erina to request a search from the AniList API (GraphQL)
    """
    # query is the response structure requested to the GraphQL AniList API (→ See GraphQL and AniList API documentation to learn more about this data structure)
    query = '''
    query ($search: String) {
        anime: Page(perPage: 1) {
            results: media(type: ANIME, search: $search) {
                id
                idMal
                title {
                    romaji
                    english
                    native
                }
                type
                format
                status
                description(asHtml: false)
                season
                seasonYear
                episodes
                duration
                startDate {
                    year
                    month
                    day
                }
                endDate {
                    year
                    month
                    day
                }
                countryOfOrigin
                source
                isLicensed
                isAdult
                hashtag
                genres
                synonyms
                averageScore
                trailer {
                    id
                    site
                }
                studios {
                    edges {
                        isMain
                        node {
                            id
                            name
                            isAnimationStudio
                        }
                    }
                }
                coverImage {
                    extraLarge
                    color
                }
                bannerImage
                streamingEpisodes {
                    title
                    url
                    site
                }
                externalLinks {
                    site
                    url
                }
                tags {
                    name
                    rank
                    isMediaSpoiler
                    isAdult
                    category
                }
                relations {
                    edges {
                        relationType
                        node {
                            id
                            title {
                                romaji
                            }
                        }
                    }
                }
                characters(sort: ROLE) {
                edges {
                    role
                    node {
                        id
                        name {
                            full
                            native
                        }
                    }
                }
                }
                staff(sort: ROLE) {
                edges {
                    role
                    node {
                        id
                        name {
                            full
                            native
                        }
                    }
                }
                }
                recommendations {
                    nodes {
                        mediaRecommendation {
                            id
                            title {
                                romaji
                            }
                        }
                    }
                }
            }
        }
    }
    '''
    variables = {
        'search': query_string
    }
    response = lifeeasy.request(url='https://graphql.anilist.co', method='post', json_body={'query': query, 'variables': variables})
    return json.loads(response.text.replace('null', '""'))['data']['anime']['results'][0]


def anilist_json_to_cache(anilist_api_result):
    """
    Internal function to convert AniList API Response (json) to Erina Cache\n
    Project Erina
    © Anime no Sekai - 2020
    """
    cache_content = []
    cache_content.append('AniList ID: ' + str(anilist_api_result['id']))
    cache_content.append('MyAnimeList ID: ' + str(anilist_api_result['idMal']))
    cache_content.append('Romaji Title: ' + anilist_api_result['title']['romaji'])
    cache_content.append('English Title: ' + anilist_api_result['title']['english'])
    cache_content.append('Native Title: ' + anilist_api_result['title']['native'])
    cache_content.append('Type: ' + anilist_api_result['type'])
    cache_content.append('Format: ' + anilist_api_result['format'])
    cache_content.append('Status: ' + anilist_api_result['status'])
    cache_content.append('Description: ' + anilist_api_result['description'].replace('\n', '').replace('<br>', '').replace('<\\br>', ''))
    cache_content.append('Season: ' + anilist_api_result['season'])
    cache_content.append('Year: ' + str(anilist_api_result['seasonYear']))
    cache_content.append('Episodes: ' + str(anilist_api_result['episodes']))
    cache_content.append('Average Duration: ' + str(anilist_api_result['duration']))
    cache_content.append('First Episode Release Date: ' + str(anilist_api_result['startDate']['year']) + '-' + str(anilist_api_result['startDate']['month']) + '-' + str(anilist_api_result['startDate']['day']))
    cache_content.append('[First Episode Release Date - Year] ' + str(anilist_api_result['startDate']['year']))
    cache_content.append('[First Episode Release Date - Month] ' + str(anilist_api_result['startDate']['month']))
    cache_content.append('[First Episode Release Date - Day] ' + str(anilist_api_result['startDate']['day']))
    cache_content.append('Last Episode Release Date: ' + str(anilist_api_result['endDate']['year']) + '-' + str(anilist_api_result['endDate']['month']) + '-' + str(anilist_api_result['endDate']['day']))
    cache_content.append('[Last Episode Release Date - Year] ' + str(anilist_api_result['endDate']['year']))
    cache_content.append('[Last Episode Release Date - Month] ' + str(anilist_api_result['endDate']['month']))
    cache_content.append('[Last Episode Release Date - Day] ' + str(anilist_api_result['endDate']['day']))
    cache_content.append('Country: ' + anilist_api_result['countryOfOrigin'])
    cache_content.append('Source Media Type: ' + anilist_api_result['source'])
    cache_content.append('Licensed? ' + str(anilist_api_result['isLicensed']))
    cache_content.append('Hentai? ' + str(anilist_api_result['isAdult']))
    cache_content.append('Twitter Hashtag: ' + anilist_api_result['hashtag'])
    cache_content.append('Average Score: ' + str(anilist_api_result['averageScore']))
    cache_content.append('Cover Image: ' + anilist_api_result['coverImage']['extraLarge'])
    try:
        cache_content.append('Average Cover Color: ' + str(anilist_api_result['coverImage']['color']))
    except:
        cache_content.append('Average Cover Color: unknown')
    cache_content.append('Banner Image: ' + str(anilist_api_result['bannerImage']))
    try:
        if anilist_api_result['trailer']['site'] == 'youtube':
            trailer_url = 'https://youtube.com/watch?v=' + str(anilist_api_result['trailer']['id'])
        elif anilist_api_result['trailer']['site'] == 'dailymotion':
            trailer_url = 'https://www.dailymotion.com/video/' + str(anilist_api_result['trailer']['id'])
        else:
            trailer_url = 'Unavailable'
    except:
        trailer_url = 'Unavailable'
    cache_content.append('Trailer: ' + trailer_url)
    genres = ''
    for genre in anilist_api_result['genres']:
        if genres == '':
            genres = genre
            continue
        genres = genres + ':::' + genre
    cache_content.append('Genres: ' + genres)
    synonyms = ''
    for synonym in anilist_api_result['synonyms']:
        if synonyms == '':
            synonyms = synonym
            continue
        synonyms = synonyms + ':::' + synonym
    cache_content.append('Alternative Title(s): ' + synonyms)
    for studio in anilist_api_result['studios']['edges']:
        cache_content.append('[STUDIO] ' + str(studio['isMain']) + '｜｜｜' + str(studio['node']['id']) + '｜｜｜' + studio['node']['name'] + '｜｜｜' + str(studio['node']['isAnimationStudio']))
    
    for tag in anilist_api_result['tags']:
        cache_content.append('[TAG] ' + tag['name'] + '｜｜｜' + str(tag['rank']) + '｜｜｜' + str(tag['isMediaSpoiler']) + '｜｜｜' + str(tag['isAdult']) + '｜｜｜' + tag['category'])
    
    for relation in anilist_api_result['relations']['edges']:
        cache_content.append('[RELATION] ' + relation['relationType'] + '｜｜｜' + str(relation['node']['id']) + '｜｜｜' + relation['node']['title']['romaji'])
    
    for character in anilist_api_result['characters']['edges']:
        cache_content.append('[CHARACTER] ' + character['role'] + '｜｜｜' + str(character['node']['id']) + '｜｜｜' + character['node']['name']['full'] + '｜｜｜' + character['node']['name']['native'])
    
    for staff in anilist_api_result['staff']['edges']:
        cache_content.append('[STAFF] ' + staff['role'] + '｜｜｜' + str(staff['node']['id']) + '｜｜｜' + staff['node']['name']['full'] + '｜｜｜' + staff['node']['name']['native'])
    
    for recommendation in anilist_api_result['recommendations']['nodes']:
        cache_content.append('[RECOMMENDATION] ' + str(recommendation['mediaRecommendation']['id']) + '｜｜｜' + recommendation['mediaRecommendation']['title']['romaji'])

    for episode in anilist_api_result['streamingEpisodes']:
        cache_content.append('[streaming link] ' + str(episode['title']) + ': ' + str(episode['url']))
    for link in anilist_api_result['externalLinks']:
        cache_content.append('[external link] ' + (str(link['site']) + ': ' + str(link['url'])))
    cache_content.append('')
    cache_content.append('Cache Timestamp: ' + str(datetime.timestamp(datetime.today())))
    cache_content.append('Cache Timestamp (formatted): ' + lifeeasy.today() + ' at ' + lifeeasy.current_time())
    return {'content': cache_content, 'filename': str(anilist_api_result['id']) + '.erina'}

def anilist_caching(anilist_id):
    '''
    Caches the anime associated with the given AniList ID (from AniList API)\n
    Project Erina
    © Anime no Sekai - 2020
    '''
    try:
        erina_log.logcaches(f'Caching {str(anilist_id)} from AniList API...', 'anilist', anilist_id)
        cache = anilist_json_to_cache(anilist_api(anilist_id))
        cache_filename = cache['filename']
        cache_content = cache['content']
        lifeeasy.write_file(cache_filename, cache_content, anilist_cache_path)
        return True
    except:
        erina_log.logerror(f'[ErinaCaches] An error occured while caching <AniList ID: {str(anilist_id)}>')
        return False

def anilist_search_caching(query):
    '''
    Caches the first search result from the given query (from AniList API)\n
    Returns the new cache's filename\n
    Project Erina
    © Anime no Sekai - 2020
    '''
    try:
        erina_log.logcaches('Caching from AniList Search API...', 'anilist_search', str(query))
        cache = anilist_json_to_cache(anilist_api_search(query))
        cache_filename = cache['filename']
        cache_content = cache['content']
        lifeeasy.write_file(cache_filename, cache_content, anilist_cache_path)
        return cache_filename
    except:
        erina_log.logerror(f'[ErinaCaches] An error occured while caching <AniList Query: {str(query)}>')
        return False

def tracemoe_caching(image_hash, api_result):
    '''
    Caches the given Trace.moe API response\n
    Project Erina
    © Anime no Sekai - 2020
    '''
    try:
        erina_log.logcaches('Caching trace.moe data...', 'tracemoe', str(image_hash))
        cache_filename = str(image_hash) + '.erina'
        cache_content = []
        tracemoe_api_result = api_result
        cache_content.append('AniList ID: ' + str(tracemoe_api_result['docs'][0]['anilist_id']))
        cache_content.append('Title Romaji: ' + str(tracemoe_api_result['docs'][0]['title_romaji']))
        cache_content.append('Anime: ' + str(tracemoe_api_result['docs'][0]['anime']))
        cache_content.append('Season: ' + str(tracemoe_api_result['docs'][0]['season']))
        cache_content.append('MyAnimeList ID: ' + str(tracemoe_api_result['docs'][0]['mal_id']))
        cache_content.append('isAdult: ' + str(tracemoe_api_result['docs'][0]['is_adult']))
        cache_content.append('Episode: ' + str(tracemoe_api_result['docs'][0]['episode']))
        cache_content.append('Filename: ' + str(tracemoe_api_result['docs'][0]['filename']))
        cache_content.append('From: ' + str(tracemoe_api_result['docs'][0]['from']))
        cache_content.append('To: ' + str(tracemoe_api_result['docs'][0]['to']))
        cache_content.append('At: ' + str(tracemoe_api_result['docs'][0]['at']))
        cache_content.append('From (formatted): ' + str(timedelta(seconds=float(str(tracemoe_api_result['docs'][0]['from'])))))
        cache_content.append('To (formatted): ' + str(timedelta(seconds=float(str(tracemoe_api_result['docs'][0]['to'])))))
        cache_content.append('At (formatted): ' + str(timedelta(seconds=float(str(tracemoe_api_result['docs'][0]['at'])))))
        cache_content.append('Similarity/Confidence: ' + str(float(tracemoe_api_result['docs'][0]['similarity']) * 100))
        cache_content.append('TokenThumb: ' + str(tracemoe_api_result['docs'][0]['tokenthumb']))
        cache_content.append('Title: ' + str(tracemoe_api_result['docs'][0]['title']))
        cache_content.append('Title Native: ' + str(tracemoe_api_result['docs'][0]['title_native']))
        cache_content.append('Title Chinese: ' + str(tracemoe_api_result['docs'][0]['title_chinese']))
        cache_content.append('Title English: ' + str(tracemoe_api_result['docs'][0]['title_english']))
        synonyms = ''
        for synonym in tracemoe_api_result['docs'][0]['synonyms']:
            if synonyms == '':
                synonyms = str(synonym)
                continue
            synonyms = synonyms + ':::' + str(synonym)
        cache_content.append('Synonyms: ' + synonyms)
        synonyms_chinese = ''
        for synonym_chinese in tracemoe_api_result['docs'][0]['synonyms']:
            if synonyms_chinese == '':
                synonyms_chinese = str(synonym_chinese)
                continue
            synonyms_chinese = synonyms_chinese + ':::' + str(synonym_chinese)
        cache_content.append('Synonyms Chinese: ' + synonyms_chinese)

        cache_content.append('')
        cache_content.append('Cache Timestamp: ' + str(datetime.timestamp(datetime.today())))
        cache_content.append('Cache Timestamp (formatted): ' + lifeeasy.today() + ' at ' + lifeeasy.current_time())

        lifeeasy.write_file(cache_filename, cache_content, tracemoe_cache_path)
        return True
    except Exception as exception:
        erina_log.logerror('[ErinaCache] TraceMOE Caching - ' + exception)
        return False

def saucenao_caching(image_hash, image_url='', file=''):
    '''
    Caches the result from the given url\n
    Project Erina\n
    © Anime no Sekai - 2020
    '''
    try:
        cache_filename = str(image_hash) + '.erina'
        erina_log.logcaches(f'Caching SauceNAO API data...', 'saucenao', str(image_hash))
        if image_url != '':
            api_results = saucenao_api.from_url(image_url)[0]
        elif file != '':
            api_results = saucenao_api.from_file(file)[0]
        else:
            return ''
        cache_content = []
        cache_content.append('   --- SAUCENAO CACHE ---   ')
        cache_content.append('')
        cache_content.append('Similarity: ' + str(api_results.similarity))
        cache_content.append('Index ID: ' + str(api_results.index_id))
        cache_content.append('Index Name: ' + str(api_results.index_name))
        cache_content.append('Title: ' + str(api_results.title))
        cache_content.append('URL: ' + str(api_results.url))
        cache_content.append('Author: ' + str(api_results.author))
        cache_content.append('Thumbnail: ' + str(api_results.thumbnail))
        if isinstance(api_results, BookSauce):
            cache_content.append('isManga: True')
            cache_content.append('isAnime: False')
            cache_content.append('Part: ' + str(api_results.part))
        elif isinstance(api_results, VideoSauce):
            cache_content.append('isManga: False')
            cache_content.append('isAnime: True')
            cache_content.append('Episode: ' + str(api_results.part))
            cache_content.append('Year: ' + str(api_results.year))
            cache_content.append('Estimated Time: ' + str(api_results.est_time))
        else:
            cache_content.append('isManga: False')
            cache_content.append('isAnime: False')

        cache_content.append('')
        cache_content.append('Cache Timestamp: ' + str(datetime.timestamp(datetime.today())))
        cache_content.append('Cache Timestamp (formatted): ' + lifeeasy.today() + ' at ' + lifeeasy.current_time())
        lifeeasy.write_file(cache_filename, cache_content, saucenao_cache_path)
        return saucenao_cache_path + cache_filename
    except Exception as exception:
        erina_log.logerror('[ErinaCache] SauceNAO Caching - ' + exception)
        return ''

def erina_caching(image_hash, database_path, similarity):
    '''
    Caches an ErinaDatabase path according to the image_hash\n
    Project Erina
    © Anime no Sekai - 2020
    '''
    try:
        erina_log.logcaches('Caching Erina Database data...', 'erina', {'image_hash': str(image_hash), 'database_path': str(database_path), 'similarity': similarity})
        cache_filename = str(image_hash) + '.erina'
        cache_content = []
        cache_content.append('Path: ' + database_path)
        cache_content.append('Hash: ' + str(image_hash))
        cache_content.append('Similarity: ' + str(similarity))
        cache_content.append('')
        cache_content.append('Cache Timestamp: ' + str(datetime.timestamp(datetime.today())))
        cache_content.append('Cache Timestamp (formatted): ' + lifeeasy.today() + ' at ' + lifeeasy.current_time())

        lifeeasy.write_file(cache_filename, cache_content, erina_cache_path)
        return True
    except Exception as exception:
        erina_log.logerror('[ErinaCache] Erina Caching - ' + exception)
        return False
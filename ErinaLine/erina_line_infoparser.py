"""
Anime Database Information Parser (for Line) for the Erina Project

@author: Anime no Sekai
Erina Project - 2020
"""
import sys
sys.path.append('..')

import erina_log
import config
from ErinaSearch import erinasearch, saucenao_db
from ErinaCaches import iqdb_api


######## UTILITY FUNCTION ########
def capitalize_string(string):
    final_string = ''
    for word in string.split(' '):
        if final_string == '':
            final_string = word.capitalize()
            continue
        else:
            final_string += ' ' + word.capitalize()
    return final_string

def create_nice_list(input_list):
    result = ''
    try:
        result = capitalize_string(str(input_list[0]))
        try:
            result = capitalize_string(str(input_list[0])) + ', ' + capitalize_string(str(input_list[1]))
            try:
                result = capitalize_string(str(input_list[0])) + ', ' + capitalize_string(str(input_list[1])) + ', ' + capitalize_string(str(input_list[2]))
            except:
                result = capitalize_string(str(input_list[0])) + ', ' + capitalize_string(str(input_list[1]))
        except:
            result = capitalize_string(str(input_list[0]))
    except:
        result = 'unknown'
    return result


######## MAIN FUNCTION ########
def search_anime_by_image_path(image_path):
    """
    Searching Anime Scenes by Image URL for Twitter\n

    Erina Project\n
    © Anime no Sekai - 2020
    """
    result = erinasearch.search_anime_from_image_path(image_path, anilist_priority=config.line_anilist_priority)
    if result['erina_cache'] or result['erina_database']:
        return create_reply_for_erinadb(result)
    elif result['tracemoe_cache'] or result['tracemoe_api']:
        return create_reply_for_tracemoe(result)
    elif result['saucenao_cache'] or result['saucenao_api']:
        return create_reply_for_saucenao(result)
    elif result['iqdb_cache'] or result['iqdb_api']:
        return create_reply_for_iqdb(result)
    else:
        return {'error': 'no result found'}


######## DATABASE INFO PARSER ########

def give_info_for_manami(result):
    anime_info = {}
    anime_info['provider'] = 'manami'
    anime_info['studios'] = 'Unknown'
    anime_info['anime'] = result['search_result']['result']['title']
    anime_info['episodes'] = result['search_result']['result']['episodes']
    anime_info['status'] = result['search_result']['result']['status']
    anime_info['genres'] = create_nice_list(result['search_result']['result']['tags'])
    return anime_info


def give_info_for_anilist(result):
    anime_info = {}
    anime_info['studios'] = 'Unknown'
    anime_info['provider'] = 'anilist'
    anime_info['anime'] = result['search_result']['result']['title']
    anime_info['episodes'] = result['search_result']['result']['episodes']
    anime_info['status'] = result['search_result']['result']['status']
    
    anime_info['genres'] = create_nice_list(result['search_result']['result']['genres'])

    for studio in result['search_result']['result']['studios']:
        if studio['is_animation_studio']:
            if anime_info['studios'] == 'Unknown':
                anime_info['studios'] = studio['name']
            else:
                anime_info['studios'] = anime_info['studios']  + ', ' + studio['name']
    anime_info['description'] = result['search_result']['result']['description']
    anime_info['hashtag'] = result['search_result']['result']['twitter_hashtag']
    return anime_info







######## IMAGE RECOGNITION INFO PARSER ########
def create_reply_for_erinadb(result):
    anime_info = {}
    anime_info['episode'] = result['erina_result']['episode']
    anime_info['at'] = result['erina_result']['at_formatted'].partition('.')[0]
    anime_info['anilist_url'] = 'https://anilist.co/anime/' + result['erina_result']['anilist_id']
    if result['search_result']['found_from_anilist_cache'] or result['search_result']['found_from_anilist_api']:
        anime_info['is_hentai'] = result['search_result']['result']['is_hentai']
    else:
        anime_info['is_hentai'] = False

    if result['search_result']['found_from_anilist_cache'] or result['search_result']['found_from_anilist_api']:
        anime_info = {**anime_info, **give_info_for_anilist(result)}
    elif result['search_result']['found_from_manami']:
        anime_info = {**anime_info, **give_info_for_manami(result)}

### MAKING THE REPLY
    reply_messages = []
    reply_text = ''
    if result['low_similarity']:
        reply_text += ' - The similarities seem pretty low -\n\n'
    reply_text += ( f"Anime: {anime_info['anime']}\n"
                    f"Episode: {anime_info['episode']}/{anime_info['episodes']} (at around {anime_info['at']})\n"
                    f"Studio: {anime_info['studios']}\n"
    )

    if anime_info['provider'] == 'anilist':
        reply_text += f"Genres: {anime_info['genres']}\n"
    else:
        reply_text += f"Tags: {anime_info['genres']}\n"
    
    reply_text += f"{anime_info['anilist_url']}\n"
    
    reply_messages.append(reply_text)
    
    if anime_info['is_hentai']:
        reply_messages.append('⚠️ Seems to be a Hentai! ⚠️')
    
    if anime_info['provider'] == 'anilist':
        description = anime_info['description']
        if len(description) > 100:
            reply_messages.append(str(description[:100]) + '...')
        else:
            reply_messages.append(description)

    return reply_messages

def create_reply_for_tracemoe(result):
###### GETTING THE INFO
    anime_info = {}
    anime_info['episode'] = result['tracemoe_result']['episode']
    anime_info['at'] = result['tracemoe_result']['at_formatted'].partition('.')[0]
    anime_info['is_hentai'] = result['tracemoe_result']['is_adult']
    anime_info['anilist_url'] = 'https://anilist.co/anime/' + result['tracemoe_result']['anilist_id']

    if result['search_result']['found_from_anilist_cache'] or result['search_result']['found_from_anilist_api']:
        anime_info = {**anime_info, **give_info_for_anilist(result)}
    elif result['search_result']['found_from_manami']:
        anime_info = {**anime_info, **give_info_for_manami(result)}



###### CREATING THE REPLY
### MAKING THE REPLY
    reply_messages = []
    reply_text = ''
    if result['low_similarity']:
        reply_text += ' - The similarities seem pretty low -\n\n'
    reply_text += ( f"Anime: {anime_info['anime']}\n"
                    f"Episode: {anime_info['episode']}/{anime_info['episodes']} (at around {anime_info['at']})\n"
                    f"Studio: {anime_info['studios']}\n"
    )

    if anime_info['provider'] == 'anilist':
        reply_text += f"Genres: {anime_info['genres']}\n"
    else:
        reply_text += f"Tags: {anime_info['genres']}\n"
    
    reply_text += f"{anime_info['anilist_url']}\n"
    
    reply_messages.append(reply_text)
    
    if anime_info['is_hentai']:
        reply_messages.append('⚠️ Seems to be a Hentai! ⚠️')
    
    if anime_info['provider'] == 'anilist':
        description = anime_info['description']
        if len(description) > 100:
            reply_messages.append(str(description[:100]) + '...')
        else:
            reply_messages.append(description)

    return reply_messages

    
def create_reply_for_saucenao(result):

    if result['is_anime']:

        anime_info = {}
##### GETTING THE INFO        
        anime_info['episode'] = result['saucenao_result']['episode']
        anime_info['at'] = result['saucenao_result']['estimated_time'].split('/')[0]
        
        if result['search_result']['found_from_anilist_cache'] or result['search_result']['found_from_anilist_api']:
            anime_info['is_hentai'] = result['search_result']['result']['is_hentai']
        else:
            anime_info['is_hentai'] = False

        anime_info['anilist_url'] = 'https://anilist.co/anime/' + str(result['search_result']['result']['anilist_id'])

        if result['search_result']['found_from_anilist_cache'] or result['search_result']['found_from_anilist_api']:
            anime_info = {**anime_info, **give_info_for_anilist(result)}
        elif result['search_result']['found_from_manami']:
            anime_info = {**anime_info, **give_info_for_manami(result)}


##### CREATING AND FORMATTING THE REPLY
    ### MAKING THE REPLY
        reply_messages = []
        reply_text = ''
        if result['low_similarity']:
            reply_text += ' - The similarities seem pretty low -\n\n'
        reply_text += ( f"Anime: {anime_info['anime']}\n"
                        f"Episode: {anime_info['episode']}/{anime_info['episodes']} (at around {anime_info['at']})\n"
                        f"Studio: {anime_info['studios']}\n"
        )

        if anime_info['provider'] == 'anilist':
            reply_text += f"Genres: {anime_info['genres']}\n"
        else:
            reply_text += f"Tags: {anime_info['genres']}\n"
        
        reply_text += f"{anime_info['anilist_url']}\n"
        
        reply_messages.append(reply_text)
        
        if anime_info['is_hentai']:
            reply_messages.append('⚠️ Seems to be a Hentai! ⚠️')
        
        if anime_info['provider'] == 'anilist':
            description = anime_info['description']
            if len(description) > 100:
                reply_messages.append(str(description[:100]) + '...')
            else:
                reply_messages.append(description)

        return reply_messages

    else:
        sauce_info = {}
        sauce_info['similarity'] = result['similarity']
        sauce_info['database'] = saucenao_db.index_to_db(result['saucenao_result']['index_id'])
        sauce_info['title'] = result['saucenao_result']['title']
        sauce_info['url'] = result['saucenao_result']['url']
        sauce_info['author'] = result['saucenao_result']['author']

        reply_text = ''
        if result['low_similarity']:
            reply_text += 'The similarities seem pretty low but...\n'
        reply_text += ( f"I found it on {str(sauce_info['database'])}\n"
                        f"Similarity: {str(sauce_info['similarity'])}%):\n"
                        f"Title: {str(sauce_info['title'])}\n"
                        f"Author: {str(sauce_info['author'])}\n\n"

                        f"{str(sauce_info['url'])}"
        )


        return [reply_text]

def create_reply_for_iqdb(result):
    sauce_info = result['iqdb_result']
    reply_text = ''
    if result['low_similarity']:
        reply_text += 'The similarities seem pretty low but...\n'
    reply_text += ( f"I found it on {str(iqdb_api.db_to_name(sauce_info['database']))}\n"
                    f"(Similarity: {str(sauce_info['similarity'])}%):\n\n"
    )

    if sauce_info['database'] == 'danbooru':
        if len(sauce_info['danbooru_results']['artists']) > 0:
            if len(sauce_info['danbooru_results']['artists']) > 1:
                reply_text += f"Authors: {create_nice_list(sauce_info['danbooru_results']['artists'])}\n"
            else:
                reply_text += f"Author: {str(sauce_info['danbooru_results']['artists'][0])}\n"
                            
        if len(sauce_info['danbooru_results']['copyrights']) > 0:
            if len(sauce_info['danbooru_results']['copyrights']) > 1:
                reply_text += f"Copyrights: {create_nice_list(sauce_info['danbooru_results']['copyrights'])}\n"
            else:
                reply_text += f"Copyright: {capitalize_string(str(sauce_info['danbooru_results']['copyrights'][0]))}\n"
                            
        if len(sauce_info['danbooru_results']['characters']) > 0:
            if len(sauce_info['danbooru_results']['characters']) > 1:
                reply_text += f"Characters: {create_nice_list(sauce_info['danbooru_results']['characters'])}\n"
            else:
                reply_text += f"Character: {capitalize_string(str(sauce_info['danbooru_results']['characters'][0]))}\n"

        if len(sauce_info['danbooru_results']['tags']) > 0:
            reply_text += f"Tags: {create_nice_list(sauce_info['danbooru_results']['tags'])}\n"
        
        if sauce_info['danbooru_results']['rating'] != '':
            reply_text += f"Rating: {capitalize_string(str(sauce_info['danbooru_results']['rating']))}\n"
        
        if sauce_info['danbooru_results']['size'] != '':
            reply_text += f"Size: {capitalize_string(str(sauce_info['danbooru_results']['size']))}\n"

        

        reply_text += f"\n{str(sauce_info['url'])}"

    elif sauce_info['database'] == 'gelbooru':
        
        if len(sauce_info['gelbooru_results']['copyrights']) > 0:
            if len(sauce_info['gelbooru_results']['copyrights']) > 1:
                reply_text += f"Copyrights: {create_nice_list(sauce_info['gelbooru_results']['copyrights'])}\n"
            else:
                reply_text += f"Copyright: {capitalize_string(str(sauce_info['gelbooru_results']['copyrights'][0]))}\n"
                            
        if len(sauce_info['gelbooru_results']['characters']) > 0:
            if len(sauce_info['gelbooru_results']['characters']) > 1:
                reply_text += f"Characters: {create_nice_list(sauce_info['gelbooru_results']['characters'])}\n"
            else:
                reply_text += f"Character: {capitalize_string(str(sauce_info['gelbooru_results']['characters'][0]))}\n"

        if len(sauce_info['gelbooru_results']['tags']) > 0:
            reply_text += f"Tags: {create_nice_list(sauce_info['gelbooru_results']['tags'])}\n"
        
        if sauce_info['gelbooru_results']['rating'] != '':
            reply_text += f"Rating: {capitalize_string(str(sauce_info['gelbooru_results']['rating']))}\n"
        
        if sauce_info['gelbooru_results']['size'] != '':
            reply_text += f"Size: {str(sauce_info['gelbooru_results']['size'])}\n"

        

        reply_text += f"\n{str(sauce_info['url'])}"

    elif sauce_info['database'] == 'zerochan':
        
        if sauce_info['zerochan_results']['name'] != '':
            reply_text += f"Title: {capitalize_string(str(sauce_info['zerochan_results']['name']))}\n"
        
        if sauce_info['zerochan_results']['managaka'] != '':
            reply_text += f"Author: {str(sauce_info['zerochan_results']['mangaka'])}\n"
        
        if sauce_info['zerochan_results']['series'] != '':
            reply_text += f"Series: {capitalize_string(str(sauce_info['zerochan_results']['series']))}"
        
        if sauce_info['zerochan_results']['character'] != '':
            reply_text += f"Character: {capitalize_string(str(sauce_info['zerochan_results']['character']))}"
        
        if sauce_info['zerochan_results']['source'] != '':
            reply_text += f"Source: {str(sauce_info['zerochan_results']['source'])}"
        
        if sauce_info['zerochan_results']['width'] != '' and sauce_info['zerochan_results']['height'] != '' :
            reply_text += f"Size: {str(sauce_info['zerochan_results']['width'])}x{str(sauce_info['zerochan_results']['height'])}"

        

        reply_text += f"\n{str(sauce_info['url'])}"

    elif sauce_info['database'] == 'konachan':
        
        if len(sauce_info['konachan_results']['artists']) > 0:
            if len(sauce_info['konachan_results']['artists']) > 1:
                reply_text += f"Authors: {create_nice_list(sauce_info['konachan_results']['artists'])}\n"
            else:
                reply_text += f"Author: {str(sauce_info['konachan_results']['artists'][0])}\n"
                            
        if len(sauce_info['konachan_results']['copyrights']) > 0:
            if len(sauce_info['konachan_results']['copyrights']) > 1:
                reply_text += f"Copyrights: {create_nice_list(sauce_info['konachan_results']['copyrights'])}\n"
            else:
                reply_text += f"Copyright: {capitalize_string(str(sauce_info['konachan_results']['copyrights'][0]))}\n"
                            
        if len(sauce_info['konachan_results']['characters']) > 0:
            if len(sauce_info['konachan_results']['characters']) > 1:
                reply_text += f"Characters: {create_nice_list(sauce_info['konachan_results']['characters'])}\n"
            else:
                reply_text += f"Character: {capitalize_string(str(sauce_info['konachan_results']['characters'][0]))}\n"

        if len(sauce_info['konachan_results']['tags']) > 0:
            reply_text += f"Tags: {create_nice_list(sauce_info['konachan_results']['tags'])}\n"
                                    
        if len(sauce_info['konachan_results']['styles']) > 0:
            if len(sauce_info['konachan_results']['styles']) > 1:
                reply_text += f"Styles: {create_nice_list(sauce_info['konachan_results']['styles'])}\n"
            else:
                reply_text += f"Style: {capitalize_string(str(sauce_info['konachan_results']['styles'][0]))}\n"

        if sauce_info['konachan_results']['rating'] != '':
            reply_text += f"Rating: {capitalize_string(str(sauce_info['konachan_results']['rating']))}\n"
        
        if sauce_info['konachan_results']['size'] != '':
            reply_text += f"Size: {str(sauce_info['konachan_results']['size'])}\n"

        

        reply_text += f"\n{str(sauce_info['url'])}"

    elif sauce_info['database'] == 'yandere':
        
        if len(sauce_info['yandere_results']['artists']) > 0:
            if len(sauce_info['yandere_results']['artists']) > 1:
                reply_text += f"Authors: {create_nice_list(sauce_info['yandere_results']['artists'])}\n"
            else:
                reply_text += f"Author: {str(sauce_info['yandere_results']['artists'][0])}\n"
                            
        if len(sauce_info['yandere_results']['copyrights']) > 0:
            if len(sauce_info['yandere_results']['copyrights']) > 1:
                reply_text += f"Copyrights: {create_nice_list(sauce_info['yandere_results']['copyrights'])}\n"
            else:
                reply_text += f"Copyright: {capitalize_string(str(sauce_info['yandere_results']['copyrights'][0]))}\n"
                            
        if len(sauce_info['yandere_results']['characters']) > 0:
            if len(sauce_info['yandere_results']['characters']) > 1:
                reply_text += f"Characters: {create_nice_list(sauce_info['yandere_results']['characters'])}\n"
            else:
                reply_text += f"Character: {capitalize_string(str(sauce_info['yandere_results']['characters'][0]))}\n"

        if len(sauce_info['yandere_results']['tags']) > 0:
            reply_text += f"Tags: {create_nice_list(sauce_info['yandere_results']['tags'])}\n"
                                    
        if len(sauce_info['yandere_results']['styles']) > 0:
            if len(sauce_info['yandere_results']['styles']) > 1:
                reply_text += f"Styles: {create_nice_list(sauce_info['yandere_results']['styles'])}\n"
            else:
                reply_text += f"Style: {capitalize_string(str(sauce_info['yandere_results']['styles'][0]))}\n"

        if sauce_info['yandere_results']['rating'] != '':
            reply_text += f"Rating: {capitalize_string(str(sauce_info['yandere_results']['rating']))}\n"
        
        if sauce_info['yandere_results']['size'] != '':
            reply_text += f"Size: {str(sauce_info['yandere_results']['size'])}\n"


        

        reply_text += f"\n{str(sauce_info['url'])}"

    elif sauce_info['database'] == 'anime_pictures':
        
        
        if sauce_info['anime_pictures_results']['artist'] != '':
            reply_text += f"Artist: {str(sauce_info['anime_pictures_results']['artist'])}\n"
        
        try:
            for link in sauce_info['anime_pictures_results']['artist_links']:
                if 'twitter.com/' in link:
                    reply_text += f"Artist Twitter: @{str(link.split('twitter.com/')[1])}\n"
                    break
        except:
            pass

        if sauce_info['anime_pictures_results']['size'] != '':
            reply_text += f"Size: {str(sauce_info['anime_pictures_results']['size'])}\n"
                            
        if len(sauce_info['anime_pictures_results']['references']) > 0:
            if len(sauce_info['anime_pictures_results']['references']) > 1:
                reply_text += f"References: {create_nice_list(sauce_info['anime_pictures_results']['references'])}\n"
            else:
                reply_text += f"Reference: {capitalize_string(str(sauce_info['anime_pictures_results']['references'][0]))}\n"
                            
        if len(sauce_info['anime_pictures_results']['objects']) > 0:
            if len(sauce_info['anime_pictures_results']['objects']) > 1:
                reply_text += f"Objects: {create_nice_list(sauce_info['anime_pictures_results']['objects'])}\n"
            else:
                reply_text += f"Object: {capitalize_string(str(sauce_info['anime_pictures_results']['objects'][0]))}"

        

        reply_text += f"\n{str(sauce_info['url'])}"

    elif sauce_info['database'] == 'e_shuushuu':
        
        if len(sauce_info['e_shuushuu_results']['artists']) > 0:
            if len(sauce_info['e_shuushuu_results']['artists']) > 1:
                reply_text += f"Authors: {create_nice_list(sauce_info['e_shuushuu_results']['artists'])}\n"
            else:
                reply_text += f"Author: {str(sauce_info['e_shuushuu_results']['artists'][0])}\n"
                            
        if len(sauce_info['e_shuushuu_results']['characters']) > 0:
            if len(sauce_info['e_shuushuu_results']['characters']) > 1:
                reply_text += f"Characters: {create_nice_list(sauce_info['e_shuushuu_results']['characters'])}\n"
            else:
                reply_text += f"Character: {capitalize_string(str(sauce_info['e_shuushuu_results']['characters'][0]))}\n"

        if len(sauce_info['e_shuushuu_results']['tags']) > 0:
            reply_text += f"Tags: {create_nice_list(sauce_info['e_shuushuu_results']['tags'])}\n"
                                    
        if len(sauce_info['e_shuushuu_results']['sources']) > 0:
            if len(sauce_info['e_shuushuu_results']['sources']) > 1:
                reply_text += f"Sources: {create_nice_list(sauce_info['e_shuushuu_results']['sources'])}\n"
            else:
                reply_text += f"Source: {str(sauce_info['e_shuushuu_results']['sources'][0])}\n"

        if sauce_info['e_shuushuu_results']['rating'] != '':
            reply_text += f"Rating: {capitalize_string(str(sauce_info['e_shuushuu_results']['rating']))}\n"
        
        if sauce_info['e_shuushuu_results']['size'] != '':
            reply_text += f"Size: {str(sauce_info['e_shuushuu_results']['size'])}\n"


        

        reply_text += f"\n{str(sauce_info['url'])}"

    return [reply_text]





def search_anime_by_title(query):
    """
    Searching for Anime Informations from his title\n

    Erina Project\n
    © Anime no Sekai - 2020
    """
    result = erinasearch.search_anime_by_title(query, anilist_priority=config.line_anilist_priority)
    anime_info = {}
    anime_info['season'] = 'unknown'
    anime_info['year'] = 'unknown'
    anime_info['episodes'] = 'unknown'
    anime_info['average_duration'] = 'unknown'
    anime_info['status'] = 'unknown'
    anime_info['image'] = 'unknown'
    anime_info['is_hentai'] = 'unknown'
    anime_info['genres'] = 'unknown'
    anime_info['studios'] = 'unknown'
    anime_info['anilist_url'] = 'unknown'
    
    if result['found_from_anilist_cache'] or result['found_from_anilist_api']:
        anime_info['provider'] = 'anilist'
        anime_info['anilist_url'] = 'https://anilist.co/anime/' + result['result']['anilist_id']
        anime_info['anime'] = result['result']['title']
        anime_info['season'] = result['result']['season'].lower().capitalize()
        anime_info['year'] = result['result']['year']
        anime_info['episodes'] = result['result']['episodes']
        anime_info['average_duration'] = result['result']['average_duration'] + 'min'
        anime_info['status'] = result['result']['status'].lower().capitalize()
        anime_info['image'] = result['result']['cover_image']
        anime_info['is_hentai'] = result['result']['is_hentai']
        try:
            anime_info['genres'] = result['result']['genres'][0]
            try:
                anime_info['genres'] = result['result']['genres'][0] + ', ' + result['result']['genres'][1]
                try:
                    anime_info['genres'] = result['result']['genres'][0] + ', ' + result['result']['genres'][1] + ', ' + result['result']['genres'][2]
                except:
                    anime_info['genres'] = result['result']['genres'][0] + ', ' + result['result']['genres'][1]
            except:
                anime_info['genres'] = result['result']['genres'][0]
        except:
            anime_info['genres'] = 'unknown'

        for studio in result['result']['studios']:
            if str(studio['is_animation_studio']) == 'True':
                if anime_info['studios'] == 'unknown':
                    anime_info['studios'] = studio['name']
                else:
                    anime_info['studios'] = anime_info['studios']  + ', ' + studio['name']
        anime_info['description'] = result['result']['description']
    elif result['found_from_manami']:
        anime_info['provider'] = 'manami'
        anime_info['anime'] = result['result']['title']
        anime_info['type'] = result['result']['type']
        anime_info['episodes'] = result['result']['episodes']
        anime_info['status'] = result['result']['status'].lower().capitalize()
        anime_info['season'] = result['result']['animeSeason']['season'].lower().capitalize()
        anime_info['year'] = result['result']['animeSeason']['year']
        try:
            anime_info['genres'] = result['result']['tags'][0]
            try:
                anime_info['genres'] = result['result']['tags'][0] + ', ' + result['result']['tags'][1]
                try:
                    anime_info['genres'] = result['result']['tags'][0] + ', ' + result['result']['tags'][1] + ', ' + result['result']['tags'][2]
                except:
                    anime_info['genres'] = result['result']['tags'][0] + ', ' + result['result']['tags'][1]
            except:
                anime_info['genres'] = result['result']['tags'][0]
        except:
            anime_info['genres'] = 'unknown'
        for source in result['result']['sources']:
            if source.find('anilist.co') != -1:
                anime_info['anilist_url'] = source
        if anime_info['anilist_url'] == 'unknown':
            for source in result['result']['sources']:
                if source.find('myanimelist.net') != -1:
                    anime_info['anilist_url'] = source
        if anime_info['anilist_url'] == 'unknown':
            if len(result['result']['sources']) != 0:
                anime_info['anilist_url'] = result['result']['sources'][0]

    return anime_info
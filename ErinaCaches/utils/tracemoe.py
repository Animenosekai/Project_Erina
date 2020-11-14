import datetime

def erina_from_json(tracemoe_api_result):
    cache_content = f"""   --- TRACEMOE CACHE ---   
AniList ID: {str(tracemoe_api_result['docs'][0]['anilist_id'])}
Title Romaji: {str(tracemoe_api_result['docs'][0]['title_romaji'])}
Anime: {str(tracemoe_api_result['docs'][0]['anime'])}
Season: {str(tracemoe_api_result['docs'][0]['season'])}
MyAnimeList ID: {str(tracemoe_api_result['docs'][0]['mal_id'])}
isAdult: {str(tracemoe_api_result['docs'][0]['is_adult'])}
Episode: {str(tracemoe_api_result['docs'][0]['episode'])}
Filename: {str(tracemoe_api_result['docs'][0]['filename'])}
From: {str(tracemoe_api_result['docs'][0]['from'])}
To: {str(tracemoe_api_result['docs'][0]['to'])}
At: {str(tracemoe_api_result['docs'][0]['at'])}
Similarity: {str(float(tracemoe_api_result['docs'][0]['similarity']) * 100)}
TokenThumb: {str(tracemoe_api_result['docs'][0]['tokenthumb'])}
Title: {str(tracemoe_api_result['docs'][0]['title'])}
Title Native: {str(tracemoe_api_result['docs'][0]['title_native'])}
Title Chinese: {str(tracemoe_api_result['docs'][0]['title_chinese'])}
Title English: {str(tracemoe_api_result['docs'][0]['title_english'])}
Synonyms: {':::'.join(tracemoe_api_result['docs'][0]['synonyms'])}
Synonyms Chinese: {':::'.join(tracemoe_api_result['docs'][0]['synonyms'])}

Cache Timestamp: {str(datetime.timestamp(datetime.today()))}
"""
    return cache_content
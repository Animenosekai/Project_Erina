from datetime import datetime

def erina_from_json(tracemoe_api_result):
    cache_content = """   --- TRACEMOE CACHE ---   
AniList ID: {anilistID}
Title Romaji: {title_romaji}
Anime: {anime}
Season: {season}
MyAnimeList ID: {malID}
isAdult: {hentai}
Episode: {episode}
Filename: {filename}
From: {from_time}
To: {to_time}
At: {at_time}
Similarity: {similarity}
TokenThumb: {tokenthumb}
Title: {title}
Title Native: {title_native}
Title Chinese: {title_chinese}
Title English: {title_english}
Synonyms: {synonyms}
Synonyms Chinese: {synonyms_chinese}

Cache Timestamp: {cache_timestamp}
""".format(
    anilistID=str(tracemoe_api_result['docs'][0]['anilist_id']),
    title_romaji=str(tracemoe_api_result['docs'][0]['title_romaji']),
    anime=str(tracemoe_api_result['docs'][0]['anime']),
    season=str(tracemoe_api_result['docs'][0]['season']),
    malID=str(tracemoe_api_result['docs'][0]['mal_id']),
    hentai=str(tracemoe_api_result['docs'][0]['is_adult']),
    episode=str(tracemoe_api_result['docs'][0]['episode']),
    filename=str(tracemoe_api_result['docs'][0]['filename']),
    from_time=str(tracemoe_api_result['docs'][0]['from']),
    to_time=str(tracemoe_api_result['docs'][0]['to']),
    at_time=str(tracemoe_api_result['docs'][0]['at']),
    similarity=str(float(tracemoe_api_result['docs'][0]['similarity']) * 100),
    tokenthumb=str(tracemoe_api_result['docs'][0]['tokenthumb']),
    title=str(tracemoe_api_result['docs'][0]['title']),
    title_native=str(tracemoe_api_result['docs'][0]['title_native']),
    title_chinese=str(tracemoe_api_result['docs'][0]['title_chinese']),
    title_english=str(tracemoe_api_result['docs'][0]['title_english']),
    synonyms=':::'.join(tracemoe_api_result['docs'][0]['synonyms']),
    synonyms_chinese=':::'.join(tracemoe_api_result['docs'][0]['synonyms']),
    cache_timestamp=str(datetime.timestamp(datetime.today()))
)
    return cache_content
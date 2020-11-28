import json
import requests
from datetime import datetime

anilistApiQuery = '''
{
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
    description(asHtml: true)
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
'''

def anilist_api(anilist_id):
    """
    Internal Function for the cache API of Erina to request from the AniList API (GraphQL)
    """
    # query is the response structure requested to the GraphQL AniList API (→ See GraphQL and AniList API documentation to learn more about this data structure)
    query = '''
    query ($id: Int) {
        Media(id: $id, type: ANIME) {queryInside}
    }
    '''.format(queryInside=anilistApiQuery)
    variables = {
        'id': anilist_id
    }
    response = requests.post(url='https://graphql.anilist.co', json={'query': query, 'variables': variables}).text
    return json.loads(response.replace('null', '""'))['data']['Media']

def anilist_api_search(query_string):
    """
    Internal Function for the cache API of Erina to request a search from the AniList API (GraphQL)
    """
    # query is the response structure requested to the GraphQL AniList API (→ See GraphQL and AniList API documentation to learn more about this data structure)
    query = '''
    query ($search: String) {
        anime: Page(perPage: 1) {
            results: media(type: ANIME, search: $search) {queryInside}
        }
    }
    '''.format(queryInside=anilistApiQuery)
    variables = {
        'search': query_string
    }
    response = requests.post(url='https://graphql.anilist.co', json={'query': query, 'variables': variables}).text
    return json.loads(response.replace('null', '""'))['data']['anime']['results'][0]



def anilist_json_to_cache(anilist_api_result):
    """
    Internal function to convert AniList API Response (json) to Erina Cache\n
    Project Erina
    © Anime no Sekai - 2020
    """
    cache_content = """   --- ANILIST CACHE ---   
AniList ID: {anilistID}
MyAnimeList ID: {malID}
Romaji Title: {title_romaji}
English Title: {title_english}
Native Title: {title_native}
Type: {type}
Format: {format}
Status: {status}
Description: {description}
Season: {season}
Year: {year}
Episodes: {episodes}
Average Duration: {duration}
First Episode Release Date: {release_first}
Last Episode Release Date: {release_last}
Country: {country}
Source Media Type: {source_type}
Licensed? {licensed}
Hentai? {hentai}
Twitter Hashtag: {hashtag}
Average Score: {score}
Cover Image: {cover}
Banner Image: {banner}
Genres: {genres}
Alternative Title(s): {alt_titles}
""".format(
    anilistID=str(anilist_api_result['id']),
    malID=str(anilist_api_result['idMal']),
    title_romaji=str(anilist_api_result['title']['romaji']),
    title_english=str(anilist_api_result['title']['english']),
    title_native=str(anilist_api_result['title']['native']),
    type=str(anilist_api_result['type']),
    format=str(anilist_api_result['format']),
    status=str(anilist_api_result['status']),
    description=str(anilist_api_result['description']).replace('\n', ' '),
    season=str(anilist_api_result['season']),
    year=str(anilist_api_result['seasonYear']),
    episodes=str(anilist_api_result['episodes']),
    duration=str(anilist_api_result['duration']),
    release_first=str(anilist_api_result['startDate']['year']) + "-" + str(anilist_api_result['startDate']['month']) + "-" + str(anilist_api_result['startDate']['day']),
    release_last=str(anilist_api_result['endDate']['year']) + "-" + str(anilist_api_result['endDate']['month']) + "-" + str(anilist_api_result['endDate']['day']),
    country=str(anilist_api_result['countryOfOrigin']),
    source_type=str(anilist_api_result['source']),
    licensed=str(anilist_api_result['isLicensed']),
    hentai=str(anilist_api_result['isAdult']),
    hashtag=str(anilist_api_result['hashtag']),
    score=str(anilist_api_result['averageScore']),
    cover=str(anilist_api_result['coverImage']['extraLarge']),
    banner=str(anilist_api_result['bannerImage']),
    genres=':::'.join(anilist_api_result['genres']),
    alt_titles=':::'.join(anilist_api_result['synonyms'])
)
    try:
        cache_content += "Average Cover Color: " + str(anilist_api_result['coverImage']['color']) + "\n"
    except:
        cache_content += 'Average Cover Color: Unknown\n'
    try:
        if anilist_api_result['trailer']['site'] == 'youtube':
            trailer_url = 'https://youtube.com/watch?v=' + str(anilist_api_result['trailer']['id'])
        elif anilist_api_result['trailer']['site'] == 'dailymotion':
            trailer_url = 'https://www.dailymotion.com/video/' + str(anilist_api_result['trailer']['id'])
        else:
            trailer_url = 'Unavailable'
    except:
        trailer_url = 'Unavailable'

    cache_content += f"Trailer: {str(trailer_url)}\n"
    
    for studio in anilist_api_result['studios']['edges']:
        cache_content += f"[STUDIO] {str(studio['isMain'])}｜｜｜{str(studio['node']['id'])}｜｜｜{str(studio['node']['name'])}｜｜｜{str(studio['node']['isAnimationStudio'])}\n"
    
    for tag in anilist_api_result['tags']:
        cache_content += f"[TAG] {str(tag['name'])}｜｜｜{str(tag['rank'])}｜｜｜{str(tag['isMediaSpoiler'])}｜｜｜{str(tag['isAdult'])}｜｜｜{str(tag['category'])}\n"
    
    for relation in anilist_api_result['relations']['edges']:
        cache_content += f"[RELATION] {str(relation['relationType'])}｜｜｜{str(relation['node']['id'])}｜｜｜{str(relation['node']['title']['romaji'])}\n"
    
    for character in anilist_api_result['characters']['edges']:
        cache_content += f"[CHARACTER] {str(character['role'])}｜｜｜{str(character['node']['id'])}｜｜｜{str(character['node']['name']['full'])}｜｜｜{str(character['node']['name']['native'])}\n"
    
    for staff in anilist_api_result['staff']['edges']:
        cache_content += f"[STAFF] {str(staff['role'])}｜｜｜{str(staff['node']['id'])}｜｜｜{str(staff['node']['name']['full'])}｜｜｜{str(staff['node']['name']['native'])}\n"
    
    for recommendation in anilist_api_result['recommendations']['nodes']:
        cache_content += f"[RECOMMENDATION] {str(recommendation['mediaRecommendation']['id'])}｜｜｜{recommendation['mediaRecommendation']['title']['romaji']}\n"

    for episode in anilist_api_result['streamingEpisodes']:
        cache_content += f"[streaming link] {str(episode['title'])}: {str(episode['url'])}\n"
    
    for link in anilist_api_result['externalLinks']:
        cache_content += f"[external link] {str(link['site'])}: {str(link['url'])}\n"
    
    cache_content += "\n"
    cache_content += f"Cache Timestamp: {str(datetime.timestamp(datetime.today()))}"
    return {'content': cache_content, 'filename': str(anilist_api_result['id']) + '.erina'}
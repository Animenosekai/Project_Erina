"""
Parses ErinaSearch for Discord
"""


def makeInfoResponse(erinaSearchResponse):
    return "Hey"

def makeImageResponse(erinaSearchResponse):
    return "Hey"

def makeDescriptionResponse(erinaSearchResponse):
    return "Hey"








####### OLD

async def anime_search(channel, search):
    """
    When someone wants to search about an anime
    """
    anime_info = erina_discord_infoparser.search_anime_by_title(search)
    reply_text = ''
    if anime_info['anime'] != 'unknown':
        anime = anime_info['anime']
        reply_text += f'**Anime:** {anime}\n'
    if anime_info['year'] != 'unknown':
        if anime_info['season'] != 'unknown':
            season = anime_info['season']
            year = anime_info['year']
            reply_text += f'**Season:** {season} of {year}\n'
        else:
            year = anime_info['year']
            reply_text += f'**Year:** {year}\n'
    if anime_info['episodes'] != 'unknown':
        episodes = anime_info['episodes'] 
        reply_text += f'**Number of episodes:** {episodes}\n'
    if anime_info['average_duration'] != 'unknown':
        avg_duration = anime_info['average_duration']
        reply_text += f'**Average Duration:** {avg_duration}\n'
    if anime_info['status'] != 'unknown':
        status = anime_info['status']
        reply_text += f'**Status:** {status}\n'
    if anime_info['genres'] != 'unknown':
        genres = anime_info['genres']
        reply_text += f'**Genres:** {genres}\n'
    if anime_info['studios'] != 'unknown':
        studios = anime_info['studios']
        reply_text += f'**Studio:** {studios}\n'
    if anime_info['description'] != 'unknown':
        description = anime_info['description']
        if len(description) > 200:
            reply_text += '\n' + description[:200] + '...' + '\n'
        else:
            reply_text += '\n' + description + '\n'
    if anime_info['is_hentai'] != 'unknown':
        if str(anime_info['is_hentai']) == 'True':
            reply_text += '**⚠️ Seems to be a Hentai!**\n'
    if anime_info['anilist_url'] != 'unknwon':
        reply_text += anime_info['anilist_url'] 

    reply_embed = discord.Embed(title=f'Anime Info', colour=discord.Colour.blue())
    reply_embed.add_field(name=anime_info['anime'], value=reply_text)

    if anime_info['image'] != 'unknown':
        reply_embed.set_thumbnail(url=anime_info['image'])
    
    await channel.send(embed=reply_embed)

async def anime_description(channel, query):
    '''
    When someone wants the description of an anime
    '''
    anime_info = erina_discord_infoparser.search_anime_by_title(query)
    reply_text = ''
    anime = anime_info['anime']
    description = anime_info['description']
    if len(description) > 2000:
        reply_text += '\n' + description[:2000] + '...' + '\n'
    else:
        reply_text += '\n' + description + '\n'
    if anime_info['anilist_url'] != 'unknwon':
        reply_text += anime_info['anilist_url'] 
    reply_embed = discord.Embed(title=f'Anime Description: {anime}', description=reply_text, colour=discord.Colour.blue())

    if anime_info['image'] != 'unknown':
        reply_embed.set_thumbnail(url=anime_info['image'])
    
    await channel.send(embed=reply_embed)
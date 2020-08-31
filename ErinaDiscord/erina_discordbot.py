"""
Erina Discord Client for the Erina Project

@author: Anime no Sekai
Erina Project - 2020
"""
import sys
sys.path.append('..')

### PYTHON BUILT-IN
import asyncio
import random

### INSTALLED WITH PIP
from discord.ext import commands # to get discord commands
import discord # to communicate with discord
import filecenter

import config
import erina_log
from . import erina_discord_infoparser

### REACTION EMOJI WHILE MESSAGE RECEIVED (FROM MY DISCORD SERVER)
roger_reaction = '<:easygif_roger:712005159676411914>'

### DEFINING CLIENT/BOT AND ITS PREFIX 
client = commands.Bot(command_prefix='.')

# WHEN THE BOT IS UP
@client.event
async def on_ready():
    '''
    When the bot is ready
    '''
    await client.change_presence(activity=discord.Game(name='Ready to give you the sauce!')) # GAME ACTIVITY
    erina_log.logdiscord('[Discord] Erina is ready.', 'ready') # LOG THAT THE BOT IS READY


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

async def erinainvite(channel):
    '''
    When someone wants to invite Erina to another server
    '''
    await channel.send(content="I'm glad that you wanna share me with your friends!")
    await asyncio.sleep(2)
    await channel.send(content="Here is the link: **https://bit.ly/invite-erina-discord**")

async def erinastats(channel):
    '''
    When someone wants to know the bot's stats
    '''
    number_of_servers_erina_is_in = str(len(client.guilds))
    latency = round(client.latency * 1000,2)
    users = str(len(client.users))
    embed = discord.Embed(title='ErinaSauce Bot Stats', colour=discord.Colour.blue())
    embed.add_field(name='Stats', value=f"Version: **ErinaSauce v.0.8 (Beta)**\nPing/Latency: **{latency}ms**\nNumber of servers: **{number_of_servers_erina_is_in}**\nNumber of users: **{users}**\nDeveloper: **Anime no Sekai**\nProgramming Language: **Python**")
    embed.add_field(name='Powered by', value="ErinaSauce\nAniList\nTrace.moe\nManami Project\nGitHub\nDiscord")
    await channel.send(embed=embed)
    
async def erinadev(channel):
    '''
    When someone wants the repo link
    '''
    await channel.send(content="Thank's for having interest in the development of ErinaSauce!")
    await asyncio.sleep(random.uniform(0.8, 1.3))
    donatelink_embed = discord.Embed(title='GitHub Repository', colour=discord.Colour.blue())
    donatelink_embed.add_field(name='**GitHub**', value="https://github.com/Animenosekai/ErinaSauce")
    donatelink_embed.set_footer(text="©Anime no Sekai - Thank you for using ErinaSauce!")
    await channel.send(embed=donatelink_embed)

async def erinahelp(channel, author):
    '''
    When someone wants some help with the bot commands
    '''
    embed = discord.Embed(title='ErinaSauce Help Center', colour=discord.Colour.blue())
    embed.add_field(name='Available Commands', value="`anime_info <anime title>`: Searches an anime with the terms you provided and gives you infos on it.\n`anime_description`: Gives you the full description of the given anime.\nAsk `'what anime is it?'` or other variants to get the source of the anime of the given image (attachment) or the first image from the last 3 messages.\n`erinainvite`: Gives you a link to invite ErinaSauce on any discord server.\n`erinastats`: Gives ErinaSauce bot stats\n`erinadev`: Gives you a link to ErinaSauce github repo.\n`erinahelp`: Sends the message you are currently reading.")
    embed.set_author(name=f"Requested by {author}")
    embed.set_footer(text="ErinaSauce by Anime no Sekai - 2020")
    await channel.send(embed=embed)

async def erinadonate(channel):
    '''
    When someone wants to donate to help me developing stuff
    '''
    await channel.send(content="Thank's for having interest in the development of ErinaSauce!")
    await asyncio.sleep(random.uniform(1.5, 2.3))
    await channel.send(content="The fact that you're using this bot is already amazing")
    await asyncio.sleep(random.uniform(0.8, 1.5))
    await channel.send(content="But I won't lie, keeping the database and the server alive will cost me money someday")
    await asyncio.sleep(random.uniform(0.8, 1.5))
    donatelink_embed = discord.Embed(title='Donation Links', colour=discord.Colour.blue())
    donatelink_embed.add_field(name='**PayPal**', value="https://paypal.me/animenosekai")
    donatelink_embed.add_field(name='**uTip** (if you want to help me without spending anything)', value="https://utip.io/animenosekai")
    donatelink_embed.set_footer(text="©Anime no Sekai - Thank you for using ErinaSauce!")
    await channel.send(embed=donatelink_embed)

@client.event
async def on_message(message):
    '''
    When the bot receives a message
    '''

    # Variable declaration
    message_content = message.content
    list_of_results = []
    asking_for_anime_source = False
    source_flags = config.discord_flags

    # If someone wants informations about an anime
    if message.content.startswith('anime_info'):
        erina_log.logdiscord(f"→ Request of Anime Info came from the server: {message.guild} (user: {message.author})")
        search_query = message.content
        search_query = search_query.replace('anime_info ', '')
        erina_log.logdiscord(stattype='anime_info_request', value={"server": str(message.guild), "user": str(message.author), "query": str(search_query)})
        await message.add_reaction(roger_reaction) # REACT TO SHOW THAT THE BOT HAS UNDESTAND HIS COMMAND
        status = await message.channel.send(f'Please wait until I get the informations about {search_query}...')
        await anime_search(message.channel, search_query)
        await status.delete()
        erina_log.logdiscord(f"← Anime Info sent to {message.author}", 'anime_info_successful')

    # If someone wants the description of an anime
    elif message.content.startswith('anime_description'):
        erina_log.logdiscord(f"→ Request of Anime Description came from the server: {message.guild} (user: {message.author})")
        search_query = message.content
        search_query = search_query.replace('anime_description ', '')
        erina_log.logdiscord(stattype='anime_description_request', value={"server": str(message.guild), "user": str(message.author), "query": str(search_query)})
        await message.add_reaction(roger_reaction) # REACT TO SHOW THAT THE BOT HAS UNDESTAND HIS COMMAND
        status = await message.channel.send(f'Please wait until I get the informations about {search_query}...')
        await anime_description(message.channel, search_query)
        await status.delete()
        erina_log.logdiscord(f"← Anime Description sent to {message.author}", 'anime_description_successful')

    # If someone wants help with the bot
    elif message.content.startswith('erinahelp'):
        erina_log.logdiscord(f"→ Help request came from the server: {message.guild}  (user: {message.author})", 'helpcenter_request')
        await message.add_reaction(roger_reaction) # REACT TO SHOW THAT THE BOT HAS UNDESTAND HIS COMMAND
        await erinahelp(message.channel, message.author)
        erina_log.logdiscord(f"← Help Center sent on {message.guild} to {message.author}")

    # If someone wants the bot's stats
    elif message.content.startswith('erinastats'):
        erina_log.logdiscord(f"→ ErinaSauce Bot Stats request came from the server: {message.guild}  (user: {message.author})", 'erina_stats_request')
        await message.add_reaction(roger_reaction) # REACT TO SHOW THAT THE BOT HAS UNDESTAND HIS COMMAND
        await erinastats(message.channel)
        erina_log.logdiscord(f"← ErinaSauce Bot Stats sent on {message.guild} to {message.author}")

    # If someone wants to help with Erina's dev (repo link)
    elif message.content.startswith('erinadev'):
        erina_log.logdiscord(f"→ Development links request came from the server: {message.guild}  (user: {message.author})", 'erinadev_request')
        await message.add_reaction(roger_reaction) # REACT TO SHOW THAT THE BOT HAS UNDESTAND HIS COMMAND
        await erinadev(message.channel)
        erina_log.logdiscord(f"← Development links sent on {message.guild} to {message.author}")

    # If someone wants to invite Erina on another server
    elif message.content.startswith('erinainvite'):
        erina_log.logdiscord(f"→ Invite link request came from the server: {message.guild}  (user: {message.author})", 'erinainvite_request')
        await message.add_reaction(roger_reaction) # REACT TO SHOW THAT THE BOT HAS UNDESTAND HIS COMMAND
        await erinainvite(message.channel)
        erina_log.logdiscord(f"← Invite link sent on {message.guild} to {message.author}")

    # If someone wants to donate
    elif message.content.startswith('erinadonate'):
        erina_log.logdiscord(f"→ Donation request came from the server: {message.guild}  (user: {message.author})", 'erinadonate_request')
        await message.add_reaction(roger_reaction) # REACT TO SHOW THAT THE BOT HAS UNDESTAND HIS COMMAND
        await erinadonate(message.channel)
        erina_log.logdiscord(f"← Donation links sent on {message.guild} to {message.author}")
    


    # Any other message
    else:

        ############ SEARCH THE MESSAGE HAS ONE OF THE FLAG ############
        for flag in source_flags:
            if message_content.lower().find(flag) != -1: # If someone wants to search for an anime, based on a picture
                asking_for_anime_source = True
                erina_log.logdiscord(f"→ Anime source search came from the server: {message.guild} (user: {message.author})", 'source_search_request')
                break

        ############ SEARCHING FOR AN IMAGE ############
        if asking_for_anime_source:
            await message.add_reaction(roger_reaction) # REACT TO SHOW THAT THE BOT HAS UNDESTAND HIS COMMAND
            #status = await message.channel.send(f'Please wait until I get the informations about {search_query}...')
            if not len(message.attachments) == 0: # If the image got sent with the message
                for file in message.attachments:
                    if filecenter.type_from_extension(filecenter.extension_from_base(file.filename)) == 'Image': # If the file is an image
                        current_image = file.url
                        erina_log.logdiscord(stattype='source_search', value=current_image)
                        current_anime = erina_discord_infoparser.search_anime_by_imageurl(current_image) # Get infos about the anime
                        list_of_results.append(current_anime) # Append to the results list
            else:
                message_history = await message.channel.history(limit=3).flatten() # Search from the last 3 messages a picture 
                for message in message_history:
                    if not len(message.attachments) == 0:
                        for file in message.attachments:
                            if filecenter.type_from_extension(filecenter.extension_from_base(file.filename)) == 'Image':
                                current_image = file.url
                                current_anime = erina_discord_infoparser.search_anime_by_imageurl(current_image)
                                list_of_results.append(current_anime)
                                break
                        break


            ############ SEARCHING AND CREATING THE REPLY ############
            if len(list_of_results) != 0:

                ############ IF THERE IS ONLY ONE IMAGE ############
                if len(list_of_results) == 1:

                    anime_info = list_of_results[0]

                    await message.channel.send(f"It seems to be {list_of_results[0]['anime']}!")

                    reply_embed = discord.Embed(title=f'Anime Info', colour=discord.Colour.blue())
                    reply_embed.add_field(name=list_of_results[0]['anime'], value=anime_info['reply'])
                    
                    if 'image' in anime_info and anime_info['image'] != '':
                        reply_embed.set_thumbnail(url=anime_info['image'])

                    await asyncio.sleep(1)
                    await message.channel.send(embed=reply_embed)

                ############ IF THERE IS MULTIPLE IMAGES ############
                else:
                    iteration = 0
                    for search_result in list_of_results:

                        iteration += 1
                        number = ''
                        if iteration == 1:
                            number = '1st'
                        elif iteration == 2:
                            number = '2nd'
                        elif iteration == 3:
                            number = '3rd'
                        else:
                            number = f'{str(iteration)}th'


                        anime_info = search_result

                        #### FIRST REPLY
                        await message.channel.send(f"The {number} anime seems to be {anime_info['anime']}!")

                        reply_embed = discord.Embed(title=f'Anime Info', colour=discord.Colour.blue())
                        reply_embed.add_field(name=anime_info['anime'].capitalize(), value=anime_info['reply'])
                        
                        if 'image' in anime_info and anime_info['image'] != '':
                            reply_embed.set_thumbnail(url=anime_info['image'])
                        
                        await asyncio.sleep(1)
                        await message.channel.send(embed=reply_embed)
                erina_log.logdiscord(f"← Search result sent to {message.author}", 'successful_search_request')

# Run the bot with my ErinaSauce bot token
#client.run(os.environ['erina-discordbot-token'])
"""
Erina Discord Client for the Erina Project

@author: Anime no Sekai
Erina Project - 2020
"""
import asyncio

import filecenter
import discord
from discord.ext import commands

import config
import erina_log
from ErinaSearch import erinasearch
from ErinaDiscord.utils import utils
from ErinaDiscord.utils import Parser
from ErinaDiscord.utils import StaticResponse
from ErinaDiscord.utils.cosine_similarity import searchCommand

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
    await client.change_presence(activity=discord.Game(name='.erina help | Ready to give you the sauce!')) # GAME ACTIVITY
    erina_log.logdiscord('[Discord] Erina is ready.', 'ready') # LOG THAT THE BOT IS READY


@client.event
async def on_message(message):
    '''
    When the bot receives a message
    '''
    await message.add_reaction(roger_reaction) # REACT TO SHOW THAT THE BOT HAS UNDESTAND HIS COMMAND    
    if message.content.startswith('.erina'): # ERINA SPECIFIC COMMAND
        utils.removeSpaceBefore(str(message.content)[:6])
        userCommand = utils.removeSpaceBefore(str(message.content)[:6])
        commandLength = len(userCommand.split(" ")[0])
        command, commandSimilarity = searchCommand(userCommand.split(" ")[0].lower())
        if commandSimilarity < 0.75:
            await message.channel.send("Sorry, this command is not available.")
        else:
            if command == "search":
                query = utils.removeSpaceBefore(userCommand[commandLength:])
                discordResponse = Parser.makeInfoResponse(erinasearch.searchAnime(query))
            elif command == "description":
                query = utils.removeSpaceBefore(userCommand[commandLength:])
                discordResponse = Parser.makeDescriptionResponse(erinasearch.searchAnime(query))
                await message.channel.send()
            elif command == "dev":
                StaticResponse.erinadev(message.channel)
            elif command == "donate":
                StaticResponse.erinadonate(message.channel)
            elif command == "help":
                StaticResponse.erinahelp(message.channel, message.author)
            elif command == "stats":
                StaticResponse.erinastats(message.channel)
            elif command == "invite":
                StaticResponse.erinainvite(message.channel)
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
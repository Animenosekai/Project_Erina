"""
Erina Discord Client for the Erina Project

@author: Anime no Sekai
Erina Project - 2020
"""
import asyncio

import filecenter
import discord
from discord.ext import commands as DiscordCommands

from Erina import config
from ErinaSearch import erinasearch
from ErinaDiscord.utils import utils
from ErinaDiscord.utils import Parser
from ErinaDiscord.utils import StaticResponse
from ErinaDiscord.utils.cosine_similarity import searchCommand

from Erina.erina_stats import StatsAppend
from Erina.erina_stats import discord as DiscordStats
from Erina.erina_log import log

### REACTION EMOJI WHILE MESSAGE RECEIVED (FROM MY DISCORD SERVER)
roger_reaction = '<:easygif_roger:712005159676411914>'

### DEFINING CLIENT/BOT AND ITS PREFIX 
client = DiscordCommands.Bot(command_prefix='')

# WHEN THE BOT IS UP
@client.event
async def on_ready():
    '''
    When the bot is ready
    '''
    await client.change_presence(activity=discord.Game(name='.erina help | Ready to give you the sauce!')) # GAME ACTIVITY
    log("ErinaDiscord", "Erina is ready")


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
            return
        else:
            if command == "search":
                query = utils.removeSpaceBefore(userCommand[commandLength:])
                log("ErinaDiscord", "New info hit from @" + str(message.author) + " (asking for " + str(query) + ")")
                StatsAppend(DiscordStats.infoHit, f"{str(query)} >>> {str(message.author)}")
                anime, thumbnail, discordResponse = Parser.makeInfoResponse(erinasearch.searchAnime(query))
                if discordResponse is not None:
                    newEmbed = discord.Embed(title='Anime Info', colour=discord.Colour.blue())
                    newEmbed.add_field(name=anime.capitalize(), value=discordResponse)
                    
                    if thumbnail is not None:
                        newEmbed.set_thumbnail(url=thumbnail)

                    await message.channel.send(embed=newEmbed)
            elif command == "description":
                query = utils.removeSpaceBefore(userCommand[commandLength:])
                log("ErinaDiscord", "New description hit from @" + str(message.author) + " (asking for " + str(query) + ")")
                StatsAppend(DiscordStats.descriptionHit, f"{str(query)} >>> {str(message.author)}")
                anime, thumbnail, discordResponse = Parser.makeDescriptionResponse(erinasearch.searchAnime(query))
                if discordResponse is not None:
                    newEmbed = discord.Embed(title=f'Anime Description: {str(anime)}', colour=discord.Colour.blue())
                    newEmbed.add_field(name=anime.capitalize(), value=discordResponse)
                    
                    if thumbnail is not None:
                        newEmbed.set_thumbnail(url=thumbnail)

                    await message.channel.send(embed=newEmbed)
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
        if any([flag in str(message.content).lower() for flag in (config.Discord.flags if str(config.Discord.flags).replace(" ", "") not in ["None", ""] else config.Erina.flags)]):
            listOfResults = []
            await message.add_reaction(roger_reaction) # REACT TO SHOW THAT THE BOT HAS UNDESTAND HIS COMMAND
            log("ErinaDiscord", "New image search from @" + str(message.author))
            StatsAppend(DiscordStats.imageSearchHit, f"From {str(message.author)}")
            for file in message.attachments:
                if filecenter.type_from_extension(filecenter.extension_from_base(file.filename)) == 'Image': # If the file is an image
                    current_anime = Parser.makeImageResponse(erinasearch.imageSearch(file.url)) # Get infos about the anime
                    listOfResults.append(current_anime) # Append to the results list
            else:
                message_history = await message.channel.history(limit=5).flatten() # Search from the last 3 messages a picture 
                for message in message_history:
                    for file in message.attachments:
                        if filecenter.type_from_extension(filecenter.extension_from_base(file.filename)) == 'Image': # If the file is an image
                            current_anime = Parser.makeImageResponse(erinasearch.imageSearch(file.url)) # Get infos about the anime
                            listOfResults.append(current_anime) # Append to the results list

            if len(listOfResults) == 0:
                await message.channel.send("Sorry, I couldn't find anything...")
            
            elif len(listOfResults) == 1:
                title, thumbnail, reply = listOfResults[0]
                if reply is None:
                    await message.channel.send("An error occured while retrieving information on the anime...")

                await message.channel.send(f"It seems to be {title}!")

                newEmbed = discord.Embed(title='Anime Info', colour=discord.Colour.blue())
                newEmbed.add_field(name=title.capitalize(), value=reply)
                
                if thumbnail is not None:
                    newEmbed.set_thumbnail(url=thumbnail)

                await message.channel.send(embed=newEmbed)
                await asyncio.sleep(1)

            else:
                for iteration, result in enumerate(listOfResults):
                    number = ''
                    if iteration == 0:
                        number = '1st'
                    elif iteration == 1:
                        number = '2nd'
                    elif iteration == 2:
                        number = '3rd'
                    else:
                        number = f'{str(iteration)}th'

                    title, thumbnail, reply = result
                    if reply is None:
                        continue

                    await message.channel.send(f"The {number} anime seems to be {title}!")

                    newEmbed = discord.Embed(title='Anime Info', colour=discord.Colour.blue())
                    newEmbed.add_field(name=title.capitalize(), value=reply)
                    
                    if thumbnail is not None:
                        newEmbed.set_thumbnail(url=thumbnail)
                    
                    await message.channel.send(embed=newEmbed)
                    await asyncio.sleep(1)
    return

def disconnect():
    """
    Disconnects the bot
    """
    client.close()
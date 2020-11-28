import discord

async def erinainvite(channel):
    '''
    When someone wants to invite Erina to another server
    '''
    await channel.send(content="I'm glad that you wanna share me with your friends!")
    await channel.send(content="Here is the link: **https://bit.ly/invite-erina-discord**")

async def erinastats(channel):
    '''
    When someone wants to know the bot's stats
    '''
    embed = discord.Embed(title='ErinaSauce Bot Stats', colour=discord.Colour.blue())
    embed.add_field(name='Stats', value=f"Version: **ErinaSauce v.2.0 (Stable)**\nPing/Latency: **{round(client.latency * 1000,2)}ms**\nNumber of servers: **{str(len(client.guilds))}**\nNumber of users: **{str(len(client.users))}**\nDeveloper: **Anime no Sekai**\nProgramming Language: **Python**")
    embed.add_field(name='Powered by', value="ErinaSauce\nAniList\nTrace.moe\nSauceNAO\nIQDB\nManami-Project")
    await channel.send(embed=embed)
    
async def erinadev(channel):
    '''
    When someone wants the repo link
    '''
    await channel.send(content="Thank's for having interest in the development of ErinaSauce!")
    donatelink_embed = discord.Embed(title='GitHub Repository', colour=discord.Colour.blue())
    donatelink_embed.add_field(name='**GitHub**', value="https://github.com/Animenosekai/ErinaSauce")
    donatelink_embed.set_footer(text="©Anime no Sekai - Thank you for using ErinaSauce!")
    await channel.send(embed=donatelink_embed)

async def erinahelp(channel, author):
    '''
    When someone wants some help with the bot commands
    '''
    embed = discord.Embed(title='ErinaSauce Help Center', colour=discord.Colour.blue())
    embed.add_field(name='Available Commands', value="`.erina search <anime title>`: Gives you information on the given anime.\n`.erina description`: Gives you the full description of the given anime.\nAsk `'what anime is it?'` or other variants to get the source of the anime of the given image (attachment) or the last messages.\n`.erina invite`: Gives you a link to invite ErinaSauce on any discord server.\n`.erina stats`: Gives ErinaSauce bot stats\n`.erina dev`: Gives you a link to ErinaSauce GitHub repo.\n`.erina help`: Sends the message you are currently reading.")
    embed.set_author(name=f"Requested by {author}")
    embed.set_footer(text="ErinaSauce by Anime no Sekai - 2020")
    await channel.send(embed=embed)

async def erinadonate(channel):
    '''
    When someone wants to donate to help me developing stuff
    '''
    await channel.send(content="Thank's for having interest in the development of ErinaSauce!")
    await channel.send(content="The fact that you're using this bot is already amazing")
    await channel.send(content="Keeping the server alive will cost me money someday and any donation would be awesome!")

    donatelink_embed = discord.Embed(title='Donation Links', colour=discord.Colour.blue())
    donatelink_embed.add_field(name='**PayPal**', value="https://paypal.me/animenosekai")
    donatelink_embed.add_field(name='**uTip** (if you want to help me without spending anything)', value="https://utip.io/animenosekai")
    donatelink_embed.set_footer(text="©Anime no Sekai - Thank you for using ErinaSauce!")
    await channel.send(embed=donatelink_embed)

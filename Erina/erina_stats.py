"""
Erina Stats Managing API
"""

from time import time
from Erina.stats import files
from Erina.config import Erina as ErinaConfig

api = files.apiStats()
db = files.dbStats()
discord = files.discordStats()
erinahash = files.erinahashStats()
erina = files.erinaStats()
external = files.externalStats()
line = files.lineStats()
search = files.searchStats()
twitter = files.twitterStats()

def StatsAppend(file, content=None):
    """
    Appends a new stat event to the given file
    """
    if ErinaConfig.stats:
        if content is not None:
            file.append(f"{str(int(time()))}    {str(content)}".replace("\n", "") + "\n")
        else:
            file.append(str(int(time())) + "\n")

def StatsReset():
    """
    Resets the stats
    """
    api.searchEndpointCall.write("")
    db.erinaDatabaseLookups.write("")
    db.manamiDBTitleVectorLookups.write("")
    discord.descriptionHit.write("")
    discord.imageSearchHit.write("")
    discord.infoHit.write("")
    erinahash.createdBase64String.write("")
    erinahash.createdHashes.write("")
    erina.cacheFilesCount.write("")
    erina.erinaParsingCount.write("")
    erina.errorsCount.write("")
    erina.fileIOCounter.write("")
    external.anilistAPICalls.write("")
    external.iqdbCalls.write("")
    external.saucenaoAPICalls.write("")
    external.tracemoeAPICalls.write("")
    line.descriptionHit.write("")
    line.imageSearchHit.write("")
    line.infoHit.write("")
    line.storedImages.write("")
    search.searchCount.write("")
    search.anilistIDSearchCount.write("")
    search.imageSearchCount.write("")
    search.titleSearchCount.write("")
    twitter.askingHit.write("")
    twitter.directMessagingHit.write("")
    twitter.responsePolarity.write("")
    twitter.responses.write("")
    twitter.streamHit.write("")
    
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
    if ErinaConfig.stats:
        if content is not None:
            file.append(f"{str(int(time()))}    {str(content)}".replace("\n", "") + "\n")
        else:
            file.append(str(int(time())) + "\n")
from time import time
from Erina.stats import files

api = files.apiStats()
db = files.dbStats()
discord = files.discordStats()
erinahash = files.erinahashStats()
erina = files.erinaStats()
external = files.externalStats()
line = files.lineStats()
search = files.searchStats()
twitter = files.twitterStats()

def StatsAppend(file, content):
    file.append(f"{str(time())}    {str(content)}".replace("\n", "") + "\n")
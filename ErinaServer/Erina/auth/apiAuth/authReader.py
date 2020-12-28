
from safeIO import TextFile

from Erina.env_information import erina_dir
from Erina.utils import convert_to_float, convert_to_int

class APIAuth():
    def __init__(self, key) -> None:
        self.key = str(key)
        self.authFile = TextFile(erina_dir + "/ErinaServer/Erina/auth/apiAuth/" + self.key + ".erina")
        self.name = None
        self.rate_limit = None
        self.stats = []
        inStats = False
        for line in self.authFile:
            currentLine = line.replace("\n", "")
            if currentLine[:5] == "Name:":
                self.name = currentLine[6:]
            elif currentLine[:11] == "Rate Limit:":
                self.rate_limit = convert_to_float(currentLine[12:])
            elif currentLine == "----STATS----":
                inStats = True
            elif inStats:
                self.stats.append(convert_to_int(currentLine))
    
    def as_dict(self):
        return {
            "key": self.key,
            "name": self.name,
            "rateLimit": self.rate_limit,
            "usage": self.stats
        }
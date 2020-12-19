from time import time
from datetime import datetime
from Erina.erina_log import log
from Erina.erina_stats import StatsAppend
from Erina.erina_stats import erina

class TwitterError():
    """
    A twitter client error
    """
    def __init__(self, type, message) -> None:
        self.type = str(type)
        self.message = str(message)
        self.timestamp = time()
        self.datetime = datetime.fromtimestamp(self.timestamp)
        self.formatted_timestamp = f"{str(self.datetime.year)}-{str(self.datetime.month)}-{str(self.datetime.day)} at {str(self.datetime.hour)}:{str(self.datetime.minute)}:{str(self.datetime.second)}"
        log("ErinaTwitter", self.type + ": " + self.message, error=True)
        StatsAppend(erina.errorsCount, "ErinaTwitter")
    
    def __repr__(self) -> str:
        return f"{str(self.formatted_timestamp)}   ErinaTwitter >> [{self.type}] {self.message}"
"""
All of the errors class
"""

from time import time
from datetime import datetime
from Erina.erina_log import log
from Erina.erina_stats import StatsAppend
from Erina.erina_stats import erina



class CachingError():
    """
    A caching error
    """
    def __init__(self, type, message) -> None:
        self.type = str(type)
        self.message = str(message)
        self.timestamp = time()
        self.datetime = datetime.fromtimestamp(self.timestamp)
        self.formatted_timestamp = f"{str(self.datetime.year)}-{str(self.datetime.month)}-{str(self.datetime.day)} at {str(self.datetime.hour)}:{str(self.datetime.minute)}:{str(self.datetime.second)}"
        log("ErinaCaches", self.type + ": " + self.message, error=True)
        StatsAppend(erina.errorsCount, "ErinaCaches")
    
    def __repr__(self) -> str:
        return f"{str(self.formatted_timestamp)} ErinaCaches >> [{self.type}] {self.message}"


class DatabaseError():
    """
    A database error
    """
    def __init__(self, type, message) -> None:
        self.type = str(type)
        self.message = str(message)
        self.timestamp = time()
        self.datetime = datetime.fromtimestamp(self.timestamp)
        self.formatted_timestamp = f"{str(self.datetime.year)}-{str(self.datetime.month)}-{str(self.datetime.day)} at {str(self.datetime.hour)}:{str(self.datetime.minute)}:{str(self.datetime.second)}"
        log("ErinaDB", self.type + ": " + self.message, error=True)
        StatsAppend(erina.errorsCount, "ErinaDB")
    
    def __repr__(self) -> str:
        return f"{str(self.formatted_timestamp)} ErinaDatabase >> [{self.type}] {self.message}"


class DiscordError():
    """
    A discord client error
    """
    def __init__(self, type, message) -> None:
        self.type = str(type)
        self.message = str(message)
        self.timestamp = time()
        self.datetime = datetime.fromtimestamp(self.timestamp)
        self.formatted_timestamp = f"{str(self.datetime.year)}-{str(self.datetime.month)}-{str(self.datetime.day)} at {str(self.datetime.hour)}:{str(self.datetime.minute)}:{str(self.datetime.second)}"
        log("ErinaDiscord", self.type + ": " + self.message, error=True)
        StatsAppend(erina.errorsCount, "ErinaDiscord")
    
    def __repr__(self) -> str:
        return f"{str(self.formatted_timestamp)}   ErinaDiscord >> [{self.type}] {self.message}"


class HashingError():
    """
    A hash error
    """
    def __init__(self, type, message) -> None:
        self.type = str(type)
        self.message = str(message)
        self.timestamp = time()
        self.datetime = datetime.fromtimestamp(self.timestamp)
        self.formatted_timestamp = f"{str(self.datetime.year)}-{str(self.datetime.month)}-{str(self.datetime.day)} at {str(self.datetime.hour)}:{str(self.datetime.minute)}:{str(self.datetime.second)}"
        log("ErinaHash", self.type + ": " + self.message, error=True)
        StatsAppend(erina.errorsCount, "ErinaHash")
    
    def __repr__(self) -> str:
        return f"{str(self.formatted_timestamp)} ErinaHash >> [{self.type}] {self.message}"

class LineError():
    """
    A LINE client error
    """
    def __init__(self, type, message) -> None:
        self.type = str(type)
        self.message = str(message)
        self.timestamp = time()
        self.datetime = datetime.fromtimestamp(self.timestamp)
        self.formatted_timestamp = f"{str(self.datetime.year)}-{str(self.datetime.month)}-{str(self.datetime.day)} at {str(self.datetime.hour)}:{str(self.datetime.minute)}:{str(self.datetime.second)}"
        log("ErinaLine", self.type + ": " + self.message, error=True)
        StatsAppend(erina.errorsCount, "ErinaLine")
    
    def __repr__(self) -> str:
        return f"{str(self.formatted_timestamp)} ErinaLine >> [{self.type}] {self.message}"


class ParserError():
    """
    A .erina parser error
    """
    def __init__(self, type, message) -> None:
        self.type = str(type)
        self.message = str(message)
        self.timestamp = time()
        self.datetime = datetime.fromtimestamp(self.timestamp)
        self.formatted_timestamp = f"{str(self.datetime.year)}-{str(self.datetime.month)}-{str(self.datetime.day)} at {str(self.datetime.hour)}:{str(self.datetime.minute)}:{str(self.datetime.second)}"
        log("ErinaParser", self.type + ": " + self.message, error=True)
        StatsAppend(erina.errorsCount, "ErinaParser")
    
    def __repr__(self) -> str:
        return f"{str(self.formatted_timestamp)} ErinaParser >> [{self.type}] {self.message}"


class SearchingError():
    """
    A search engine error
    """
    def __init__(self, type, message) -> None:
        self.type = str(type)
        self.message = str(message)
        self.timestamp = time()
        self.datetime = datetime.fromtimestamp(self.timestamp)
        self.formatted_timestamp = f"{str(self.datetime.year)}-{str(self.datetime.month)}-{str(self.datetime.day)} at {str(self.datetime.hour)}:{str(self.datetime.minute)}:{str(self.datetime.second)}"
        log("ErinaSearch", self.type + ": " + self.message, error=True)
        StatsAppend(erina.errorsCount, "ErinaSearch")
    
    def __repr__(self) -> str:
        return f"{str(self.formatted_timestamp)} ErinaSearch >> [{self.type}] {self.message}"



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


def isAnError(element):
    """
    Wether the given element is an error or not
    """
    return isinstance(element, (CachingError, DatabaseError, DiscordError, HashingError, LineError, ParserError, SearchingError, TwitterError))
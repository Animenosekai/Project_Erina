import datetime
from ErinaParser.utils import utils


class ErinaCache():
    class CacheTimestamp():
        """
        A cache file timestamp object
        """
        def __init__(self, timestamp) -> None:
            self.datetime = datetime.datetime.fromtimestamp(utils.convert_to_float(timestamp))
            self.timestamp = timestamp
            self.formatted = f"{str(self.datetime.year)}-{str(self.datetime.month)}-{str(self.datetime.day)} at {str(self.datetime.hour)}:{str(self.datetime.minute)}:{str(self.datetime.second)}"

        def __repr__(self) -> str:
            return str(self.formatted)

        def as_dict(self):
            return {
                "timestamp": self.timestamp,
                "formatted": self.formatted
            }
    
    def __init__(self, data) -> None:
        # Normalize to get the same type of data everytime
        if isinstance(data, list):
            "\n".join(data)
        else:
            data = str(data)

        self.data = data.split("\n")

        self.path = None
        self.anilist_id = None
        self.hash = None
        self.similarity = None
        self.cache_timestamp = None

        for element in self.data:
            element = str(element).replace("\n", "")
            if element[:5] == 'Path:':
                self.path = str(element[6:])
            elif element[:11] == 'AniList ID:':
                self.anilist_id = str(element[12:])
            elif element[:5] == 'Hash:':
                self.hash = str(element[6:])
            elif element[:11] == 'Similarity:':
                self.similarity = utils.convert_to_float(element[12:])
            elif element[:16] == 'Cache Timestamp:':
                self.cache_timestamp = self.CacheTimestamp(element[17:])
    
    def as_dict(self):
        return {
            "path": self.path,
            "hash": self.hash,
            "similarity": self.similarity,
            "cacheTimestamp": (self.cache_timestamp.as_dict() if self.cache_timestamp is not None else None)
        }
         
    def __repr__(self) -> str:
        return str(self.path)
import datetime
from ErinaParser.utils import utils
from Erina.erina_stats import StatsAppend
from Erina.erina_stats import erina
class IQDBCache():
    class Size():
        """
        An image size object
        """
        def __init__(self, size) -> None:
            size = str(size)
            self.width = size.split('x')[0]
            self.height = size.split('x')[0]
            self.size = size
        
        def __repr__(self) -> str:
            return self.size
        
        def as_dict(self):
            return {
                "width": self.width,
                "height": self.height,
                "size": self.size
            }

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
        StatsAppend(erina.erinaParsingCount, "IQDB")
        # Normalize to get the same type of data everytime
        if isinstance(data, list):
            "\n".join(data)
        else:
            data = str(data)

        self.data = data.split("\n")

        self.tags = None
        self.link = None
        self.size = None
        self.hentai = None
        self.similarity = None
        self.database = None

        for element in self.data:
            element = str(element).replace("\n", "")

            if element[:10] == 'IQDB Tags:':
                self.tags = [utils.capitalize_string(tag) for tag in str(element[11:]).split(':::')]
            elif element[:4] == 'URL:':
                self.link = str(element[5:])
            elif element[:5] == 'Size:':
                self.size = self.Size(element[6:])
            elif element[:7] == 'isSafe:':
                self.hentai = utils.convert_to_boolean(element[8:])
            elif element[:11] == 'Similarity:':
                self.similarity = utils.convert_to_float(element[12:])
            elif element[:9] == 'Database:':
                self.database = str(element[10:])
            elif element[:16] == 'Cache Timestamp:':
                self.cache_timestamp = self.CacheTimestamp(element[17:])
    
    def as_dict(self):
        return {
            "tags": self.tags,
            "link": self.link,
            "size": (self.size.as_dict() if self.size is not None else None),
            "hentai": self.hentai,
            "similarity": self.similarity,
            "database": self.database,
            "cacheTimestamp": (self.cache_timestamp.as_dict() if self.cache_timestamp is not None else None)
        }
         
    def __repr__(self) -> str:
        return str(self.path)
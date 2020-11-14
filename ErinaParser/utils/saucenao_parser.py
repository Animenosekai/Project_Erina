import datetime
from ErinaParser.utils import utils

index_id_to_name = {
    0 : "HMagazines",
    2 : "HGame CG",
    3 : "DoujinshiDB",
    5 : "Pixiv Images",
    8 : "Nico Nico Seiga",
    9 : "Danbooru",
    10 : "Drawr Images",
    11 : "Nijie Images",
    12 : "Yandere",
    13 : "Openingsmoe",
    15 : "Shutterstock",
    16 : "FAKKU",
    18 : "HMisc",
    19 : "TwoDMarket",
    20 : "MediBang",
    21 : "Anime",
    22 : "HAnime",
    23 : "Movies",
    24 : "Shows",
    25 : "Gelbooru",
    26 : "Konachan",
    27 : "SankakuChannel",
    28 : "AnimePicturesnet",
    29 : "E621net",
    30 : "IdolComplex",
    31 : "Bcynet Illust",
    32 : "Bcynet Cosplay",
    33 : "PortalGraphicsnet",
    34 : "DeviantArt",
    35 : "Pawoonet",
    36 : "Madokami",
    37 : "MangaDex",
    38 : "HMisc EHentai",
    999 : "ALL"
}


class SauceNAOCache():
    class Index():
        """
        A SauceNAO Index (database)
        """
        def __init__(self, index) -> None:
            self.id = utils.convert_to_int(index)
            try:
                self.name = str(index_id_to_name[self.id])
            except:
                self.name = None
        
        def __repr__(self) -> str:
            return self.name
        
        def as_dict(self):
            return {
                "id": self.id,
                "name": self.name
            }


    class AnimeTitle():
        """
        An anime title
        """
        def __init__(self, romaji_title=None, english_title=None, native_title=None, chinese_title=None, alternative_titles=None) -> None:
            self.romaji_title = romaji_title
            self.english_title = english_title
            self.native_title = native_title
            self.chinese_title = chinese_title
            if isinstance(alternative_titles, list):
                self.alternative_titles = alternative_titles
            else:
                self.alternative_titles = [str(alternative_titles)]

        def __repr__(self) -> str:
            if self.romaji_title is not None:
                return str(self.romaji_title)
            elif self.english_title is not None:
                return str(self.english_title)
            elif self.native_title is not None:
                return str(self.native_title)
            elif self.alternative_titles is not None:
                return str(self.alternative_titles[0])
            elif self.chinese_title is not None:
                return str(self.chinese_title)
            else:
                return "<AnimeTitle Object>"


        def addTitle(self, romaji_title=None, english_title=None, native_title=None, chinese_title=None):
            """
            Adds a title (translation for example) to the object
            """
            if romaji_title is not None:
                self.romaji_title = str(romaji_title)
            elif english_title is not None:
                self.english_title = str(english_title)
            elif native_title is not None:
                self.native_title = str(native_title)
            elif chinese_title is not None:
                self.chinese_title = str(chinese_title)

        def addAlternativeTitle(self, alternative_title):
            if self.alternative_titles is None:
                if isinstance(alternative_title, list):
                    self.alternative_titles = alternative_title
                else:
                    self.alternative_titles = [str(alternative_title)]
            else:
                if isinstance(alternative_title, list):
                    self.alternative_titles.extend(alternative_title)
                else:
                    self.alternative_titles.append(str(alternative_title))

        def as_dict(self):
            """
            Converts the object as a dictionary
            """
            return {
                "title": self.__repr__(),
                "romajiTitle": self.romaji_title,
                "englishTitle": self.english_title,
                "nativeTitle": self.native_title,
                "chineseTitle": self.chinese_title,
                "alternativeTitles": self.alternative_titles
            }

    
    class Timing():
        """
        An anime scene timing (from, to, at) object
        """
        def __init__(self, from_time=None, to=None, at=None) -> None:
            if from_time is not None:
                self.from_time = utils.convert_to_float(from_time)
                self.from_formatted = str(datetime.timedelta(seconds=self.from_time))
            else:
                self.from_time = None
                self.from_formatted = None
            if to is not None:
                self.to = utils.convert_to_float(to)
                self.to_formatted = str(datetime.timedelta(seconds=self.to))
            else:
                self.to = None
                self.to_formatted = None
            if at is not None:
                self.at = utils.convert_to_float(at)
                self.at_formatted = str(datetime.timedelta(seconds=self.at))
            else:
                self.at = None
                self.at_formatted = None
            
        def addTiming(self, from_time=None, to=None, at=None) -> None:
            if from_time is not None:
                self.from_time = utils.convert_to_float(from_time)
                self.from_formatted = str(datetime.timedelta(seconds=self.from_time))
            else:
                self.from_time = None
                self.from_formatted = None
            if to is not None:
                self.to = utils.convert_to_float(to)
                self.to_formatted = str(datetime.timedelta(seconds=self.to))
            else:
                self.to = None
                self.to_formatted = None
            if at is not None:
                self.at = utils.convert_to_float(at)
                self.at_formatted = str(datetime.timedelta(seconds=self.at))
            else:
                self.at = None
                self.at_formatted = None
        
        def __repr__(self) -> str:
            if self.at is not None:
                return self.at_formatted
            elif self.from_time is not None:
                return self.from_formatted
            elif self.to is not None:
                return self.to_formatted
            else:
                return "<AnimeTiming object>"

        def as_dict(self):
            return {
                "from": self.from_time,
                "to": self.to,
                "at": self.at,
                "from_formatted": self.from_formatted,
                "to_formatted": self.to_formatted,
                "at_formatted": self.at_formatted
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
        # Normalize to get the same type of data everytime
        if isinstance(data, list):
            "\n".join(data)
        else:
            data = str(data)

        self.data = data.split("\n")

        self.similarity = None
        self.database = None
        self.title = None
        self.link = None
        self.author = None
        self.thumbnail = None
        self.is_manga = None
        self.is_anime = None
        self.part = None
        self.episode = None
        self.year = None
        self.timing = None
        self.cache_timestamp = None
        
        for element in self.data:
            element = str(element).replace("\n", "")

            if element[:11] == 'Similarity:':
                self.similarity = utils.convert_to_float(element[12:])
            elif element[:9] == 'Index ID:':
                self.database = self.Index(element[10:])
            elif element[:6] == 'Title:':
                self.title = self.AnimeTitle(native_title=element[7:])
            elif element[:4] == 'URL:':
                self.link = str(element[5:])
            elif element[:7] == 'Author:':
                self.author = str(element[8:])
            elif element[:10] == 'Thumbnail:':
                self.thumbnail = str(element[11:])
            elif element[:8] == 'isManga:':
                self.is_manga = utils.convert_to_boolean(element[9:])
            elif element[:5] == 'Part:':
                self.part = utils.convert_to_int(element[6:])
            elif element[:8] == 'isAnime:':
                self.is_anime = utils.convert_to_boolean(element[9:])
            elif element[:8] == 'Episode:':
                self.episode = utils.convert_to_int(element[9:])
            elif element[:5] == 'Year:':
                self.year = utils.convert_to_int(element[6:])
            elif element[:15] == 'Estimated Time:':
                self.timing = self.Timing(from_time=element[16:], to=element[16:], at=element[16:])
            elif element[:16] == 'Cache Timestamp:':
                self.cache_timestamp = self.CacheTimestamp(element[17:])

    def __repr__(self) -> str:
        return str(self.title)

    def as_dict(self):
        return {
            "similarity": self.similarity,
            "database": (self.database.as_dict() if self.database is not None else None),
            "title": (self.title.as_dict() if self.title is not None else None),
            "link": self.link,
            "author": self.author,
            "thumbnail": self.thumbnail,
            "isManga": self.is_manga,
            "isAnime": self.is_anime,
            "part": self.part,
            "episode": self.episode,
            "year": self.year,
            "timing": (self.timing.as_dict() if self.timing is not None else None),
            "cacheTimestamp": (self.cache_timestamp.as_dict() if self.cache_timestamp is not None else None)
        }
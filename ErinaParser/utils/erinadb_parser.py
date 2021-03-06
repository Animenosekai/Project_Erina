import datetime
from Erina import utils
from Erina.erina_stats import StatsAppend
from Erina.erina_stats import erina
class ErinaData():
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
                self.from_formatted = str(datetime.timedelta(seconds=self.from_time)).split(".")[0]
            else:
                self.from_time = None
                self.from_formatted = None
            if to is not None:
                self.to = utils.convert_to_float(to)
                self.to_formatted = str(datetime.timedelta(seconds=self.to)).split(".")[0]
            else:
                self.to = None
                self.to_formatted = None
            if at is not None:
                self.at = utils.convert_to_float(at)
                self.at_formatted = str(datetime.timedelta(seconds=self.at)).split(".")[0]
            else:
                self.at = None
                self.at_formatted = None
            
        def addTiming(self, from_time=None, to=None, at=None) -> None:
            if from_time is not None:
                self.from_time = utils.convert_to_float(from_time)
                self.from_formatted = str(datetime.timedelta(seconds=self.from_time)).split(".")[0]
            else:
                self.from_time = None
                self.from_formatted = None
            if to is not None:
                self.to = utils.convert_to_float(to)
                self.to_formatted = str(datetime.timedelta(seconds=self.to)).split(".")[0]
            else:
                self.to = None
                self.to_formatted = None
            if at is not None:
                self.at = utils.convert_to_float(at)
                self.at_formatted = str(datetime.timedelta(seconds=self.at)).split(".")[0]
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

    class AnalyzeTimestamp():
        """
        A database file timestamp object
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
        StatsAppend(erina.erinaParsingCount, "ErinaDB")
        # Normalize to get the same type of data everytime
        if isinstance(data, list):
            "\n".join(data)
        else:
            data = str(data)

        self.data = data.split("\n")

        self.anilist_id = None
        self.title = None
        self.season = None
        self.episode = None
        self.first_frame = None
        self.last_frame = None
        self.timing = None
        self.hash = None
        self.hash_algorithm = None
        self.filename = None
        self.framerate = None
        self.episode_duration = None
        self.episode_framecount = None
        self.analyze_timestamp = None
        
        for element in self.data:
            element = str(element).replace("\n", "")
            if element[:11] == 'AniList ID:':
                self.anilist_id = utils.convert_to_int(element[12:])
            elif element[:6] == 'Anime:':
                self.title = self.AnimeTitle(romaji_title=element[7:])
            elif element[:7] == 'Season:':
                self.season = utils.convert_to_int(element[8:])
            elif element[:8] == 'Episode:':
                self.episode = utils.convert_to_int(element[9:])
            elif element[:12] == 'First Frame:':
                self.first_frame = utils.convert_to_int(element[13:]) 
            elif element[:11] == 'Last Frame:':
                self.last_frame = utils.convert_to_int(element[12:])
            elif element[:5] == 'From:':
                if self.timing is None:
                    self.timing = self.Timing(from_time=element[6:])
                else:
                    self.timing.addTiming(from_time=element[6:])
            elif element[:3] == 'To:':
                if self.timing is None:
                    self.timing = self.Timing(to=element[4:])
                else:
                    self.timing.addTiming(to=element[4:])
            elif element[:3] == 'At:':
                if self.timing is None:
                    self.timing = self.Timing(at=element[4:])
                else:
                    self.timing.addTiming(at=element[4:])
            elif element[:5] == 'Hash:':
                self.hash = str(element[6:])
            elif element[:18] == 'Hashing Algorithm:':
                self.hash_algorithm = str(element[19:])
            elif element[:9] == 'Filename:':
                self.filename = str(element[10:])
            elif element[:18] == 'Episode Framerate:':
                self.framerate = utils.convert_to_float(element[19:])
            elif element[:17] == 'Episode Duration:':
                self.episode_duration = utils.convert_to_float(element[18:])
            elif element[:20] == 'Episode Frame Count:':
                self.episode_framecount = utils.convert_to_int(element[21:])
            elif element[:13] == 'Analyze Date:':
                self.analyze_timestamp = self.AnalyzeTimestamp(element[14:])
    
    def as_dict(self):
        return {
            "anilistID": self.anilist_id,
            "title": (self.title.as_dict() if self.title is not None else None),
            "season": self.season,
            "episode": self.episode,
            "firstFrame": self.first_frame,
            "lastFrame": self.last_frame,
            "timing": (self.timing.as_dict() if self.timing is not None else self.timing),
            "hash": self.hash,
            "hashAlgorithm": self.hash_algorithm,
            "filename": self.filename,
            "framerate": self.framerate,
            "episodeDuration": self.episode_duration,
            "episodeFramecount": self.episode_framecount,
            "analyzeTimestamp": (self.analyze_timestamp.as_dict() if self.analyze_timestamp is not None else None),
            "docType": "ERINADB"
        }

    def as_text(self):
        return ("\n".join(self.data) if self.data is not None else "No data")
         
    def __repr__(self) -> str:
        return str(self.title)
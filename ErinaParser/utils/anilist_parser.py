"""
A .erina AniList cache file parser

© Anime no Sekai - 2020
"""

import re
from Erina import utils
from datetime import datetime
from Erina.erina_stats import StatsAppend
from Erina.erina_stats import erina
class AnilistCache():
    
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
            elif alternative_titles is not None:
                self.alternative_titles = [str(alternative_titles)]
            else:
                self.alternative_titles = None
            

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


        
    class AnimeDescription():
        """
        An anime description
        """
        def __init__(self, description) -> None:
            self.html = str(description).replace("\n", "<br/>").replace("&quot;", '"')
            self.description = utils.textFromHTML(self.html)
            
        def __repr__(self) -> str:
            return str(self.description)

        def as_dict(self):
            return {
                "description": self.description,
                "html": self.html
            }

    class AnimeDate():
        """
        A date object
        """
        def __init__(self, date) -> None:
            self.date = str(date)
            self.year = utils.convert_to_int(date.split("-")[0])
            self.month = utils.convert_to_int(date.split("-")[1])
            self.day = utils.convert_to_int(date.split("-")[2])

        def __repr__(self) -> str:
            return str(self.date)

        def as_dict(self):
            return {
                "date": self.date,
                "year": self.year,
                "month": self.month,
                "day": self.day
            }

    class AnimeGenres():
        """
        An anime genre object
        """
        def __init__(self, genres) -> None:
            self.genres = list(genres)
        
        def __repr__(self) -> str:
            return utils.create_nice_list(self.genres)

        def as_dict(self):
            return self.genres

    class AnimeStudio():
        """
        An anime studio object
        """
        def __init__(self, data) -> None:
            #print(data)
            self.is_main = utils.convert_to_boolean(data[0])
            self.anilist_id = utils.convert_to_int(data[1])
            self.name = str(data[2])
            self.is_animation_studio = utils.convert_to_boolean(data[3])

        def __repr__(self) -> str:
            return str(self.name)

        def as_dict(self):
            return {
                "name": self.name,
                "isMain": self.is_main,
                "isAnimationStudio": self.is_animation_studio,
                "anilistID": self.anilist_id
            }

    class AnimeTag():
        """
        An anime tag object
        """
        def __init__(self, data) -> None:
            self.name = str(data[0])
            self.rank = utils.convert_to_int(data[1])
            self.is_spoiler = utils.convert_to_boolean(data[2])
            self.is_adult = utils.convert_to_boolean(data[3])
            self.category = str(data[4])
        
        def __repr__(self) -> str:
            return str(self.name)

        def as_dict(self):
            return {
                "name": self.name,
                "rank": self.rank,
                "isSpoiler": self.is_spoiler,
                "isAdult": self.is_adult,
                "category": self.category
            }

    class AnimeRelation():
        """
        An anime relation (anime related to the current object) object
        """
        def __init__(self, data) -> None:
            self.relation = str(data[0])
            self.anilist_id = utils.convert_to_int(data[1])
            self.title = str(data[2])

        def __repr__(self) -> str:
            return str(self.title)
        
        def as_dict(self):
            return {
                "title": self.title,
                "relation": self.relation,
                "anilistID": self.anilist_id
            }

    class AnimeCharacter():
        """
        An anime character object
        """
        def __init__(self, data) -> None:
            self.role = str(data[0])
            self.anilist_id = utils.convert_to_int(data[1])
            self.name = str(data[2])
            try:
                self.native_name = str(data[3])
            except:
                self.native_name = None

        def __repr__(self) -> str:
            if self.name is not None:
                return f"{str(self.name)} ({str(self.role)})"
            elif self.native_name is not None:
                return f"{str(self.native_name)} ({str(self.role)})"
            else:
                return str(self.role) + " character"

        def as_dict(self):
            return {
                "name": self.name,
                "nativeName": self.native_name,
                "role": self.role,
                "anilistID": self.anilist_id
            }

    class AnimeStaff():
        """
        An anime staff object
        """
        def __init__(self, data) -> None:
            self.role = str(data[0])
            self.anilist_id = utils.convert_to_int(data[1])
            self.name = str(data[2])
            try:
                self.native_name = str(data[3])
            except:
                self.native_name = None

        def __repr__(self) -> str:
            if self.name is not None:
                return f"{str(self.name)} ({str(self.role)})"
            elif self.native_name is not None:
                return f"{str(self.native_name)} ({str(self.role)})"
            else:
                return str(self.role)

        def as_dict(self):
            return {
                "name": self.name,
                "nativeName": self.native_name,
                "role": self.role,
                "anilistID": self.anilist_id
            }


    class AnimeRecommendation():
        """
        An anime recommendation object
        """
        def __init__(self, data) -> None:
            self.anilist_id = utils.convert_to_int(data[0])
            self.title = str(data[1])

        def __repr__(self) -> str:
            return str(self.title)

        def as_dict(self):
            return {
                "title": self.title,
                "anilistID": self.anilist_id
            }

    class AnimeStreamingLink():
        """
        An anime streaming link object
        """
        def __init__(self, link=None, episode=None, title=None) -> None:
            self.link = str(link)
            self.episode = utils.convert_to_int(episode)
            self.title = str(title)

        def __repr__(self) -> str:
            return str(self.link)

        def as_dict(self):
            return {
                "link": self.link,
                "title": self.title,
                "episode": self.episode
            }

    class AnimeExternalLink():
        """
        An anime external link object
        """
        def __init__(self, link=None, site=None) -> None:
            self.link = link
            self.site = site

        def __repr__(self) -> str:
            return str(self.link)

        def as_dict(self):
            return {
                "link": self.link,
                "site": self.site
            }
    
    class CacheTimestamp():
        """
        A cache file timestamp object
        """
        def __init__(self, timestamp) -> None:
            self.datetime = datetime.fromtimestamp(timestamp)
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
        StatsAppend(erina.erinaParsingCount, "AniList")
        # Normalize to get the same type of data everytime
        if isinstance(data, list):
            "\n".join(data)
        else:
            data = str(data)

        self.data = data.split("\n")
        episode_fallback = 0

        ### Data initialization
        self.anilist_id = None
        self.myanimelist_id = None
        self.title = None
        self.type = None
        self.format = None
        self.status = None
        self.description = None
        self.season = None
        self.year = None
        self.number_of_episodes = None
        self.episode_duration = None
        self.first_episode_release_date = None
        self.last_episode_release_date = None
        self.country = None
        self.source_type = None
        self.licensed = None
        self.hentai = None
        self.twitter_hashtag = None
        self.average_score = None
        self.cover_image = None
        self.average_cover_color = None
        self.banner_image = None
        self.trailer = None
        self.genres = None
        self.studios = None
        self.tags = None
        self.relations = None
        self.characters = None
        self.staff = None
        self.recommendations = None
        self.link = None
        self.streaming_links = None
        self.external_links = None
        self.cache_timestamp = None

        for element in self.data:
            element = str(element).replace("\n", "")
            #print(element)

            if element[:11] == "AniList ID:":
                self.anilist_id = utils.convert_to_int(element[12:])
            elif element[:15] == "MyAnimeList ID:":
                self.myanimelist_id = utils.convert_to_int(element[16:])
            elif element[:13] == 'Romaji Title:':
                if self.title is None:
                    self.title = self.AnimeTitle(element[14:])
                else:
                    self.title.addTitle(romaji_title=element[14:])
            elif element[:14] == 'English Title:':
                if self.title is None:
                    self.title = self.AnimeTitle(english_title=element[15:])
                else:
                    self.title.addTitle(english_title=element[15:])
            elif element[:13] == 'Native Title:':
                if self.title is None:
                    self.title = self.AnimeTitle(native_title=element[14:])
                else:
                    self.title.addTitle(native_title=element[14:])
            elif element[:21] == 'Alternative Title(s):':
                if self.title is None:
                    self.title = self.AnimeTitle(alternative_titles=element[22:].split(':::'))
                else:
                    self.title.addAlternativeTitle(element[22:].split(':::'))
            elif element[:5] == 'Type:':
                self.type = str(element[6:])
            elif element[:7] == 'Format:':
                self.format = str(element[8:])
            elif element[:7] == 'Status:':
                self.status = str(element[8:])
            elif element[:12] == 'Description:':
                self.description = self.AnimeDescription(element[13:])
            elif element[:7] == 'Season:':
                self.season = str(element[8:])
            elif element[:5] == 'Year:':
                self.year = utils.convert_to_int(element[6:])
            elif element[:9] == 'Episodes:':
                self.number_of_episodes = utils.convert_to_int(element[10:])
            elif element[:17] == 'Average Duration:':
                self.episode_duration = utils.convert_to_int(element[18:])
            elif element[:27] == 'First Episode Release Date:':
                self.first_episode_release_date = self.AnimeDate(element[28:])
            elif element[:26] == 'Last Episode Release Date:':
                self.last_episode_release_date = self.AnimeDate(element[27:])
            elif element[:8] == 'Country:':
                self.country = str(element[9:])
            elif element[:18] == 'Source Media Type:':
                self.source_type = str(element[19:])
            elif element[:9] == 'Licensed?':
                self.licensed = utils.convert_to_boolean(element[10:])
            elif element[:7] == 'Hentai?':
                self.hentai = utils.convert_to_boolean(element[8:])
            elif element[:16] == 'Twitter Hashtag:':
                self.twitter_hashtag = str(element[17:])
            elif element[:14] == 'Average Score:':
                self.average_score = utils.convert_to_int(element[15:])
            elif element[:12] == 'Cover Image:':
                self.cover_image = str(element[13:])                
            elif element[:20] == 'Average Cover Color:':
                self.average_cover_color == str(element[21:]) 
            elif element[:13] == 'Banner Image:':
                self.banner_image = str(element[14:])
            elif element[:8] == 'Trailer:':
                self.trailer = str(element[9:])
            elif element[:7] == 'Genres:':
                self.genres = self.AnimeGenres(element[8:].split(':::'))
            elif element[:8] == '[STUDIO]':
                if self.studios is None:
                    self.studios = [self.AnimeStudio(element[9:].split('｜｜｜'))]
                else:
                    self.studios.append(self.AnimeStudio(element[9:].split('｜｜｜')))
            elif element[:5] == '[TAG]':
                if self.tags is None:
                    self.tags = [self.AnimeTag(element[6:].split('｜｜｜'))]
                else:
                    self.tags.append(self.AnimeTag(element[6:].split('｜｜｜')))
            elif element[:10] == '[RELATION]':
                if self.relations is None:
                    self.relations = [self.AnimeRelation(element[11:].split('｜｜｜'))]
                else:
                    self.relations.append(self.AnimeRelation(element[11:].split('｜｜｜')))
            elif element[:11] == '[CHARACTER]':
                if self.characters is None:
                    self.characters = [self.AnimeCharacter(element[12:].split('｜｜｜'))]
                else:
                    self.characters.append(self.AnimeCharacter(element[12:].split('｜｜｜')))
            elif element[:7] == '[STAFF]':
                if self.staff is None:
                    self.staff = [self.AnimeStaff(element[8:].split('｜｜｜'))]
                else:
                    self.staff.append(self.AnimeStaff(element[8:].split('｜｜｜')))
            elif element[:16] == '[RECOMMENDATION]':
                if self.recommendations is None:
                    self.recommendations = [self.AnimeRecommendation(element[17:].split('｜｜｜'))]
                else:
                    self.recommendations.append(self.AnimeRecommendation(element[17:].split('｜｜｜')))
            elif element[:16] == '[streaming link]':
                episode_fallback += 1
                # Info extraction
                try:
                    element = element[17:]
                    link = re.findall("(https?:\/\/\S+)", element)[0]
                    if link.find('www.crunchyroll.com') != -1:
                        element = element.split(": http")[0].split(" - ")
                        episode = utils.convert_to_int(element[0].lower().replace("episode", ""))
                        title = str(element[1])
                    else:
                        element = element.split(": http")[0]
                        episode = episode_fallback + 1
                        title = str(element[0])
                    
                    # Appending results
                    if self.streaming_links is None:
                        self.streaming_links = [self.AnimeStreamingLink(link=link, episode=episode, title=title)]
                    else:
                        self.streaming_links.append(self.AnimeStreamingLink(link=link, episode=episode, title=title))
                except:
                    pass
                
            elif element[:15] == '[external link]':
                element = element[16:]
                link = re.findall("(https?:\/\/\S+)", element)[0]
                site = element.split(": ")[0]
                if self.external_links is None:
                    self.external_links = [self.AnimeExternalLink(link=link, site=site)]
                else:
                    self.external_links.append(self.AnimeExternalLink(link=link, site=site))
            elif element[:16] == 'Cache Timestamp:':
                self.cache_timestamp = self.CacheTimestamp(utils.convert_to_float(element[17:]))
        if self.anilist_id is not None:
            self.link = "https://anilist.co/anime/" + str(self.anilist_id)


    def __repr__(self) -> str:
        """
        Object string representation
        """
        return str(self.title)


    def as_dict(self):
        return {
            "anilistID": self.anilist_id,
            "myAnimeListID": self.myanimelist_id,
            "title": (self.title.as_dict() if self.title is not None else None),
            "type": self.type,
            "format": self.format,
            "status": self.status,
            "description": (self.description.as_dict() if self.description is not None else None),
            "season": self.season,
            "year": self.year,
            "numberOfEpisodes": self.number_of_episodes,
            "episodeDuration": self.episode_duration,
            "firstEpisodeReleaseDate": (self.first_episode_release_date.as_dict() if self.last_episode_release_date is not None else None),
            "lastEpisodeReleaseDate": (self.last_episode_release_date.as_dict() if self.first_episode_release_date is not None else None),
            "country": self.country,
            "sourceType": self.source_type,
            "licensed": self.licensed,
            "hentai": self.hentai,
            "twitterHashtag": self.twitter_hashtag,
            "averageScore": self.average_score,
            "coverImage": self.cover_image,
            "averageCoverColor": self.average_cover_color,
            "bannerImage": self.banner_image,
            "trailer": self.trailer,
            "genres": (self.genres.genres if self.genres is not None else None),
            "studios": ([studio.as_dict() for studio in self.studios] if self.studios is not None else None),
            "tags": ([tag.as_dict() for tag in self.tags] if self.tags is not None else None),
            "relations": ([relation.as_dict() for relation in self.relations] if self.relations is not None else None),
            "characters": ([character.as_dict() for character in self.characters] if self.characters is not None else None),
            "staff": ([staff.as_dict() for staff in self.staff] if self.staff is not None else None),
            "recommendations": ([recommendation.as_dict() for recommendation in self.recommendations] if self.recommendations is not None else None),
            "link": self.link,
            "streamingLinks": ([link.as_dict() for link in self.streaming_links] if self.streaming_links is not None else None),
            "externalLinks": ([link.as_dict() for link in self.external_links] if self.external_links is not None else None),
            "cacheTimestamp": (self.cache_timestamp.as_dict() if self.cache_timestamp is not None else None),
            "docType": "ANILIST"
        }

    def as_text(self):
        return ("\n".join(self.data) if self.data is not None else "No data")
"""
Parses ErinaSearch for Discord
"""
from ErinaParser.utils.utils import create_nice_list
from ErinaParser.utils.saucenao_parser import SauceNAOCache
from ErinaCaches.utils.Errors import CachingError
from ErinaDB.utils.Errors import DatabaseError
from ErinaHash.utils.Errors import HashingError
from ErinaParser.utils.Errors import ParserError
from ErinaSearch.utils.Errors import SearchingError

def makeInfoResponse(erinaSearchResponse):
    """
    Makes the response for info queries on Discord
    """
    return str(erinaSearchResponse.title), str(erinaSearchResponse.cover_image), f"""**Anime**: {(str(erinaSearchResponse.title) if erinaSearchResponse.title is not None else "Unknown")}
**Season**: {(str(erinaSearchResponse.season) if erinaSearchResponse.season is not None else (str(erinaSearchResponse.year) if erinaSearchResponse.year is not None else "N/A"))}{(("of " + str(erinaSearchResponse.year) if erinaSearchResponse.year is not None else "") if erinaSearchResponse.season is None else "")}
**Number of episodes**: {(str(erinaSearchResponse.number_of_episodes) if erinaSearchResponse.number_of_episodes is not None else "??")}
**Average Duration**: {(str(erinaSearchResponse.episode_duration) if erinaSearchResponse.episode_duration is not None else "??")}min
**Status**: {(str(erinaSearchResponse.status) if erinaSearchResponse.status is not None else "Unknown")}
**Genres**: {(str(create_nice_list(erinaSearchResponse.genres)))}
**Studio**: {(str([studio for studio in erinaSearchResponse.studios if studio.is_animation_studio]) if erinaSearchResponse.studios is not None else "Unknown")}

{(str(erinaSearchResponse.description) if len(str(erinaSearchResponse.description)) <= 200 else str(erinaSearchResponse.description)[:177] + "...")}
{(str(erinaSearchResponse.link) if erinaSearchResponse.link is not None else "")}
"""

def makeDescriptionResponse(erinaSearchResponse):
    """
    Makes the response for description queries on Discord
    """
    limit = 1020 - len(str(erinaSearchResponse.link))
    return str(erinaSearchResponse.title), str(erinaSearchResponse.cover_image), f"""{(str(erinaSearchResponse.description) if len(str(erinaSearchResponse.description)) <= limit else str(erinaSearchResponse.description)[:limit - 3] + "...")}
{(str(erinaSearchResponse.link) if erinaSearchResponse.link is not None else "")}
"""



def makeImageResponse(erinaSearchResponse):
    """
    Makes the response for image queries on Discord
    """
    errorTuple = (CachingError, DatabaseError, HashingError, ParserError, SearchingError)
    if isinstance(erinaSearchResponse, errorTuple) or isinstance(erinaSearchResponse.detectionResult, errorTuple) or isinstance(erinaSearchResponse.animeResult, errorTuple):
        return None, None, None
    else:
        discordResult = ""
        animeResult = erinaSearchResponse.animeResult
        detectionResult = erinaSearchResponse.detectionResult
        
        if animeResult is not None: # If it is an anime
            episode = "?"
            if isinstance(detectionResult, SauceNAOCache) and detectionResult.part is not None:
                episode = detectionResult.part
            elif detectionResult.episode is not None:
                episode = detectionResult.episode
            discordResult = f"""Here is the sauce!

**Anime**: {(str(animeResult.title) if animeResult.title is not None else "Unknown")}
**Episode**: {str(episode)}/{(str(animeResult.number_of_episodes) if animeResult.number_of_episodes is not None else "?")} {('(at around ' + str(detectionResult.timing) + ')') if detectionResult.timing is not None else ''})
**Studio**: {(str([studio for studio in animeResult.studios if studio.is_animation_studio]) if animeResult.studios is not None else "Unknown")}
**Genres**: {(str(create_nice_list(animeResult.genres))) if animeResult.genres is not None else "Unknown"}
**Similarity**: {(str(detectionResult.similarity)) if detectionResult.similarity is not None else "N/A"}%

{(str(animeResult.link)) if animeResult.link is not None else ""}
{(str(animeResult.description)) if animeResult.description is not None else ""}
"""
        elif isinstance(detectionResult, SauceNAOCache): # if it comes from SauceNAO
            if detectionResult.is_manga: # if it is a manga
                discordResult = f"""Here is the sauce!

**Manga**: {(str(detectionResult.title)) if detectionResult.title is not None else "Unknown"}
**Author**: {(str(detectionResult.author)) if detectionResult.author is not None else "Unknown"}
**Chapter**: {(str(detectionResult.part)) if detectionResult.part is not None else "??"}
**Similarity**: {(str(detectionResult.similarity)) if detectionResult.similarity is not None else "N/A"}%

{(str(detectionResult.link)) if detectionResult.link is not None else ""}
"""
        else:
            discordResult = f"""
Here is the sauce!

**Title**: {(str(detectionResult.title)) if detectionResult.title is not None else "Unknown"}
**Author**: {(str(detectionResult.author)) if detectionResult.author is not None else "Unknown"}
**Database**: {(str(detectionResult.database)) if detectionResult.database is not None else "Unknown"}
**Similarity**: {(str(detectionResult.similarity)) if detectionResult.similarity is not None else "N/A"}%

{(str(detectionResult.link)) if detectionResult.link is not None else ""}
"""

        if len(discordResult) >= 1000:
            discordResult = discordResult[:997] + "..."
        return str(detectionResult.title), (str(animeResult.cover_image) if animeResult.cover_image is not None else None), discordResult
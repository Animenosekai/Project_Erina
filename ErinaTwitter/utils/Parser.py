"""
Anime Database Information Parser (for Twitter) for the Erina Project

@author: Anime no Sekai\n
Erina Project - 2020
"""
from ErinaParser.utils.utils import create_nice_list
from ErinaParser.utils.saucenao_parser import SauceNAOCache
from ErinaCaches.utils.Errors import CachingError
from ErinaDB.utils.Errors import DatabaseError
from ErinaHash.utils.Errors import HashingError
from ErinaParser.utils.Errors import ParserError
from ErinaSearch.utils.Errors import SearchingError

def makeTweet(erinaSearchResponse):
    """
    Formats ErinaSearch's response for Twitter
    """
    errorTuple = (CachingError, DatabaseError, HashingError, ParserError, SearchingError)
    if isinstance(erinaSearchResponse, errorTuple) or isinstance(erinaSearchResponse.detectionResult, errorTuple) or isinstance(erinaSearchResponse.animeResult, errorTuple):
        return None
    else:
        tweetResult = ""
        animeResult = erinaSearchResponse.animeResult
        detectionResult = erinaSearchResponse.detectionResult
        
        if animeResult is not None: # If it is an anime
            episode = "?"
            if isinstance(detectionResult, SauceNAOCache) and detectionResult.part is not None:
                episode = detectionResult.part
            elif detectionResult.episode is not None:
                episode = detectionResult.episode
            tweetResult = """Here is the sauce!

Anime: {anime}
Episode: {episode}/{episodes} {timing}
Studio: {studios}
Genres: {genres}

{link}
{description}
""".format(
    anime=(str(animeResult.title) if animeResult.title is not None else "Unknown"),
    episode=str(episode),
    episodes=(str(animeResult.number_of_episodes) if animeResult.number_of_episodes is not None else "?"),
    timing=(('(at around ' + str(detectionResult.timing) + ')') if detectionResult.timing is not None else ''),
    studios=(str([studio for studio in animeResult.studios if studio.is_animation_studio]) if animeResult.studios is not None else "Unknown"),
    genres=((str(create_nice_list(animeResult.genres))) if animeResult.genres is not None else "Unknown"),
    link=((str(animeResult.link)) if animeResult.link is not None else ""),
    description=((str(animeResult.description)) if animeResult.description is not None else "")
)
        elif isinstance(detectionResult, SauceNAOCache): # if it comes from SauceNAO
            if detectionResult.is_manga: # if it is a manga
                tweetResult = """Here is the sauce!

**Manga**: {manga}
**Author**: {author}
**Chapter**: {chapter}
**Similarity**: {similarity}%

{link}
""".format(
    manga=((str(detectionResult.title)) if detectionResult.title is not None else "Unknown"),
    author=((str(detectionResult.author)) if detectionResult.author is not None else "Unknown"),
    chapter=((str(detectionResult.part)) if detectionResult.part is not None else "??"),
    similarity=((str(detectionResult.similarity)) if detectionResult.similarity is not None else "N/A"),
    link=((str(detectionResult.link)) if detectionResult.link is not None else "")
)
        else:
            tweetResult = """Here is the sauce!

**Title**: {title}
**Author**: {author}
**Database**: {database}
**Similarity**: {similarity}%

{link}
""".format(
    title=((str(detectionResult.title)) if detectionResult.title is not None else "Unknown"),
    author=((str(detectionResult.author)) if detectionResult.author is not None else "Unknown"),
    database=((str(detectionResult.database)) if detectionResult.database is not None else "Unknown"),
    similarity=((str(detectionResult.similarity)) if detectionResult.similarity is not None else "N/A"),
    link=((str(detectionResult.link)) if detectionResult.link is not None else "")
)

        if len(tweetResult) >= 280:
            tweetResult = tweetResult[:277] + "..."
        return tweetResult
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
            tweetResult = f"""
Here is the sauce!

Anime: {(str(animeResult.title) if animeResult.title is not None else "Unknown")}
Episode: {str(episode)}/{(str(animeResult.number_of_episodes) if animeResult.number_of_episodes is not None else "?")} {('(at around ' + str(detectionResult.timing) + ')') if detectionResult.timing is not None else ''})
Studio: {(str(create_nice_list(animeResult.studios)) if animeResult.studios is not None else "Unknown")}
Genres: {(str(animeResult.genres)) if animeResult.genres is not None else "Unknown"}

{(str(animeResult.link)) if animeResult.link is not None else ""}
{(str(animeResult.description)) if animeResult.description is not None else ""}
"""
        elif isinstance(detectionResult, SauceNAOCache): # if it comes from SauceNAO
            if detectionResult.is_manga: # if it is a manga
                tweetResult = f"""
Here is the sauce!

Manga: {(str(detectionResult.title)) if detectionResult.title is not None else "Unknown"}
Author: {(str(detectionResult.author)) if detectionResult.author is not None else "Unknown"}
Chapter: {(str(detectionResult.part)) if detectionResult.part is not None else "??"}
Similarity: {(str(detectionResult.similarity)) if detectionResult.similarity is not None else "N/A"}%

{(str(detectionResult.link)) if detectionResult.link is not None else ""}
"""
        else:
            tweetResult = f"""
Here is the sauce!

Title: {(str(detectionResult.title)) if detectionResult.title is not None else "Unknown"}
Author: {(str(detectionResult.author)) if detectionResult.author is not None else "Unknown"}
Database: {(str(detectionResult.database)) if detectionResult.database is not None else "Unknown"}
Similarity: {(str(detectionResult.similarity)) if detectionResult.similarity is not None else "N/A"}%

{(str(detectionResult.link)) if detectionResult.link is not None else ""}
"""

        if len(tweetResult) >= 280:
            tweetResult = tweetResult[:277] + "..."
        return tweetResult
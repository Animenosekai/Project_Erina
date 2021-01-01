"""
Parses ErinaSearch for Line
"""
from Erina.Errors import isAnError
from Erina.utils import create_nice_list
from ErinaParser.utils.saucenao_parser import SauceNAOCache

def makeInfoResponse(erinaSearchResponse):
    """
    Makes the response for info queries on Line
    """
    if isAnError(erinaSearchResponse):
        return "Sorry an error occured while searching for your anime"
    return """Anime: {anime}
Season: {season}{year}
Number of episodes: {episodes}
Average Duration: {duration}min
Status: {status}
Genres: {genres}
Studio: {studios}

{description}
{link}
""".format(
    anime=(str(erinaSearchResponse.title) if erinaSearchResponse.title is not None else "Unknown"),
    season=(str(erinaSearchResponse.season) if erinaSearchResponse.season is not None else (str(erinaSearchResponse.year) if erinaSearchResponse.year is not None else "N/A")),
    year=(("of " + str(erinaSearchResponse.year) if erinaSearchResponse.year is not None else "") if erinaSearchResponse.season is None else ""),
    episodes=(str(erinaSearchResponse.number_of_episodes) if erinaSearchResponse.number_of_episodes is not None else "??"),
    duration=(str(erinaSearchResponse.episode_duration) if erinaSearchResponse.episode_duration is not None else "??"),
    status=(str(erinaSearchResponse.status) if erinaSearchResponse.status is not None else "Unknown"),
    genres=(str(erinaSearchResponse.genres)),
    studios=(create_nice_list([studio for studio in erinaSearchResponse.studios if studio.is_animation_studio]) if erinaSearchResponse.studios is not None else "Unknown"),
    description=(str(erinaSearchResponse.description) if len(str(erinaSearchResponse.description)) <= 200 else str(erinaSearchResponse.description)[:177] + "..."),
    link=(str(erinaSearchResponse.link) if erinaSearchResponse.link is not None else "")
)

def makeDescriptionResponse(erinaSearchResponse):
    """
    Makes the response for description queries on Line
    """
    if isAnError(erinaSearchResponse):
        return "Sorry an error occured while searching for your anime"
    limit = 1020 - len(str(erinaSearchResponse.link))
    return """{description}
{link}
""".format(
    description=(str(erinaSearchResponse.description) if len(str(erinaSearchResponse.description)) <= limit else str(erinaSearchResponse.description)[:limit - 3] + "..."),
    link=(str(erinaSearchResponse.link) if erinaSearchResponse.link is not None else "")
)



def makeImageResponse(erinaSearchResponse):
    """
    Makes the response for image queries on Line
    """
    if isAnError(erinaSearchResponse) or isAnError(erinaSearchResponse.detectionResult) or isAnError(erinaSearchResponse.animeResult):
        return "Sorry an error occured while searching for your anime"
    else:
        lineResult = ""
        if erinaSearchResponse.low_similarity:
            lineResult = "⚠️The similarity seems low\n"
        animeResult = erinaSearchResponse.animeResult
        detectionResult = erinaSearchResponse.detectionResult
        
        if animeResult is not None: # If it is an anime
            episode = "?"
            if isinstance(detectionResult, SauceNAOCache) and detectionResult.part is not None:
                episode = detectionResult.part
            elif detectionResult.episode is not None:
                episode = detectionResult.episode
            lineResult = """Here is the sauce!

Anime: {anime}
Episode: {episode}/{episodes} {timestamp}
Studio: {studios}
Genres: {genres}
Similarity: {similarity}%

{link}
{description}
""".format(
    anime=(str(animeResult.title) if animeResult.title is not None else "Unknown"),
    episode=str(episode),
    episodes=(str(animeResult.number_of_episodes) if animeResult.number_of_episodes is not None else "?"),
    timestamp=(('(at around ' + str(detectionResult.timing) + ')') if detectionResult.timing is not None else ''),
    studios=(create_nice_list([studio for studio in animeResult.studios if studio.is_animation_studio]) if animeResult.studios is not None else "Unknown"),
    genres=((str(animeResult.genres)) if animeResult.genres is not None else "Unknown"),
    similarity=((str(detectionResult.similarity)) if detectionResult.similarity is not None else "N/A"),
    link=((str(animeResult.link)) if animeResult.link is not None else ""),
    description=((str(animeResult.description)) if animeResult.description is not None else "")
)
        elif isinstance(detectionResult, SauceNAOCache): # if it comes from SauceNAO
            if detectionResult.is_manga: # if it is a manga
                lineResult = """Here is the sauce!

Manga: {manga}
Author: {author}
Chapter: {chapter}
Similarity: {similarity}%

{link}
""".format(
    manga=((str(detectionResult.title)) if detectionResult.title is not None else "Unknown"),
    author=((str(detectionResult.author)) if detectionResult.author is not None else "Unknown"),
    chapter=((str(detectionResult.part)) if detectionResult.part is not None else "??"),
    similarity=((str(detectionResult.similarity)) if detectionResult.similarity is not None else "N/A"),
    link=((str(detectionResult.link)) if detectionResult.link is not None else "")
)
        else:
            lineResult = """Here is the sauce!

Title: {title}
Author: {author}
Database: {database}
Similarity: {similarity}%

{link}
""".format(
    title=((str(detectionResult.title)) if detectionResult.title is not None else "Unknown"),
    author=((str(detectionResult.author)) if detectionResult.author is not None else "Unknown"),
    database=((str(detectionResult.database)) if detectionResult.database is not None else "Unknown"),
    similarity=((str(detectionResult.similarity)) if detectionResult.similarity is not None else "N/A"),
    link=((str(detectionResult.link)) if detectionResult.link is not None else "")
)

        if len(lineResult) >= 1000:
            lineResult = lineResult[:997] + "..."
        return lineResult
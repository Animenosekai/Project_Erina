import traceback
from time import time
from os.path import isfile
from datetime import datetime

from safeIO import TextFile
from filecenter import extension_from_base, files_in_dir

from Erina import erina_stats
from Erina import env_information
from Erina.env_information import erina_dir
from ErinaParser.utils.anilist_parser import AnilistCache
from Erina.utils import convert_to_int, convert_to_float


def returnTimestamp(logLine):
    try:
        return datetime.fromtimestamp(float(logLine.split("    ")[0]))
    except:
        return None

def returnStats():
    results = {}

    ### BLOCKING EACH FILE AND GETTING ITS CONTENT
    erina_stats.api.searchEndpointCall.blocking = True
    api_searchEndpointCall = erina_stats.api.searchEndpointCall.readlines()
    erina_stats.api.searchEndpointCall.blocking = False
    erina_stats.db.erinaDatabaseLookups.blocking = True
    db_erinaDatabaseLookups = erina_stats.db.erinaDatabaseLookups.readlines()
    erina_stats.db.erinaDatabaseLookups.blocking = False
    erina_stats.db.manamiDBTitleVectorLookups.blocking = True
    db_manamiDBTitleVectorLookups = erina_stats.db.manamiDBTitleVectorLookups.readlines()
    erina_stats.db.manamiDBTitleVectorLookups.blocking = False
    erina_stats.discord.descriptionHit.blocking = True
    discord_descriptionHit = erina_stats.discord.descriptionHit.readlines()
    erina_stats.discord.descriptionHit.blocking = False
    erina_stats.discord.imageSearchHit.blocking = True
    discord_imageSearchHit = erina_stats.discord.imageSearchHit.readlines()
    erina_stats.discord.imageSearchHit.blocking = False
    erina_stats.discord.infoHit.blocking = True
    discord_infoHit = erina_stats.discord.infoHit.readlines()
    erina_stats.discord.infoHit.blocking = False
    erina_stats.erinahash.createdBase64String.blocking = True
    erinahash_createdBase64String = erina_stats.erinahash.createdBase64String.readlines()
    erina_stats.erinahash.createdBase64String.blocking = False
    erina_stats.erinahash.createdHashes.blocking = True
    erinahash_createdHashes = erina_stats.erinahash.createdHashes.readlines()
    erina_stats.erinahash.createdHashes.blocking = False
    erina_stats.erina.cacheFilesCount.blocking = True
    erina_cacheFilesCount = erina_stats.erina.cacheFilesCount.readlines()
    erina_stats.erina.cacheFilesCount.blocking = False
    erina_stats.erina.erinaParsingCount.blocking = True
    erina_erinaParsingCount = erina_stats.erina.erinaParsingCount.readlines()
    erina_stats.erina.erinaParsingCount.blocking = False
    erina_stats.erina.errorsCount.blocking = True
    erina_errorsCount = erina_stats.erina.errorsCount.readlines()
    erina_stats.erina.errorsCount.blocking = False
    erina_stats.external.anilistAPICalls.blocking = True
    external_anilistAPICalls = erina_stats.external.anilistAPICalls.readlines()
    erina_stats.external.anilistAPICalls.blocking = False
    erina_stats.external.iqdbCalls.blocking = True
    external_iqdbCalls = erina_stats.external.iqdbCalls.readlines()
    erina_stats.external.iqdbCalls.blocking = False
    erina_stats.external.saucenaoAPICalls.blocking = True
    external_saucenaoAPICalls = erina_stats.external.saucenaoAPICalls.readlines()
    erina_stats.external.saucenaoAPICalls.blocking = False
    erina_stats.external.tracemoeAPICalls.blocking = True
    external_tracemoeAPICalls = erina_stats.external.tracemoeAPICalls.readlines()
    erina_stats.external.tracemoeAPICalls.blocking = False
    erina_stats.line.descriptionHit.blocking = True
    line_descriptionHit = erina_stats.line.descriptionHit.readlines()
    erina_stats.line.descriptionHit.blocking = False
    erina_stats.line.imageSearchHit.blocking = True
    line_imageSearchHit = erina_stats.line.imageSearchHit.readlines()
    erina_stats.line.imageSearchHit.blocking = False
    erina_stats.line.infoHit.blocking = True
    line_infoHit = erina_stats.line.infoHit.readlines()
    erina_stats.line.infoHit.blocking = False
    erina_stats.line.storedImages.blocking = True
    line_storedImages = erina_stats.line.storedImages.readlines()
    erina_stats.line.storedImages.blocking = False
    erina_stats.search.anilistIDSearchCount.blocking = True
    search_anilistIDSearchCount = erina_stats.search.anilistIDSearchCount.readlines()
    erina_stats.search.anilistIDSearchCount.blocking = False
    erina_stats.search.imageSearchCount.blocking = True
    search_imageSearchCount = erina_stats.search.imageSearchCount.readlines()
    erina_stats.search.imageSearchCount.blocking = False
    erina_stats.search.titleSearchCount.blocking = True
    search_titleSearchCount = erina_stats.search.titleSearchCount.readlines()
    erina_stats.search.titleSearchCount.blocking = False
    erina_stats.twitter.askingHit.blocking = True
    twitter_askingHit = erina_stats.twitter.askingHit.readlines()
    erina_stats.twitter.askingHit.blocking = False
    erina_stats.twitter.directMessagingHit.blocking = True
    twitter_directMessagingHit = erina_stats.twitter.directMessagingHit.readlines()
    erina_stats.twitter.directMessagingHit.blocking = False
    erina_stats.twitter.responsePolarity.blocking = True
    twitter_responsePolarity = erina_stats.twitter.responsePolarity.readlines()
    erina_stats.twitter.responsePolarity.blocking = False
    erina_stats.twitter.responses.blocking = True
    twitter_responses = erina_stats.twitter.responses.readlines()
    erina_stats.twitter.responses.blocking = False
    erina_stats.twitter.streamHit.blocking = True
    twitter_streamHit = erina_stats.twitter.streamHit.readlines()
    erina_stats.twitter.streamHit.blocking = False
    
    results["search"] = {}
    results["search"]["searchCount"] = {}
    results["search"]["searchCount"]["values"] = {}
    results["search"]["searchCount"]["success"] = True

    def _retrieveStats(category, subcategory, data):
        
        currentTime = datetime.fromtimestamp(time())

        # INIT RESULTS FOR THE CATEGORY
        if category not in results:
            results[category] = {}

        if subcategory not in results[category]:
            results[category][subcategory] = {}

        results[category][subcategory]["success"] = False
        results[category][subcategory]["values"] = {}

        if data is not None and len(data) > 0: # IF THERE IS DATA

            #### ADDING A VALUE
            def addValue(timestamp, data=None):
                """
                Adds a value to the results
                """
                timestamp = timestamp.timestamp()
                if data is None:
                    if timestamp in results[category][subcategory]["values"]:
                        results[category][subcategory]["values"][timestamp] += 1
                    else:
                        results[category][subcategory]["values"][timestamp] = 1
                    
                    if category == "search" and subcategory in ["anilistIDSearchCount", "titleSearchCount", "imageSearchCount"]:
                        if timestamp in results["search"]["searchCount"]["values"]:
                            results["search"]["searchCount"]["values"][timestamp] += 1
                        else:
                            results["search"]["searchCount"]["values"][timestamp] = 1

                elif subcategory in ["manamiDBTitleVectorLookups", "erinaDatabaseLookups"]:
                    if timestamp in results[category][subcategory]["values"]:
                        results[category][subcategory]["values"][timestamp] += convert_to_int(element.split("    ")[1])
                    else:
                        results[category][subcategory]["values"][timestamp] = convert_to_int(element.split("    ")[1])
                elif subcategory == "cacheFilesCount":
                    results[category][subcategory]["values"][timestamp] = convert_to_int(element.split("    ")[1])
                elif subcategory == "responsePolarity":
                    if timestamp in results[category][subcategory]["values"]:
                        results[category][subcategory]["values"][timestamp].append(convert_to_float(element.split("    ")[1]))
                    else:
                        results[category][subcategory]["values"][timestamp] = [convert_to_float(element.split("    ")[1])]


            firstElementTimestamp = returnTimestamp(data[0])
            if firstElementTimestamp is not None:
                results[category][subcategory]["success"] = True
                if firstElementTimestamp.month == currentTime.month:
                    if firstElementTimestamp.day == currentTime.day:
                        if firstElementTimestamp.hour == currentTime.hour:
                            if firstElementTimestamp.minute == currentTime.minute:
                                for element in data:
                                    try:
                                        currentTimestamp = returnTimestamp(element).replace(microsecond=0)
                                        if subcategory in ["manamiDBTitleVectorLookups", "erinaDatabaseLookups", "responsePolarity", "storedImages", "cacheFilesCount"]:
                                            addValue(currentTimestamp, element)
                                        else:    
                                            addValue(currentTimestamp)
                                    except:
                                        pass
                            else:
                                for element in data:
                                    try:
                                        currentTimestamp = returnTimestamp(element).replace(microsecond=0, second=0)
                                        if subcategory in ["manamiDBTitleVectorLookups", "erinaDatabaseLookups", "responsePolarity", "storedImages", "cacheFilesCount"]:
                                            addValue(currentTimestamp, element)
                                        else:    
                                            addValue(currentTimestamp)
                                    except:
                                        pass
                        else:
                            for element in data:
                                try:
                                    currentTimestamp = returnTimestamp(element).replace(microsecond=0, second=0, minute=0)
                                    if subcategory in ["manamiDBTitleVectorLookups", "erinaDatabaseLookups", "responsePolarity", "storedImages", "cacheFilesCount"]:
                                        addValue(currentTimestamp, element)
                                    else:    
                                        addValue(currentTimestamp)
                                except:
                                    pass
                    else:
                        for element in data:
                            try:
                                currentTimestamp = returnTimestamp(element).replace(microsecond=0, second=0, minute=0, hour=0)
                                if subcategory in ["manamiDBTitleVectorLookups", "erinaDatabaseLookups", "responsePolarity", "storedImages", "cacheFilesCount"]:
                                    addValue(currentTimestamp, element)
                                else:    
                                    addValue(currentTimestamp)
                            except:
                                pass
                else:
                    for element in data:
                        try:
                            currentTimestamp = returnTimestamp(element).replace(microsecond=0, second=0, minute=0, hour=0, day=1)
                            if subcategory in ["manamiDBTitleVectorLookups", "erinaDatabaseLookups", "responsePolarity", "storedImages", "cacheFilesCount"]:
                                addValue(currentTimestamp, element)
                            else:    
                                addValue(currentTimestamp)
                        except:
                            pass
            else:
                results[category][subcategory]["success"] = False
                return False

        else:
            results[category][subcategory]["values"] = {}
            for i in range(10):
                results[category][subcategory]["values"][currentTime.replace(microsecond=0, second=0, minute=0).timestamp() - (86400 * i)] = 0
            results[category][subcategory]["success"] = True
            return False

        return True

    _retrieveStats('api', 'searchEndpointCall', api_searchEndpointCall)
    _retrieveStats('db', 'erinaDatabaseLookups', db_erinaDatabaseLookups)
    _retrieveStats('db', 'manamiDBTitleVectorLookups', db_manamiDBTitleVectorLookups)
    _retrieveStats('discord', 'descriptionHit', discord_descriptionHit)
    _retrieveStats('discord', 'imageSearchHit', discord_imageSearchHit)
    _retrieveStats('discord', 'infoHit', discord_infoHit)
    _retrieveStats('erinahash', 'createdBase64String', erinahash_createdBase64String)
    _retrieveStats('erinahash', 'createdHashes', erinahash_createdHashes)
    _retrieveStats('erina', 'cacheFilesCount', erina_cacheFilesCount)
    _retrieveStats('erina', 'erinaParsingCount', erina_erinaParsingCount)
    _retrieveStats('erina', 'errorsCount', erina_errorsCount)
    _retrieveStats('external', 'anilistAPICalls', external_anilistAPICalls)
    _retrieveStats('external', 'iqdbCalls', external_iqdbCalls)
    _retrieveStats('external', 'saucenaoAPICalls', external_saucenaoAPICalls)
    _retrieveStats('external', 'tracemoeAPICalls', external_tracemoeAPICalls)
    _retrieveStats('line', 'descriptionHit', line_descriptionHit)
    _retrieveStats('line', 'imageSearchHit', line_imageSearchHit)
    _retrieveStats('line', 'infoHit', line_infoHit)
    _retrieveStats('line', 'storedImages', line_storedImages)
    _retrieveStats('search', 'anilistIDSearchCount', search_anilistIDSearchCount)
    _retrieveStats('search', 'imageSearchCount', search_imageSearchCount)
    _retrieveStats('search', 'titleSearchCount', search_titleSearchCount)
    _retrieveStats('twitter', 'askingHit', twitter_askingHit)
    _retrieveStats('twitter', 'directMessagingHit', twitter_directMessagingHit)
    _retrieveStats('twitter', 'responses', twitter_responses)
    _retrieveStats('twitter', 'streamHit', twitter_streamHit)
    polarityHasValue = _retrieveStats('twitter', 'responsePolarity', twitter_responsePolarity)
    if polarityHasValue:
        for key in results["twitter"]["responsePolarity"]["values"]:
            currentState = results["twitter"]["responsePolarity"]["values"][key]
            results["twitter"]["responsePolarity"]["values"][key] = sum(currentState) / len(currentState)
    
    animeSearchStats = {}
    for line in search_titleSearchCount:
        currentAnime = str(line.split("    ")[1]).replace("\n", "").capitalize()
        if currentAnime in animeSearchStats:
            animeSearchStats[currentAnime] += 1
        else:
            animeSearchStats[currentAnime] = 1
    
    for line in search_anilistIDSearchCount:
        currentAnime = str(line.split("    ")[1])
        if isfile(erina_dir + "/ErinaCaches/AniList_Cache/" + currentAnime + ".erina"):
            currentAnime = str(AnilistCache(TextFile(erina_dir + "/ErinaCaches/AniList_Cache/" + currentAnime + ".erina").read()).title)
            if currentAnime in animeSearchStats:
                animeSearchStats[currentAnime] += 1
            else:
                animeSearchStats[currentAnime] = 1

    animeSearchRank = []

    for anime in sorted(animeSearchStats, key=animeSearchStats.get, reverse=True):
        animeSearchRank.append({anime: animeSearchStats[anime]})

    results["animeSearchRank"] = animeSearchRank


    searchCountKeys = sorted(results["search"]["searchCount"]["values"].keys())
    finalSearchCountResult = {}
    for timestamp in searchCountKeys:
        finalSearchCountResult[timestamp] = results["search"]["searchCount"]["values"][timestamp]

    results["search"]["searchCount"]["values"] = finalSearchCountResult

    results["uptime"] = env_information.startTime


    #### User Defined Endpoints
    for file in files_in_dir(erina_dir + "/Erina/stats/userdefinedStats"):
        if extension_from_base(file) == ".erinalog":
            data = TextFile(erina_dir + "/Erina/stats/userdefinedStats/" + file).readlines()
            _retrieveStats("userDefinedEndpoints", file[:-9], data)

    return results


def returnOverviewStats():
    results = {}

    ### BLOCKING EACH FILE AND GETTING ITS CONTENT
    
    erina_stats.search.anilistIDSearchCount.blocking = True
    search_anilistIDSearchCount = erina_stats.search.anilistIDSearchCount.readlines()
    erina_stats.search.anilistIDSearchCount.blocking = False
    erina_stats.search.imageSearchCount.blocking = True
    search_imageSearchCount = erina_stats.search.imageSearchCount.readlines()
    erina_stats.search.imageSearchCount.blocking = False
    erina_stats.search.titleSearchCount.blocking = True
    search_titleSearchCount = erina_stats.search.titleSearchCount.readlines()
    erina_stats.search.titleSearchCount.blocking = False
    
    erina_stats.twitter.responses.blocking = True
    twitter_responses = erina_stats.twitter.responses.readlines()
    erina_stats.twitter.responses.blocking = False
    
    results["search"] = {}
    results["search"]["searchCount"] = {}
    results["search"]["searchCount"]["values"] = {}
    results["search"]["searchCount"]["success"] = True

    def _retrieveStats(category, subcategory, data):
        
        currentTime = datetime.fromtimestamp(time())

        # INIT RESULTS FOR THE CATEGORY
        if category not in results:
            results[category] = {}

        if subcategory not in results[category]:
            results[category][subcategory] = {}

        results[category][subcategory]["success"] = False
        results[category][subcategory]["values"] = {}

        if data is not None and len(data) > 0: # IF THERE IS DATA

            #### ADDING A VALUE
            def addValue(timestamp, data=None):
                """
                Adds a value to the results
                """
                timestamp = timestamp.timestamp()
                if data is None:
                    if timestamp in results[category][subcategory]["values"]:
                        results[category][subcategory]["values"][timestamp] += 1
                    else:
                        results[category][subcategory]["values"][timestamp] = 1
                    
                    if category == "search" and subcategory in ["anilistIDSearchCount", "titleSearchCount", "imageSearchCount"]:
                        if timestamp in results["search"]["searchCount"]["values"]:
                            results["search"]["searchCount"]["values"][timestamp] += 1
                        else:
                            results["search"]["searchCount"]["values"][timestamp] = 1

                elif subcategory in ["manamiDBTitleVectorLookups", "erinaDatabaseLookups"]:
                    if timestamp in results[category][subcategory]["values"]:
                        results[category][subcategory]["values"][timestamp] += convert_to_int(element.split("    ")[1])
                    else:
                        results[category][subcategory]["values"][timestamp] = convert_to_int(element.split("    ")[1])
                elif subcategory == "cacheFilesCount":
                    results[category][subcategory]["values"][timestamp] = convert_to_int(element.split("    ")[1])
                elif subcategory == "responsePolarity":
                    if timestamp in results[category][subcategory]["values"]:
                        results[category][subcategory]["values"][timestamp].append(convert_to_float(element.split("    ")[1]))
                    else:
                        results[category][subcategory]["values"][timestamp] = [convert_to_float(element.split("    ")[1])]

            firstElementTimestamp = returnTimestamp(data[0])
            if firstElementTimestamp is not None:
                results[category][subcategory]["success"] = True
                if firstElementTimestamp.month == currentTime.month:
                    if firstElementTimestamp.day == currentTime.day:
                        if firstElementTimestamp.hour == currentTime.hour:
                            if firstElementTimestamp.minute == currentTime.minute:
                                for element in data:
                                    currentTimestamp = returnTimestamp(element).replace(microsecond=0)
                                    if subcategory in ["manamiDBTitleVectorLookups", "erinaDatabaseLookups", "responsePolarity", "storedImages", "cacheFilesCount"]:
                                        addValue(currentTimestamp, element)
                                    else:    
                                        addValue(currentTimestamp)
                            else:
                                for element in data:
                                    currentTimestamp = returnTimestamp(element).replace(microsecond=0, second=0)
                                    if subcategory in ["manamiDBTitleVectorLookups", "erinaDatabaseLookups", "responsePolarity", "storedImages", "cacheFilesCount"]:
                                        addValue(currentTimestamp, element)
                                    else:    
                                        addValue(currentTimestamp)
                        else:
                            for element in data:
                                currentTimestamp = returnTimestamp(element).replace(microsecond=0, second=0, minute=0)
                                if subcategory in ["manamiDBTitleVectorLookups", "erinaDatabaseLookups", "responsePolarity", "storedImages", "cacheFilesCount"]:
                                    addValue(currentTimestamp, element)
                                else:    
                                    addValue(currentTimestamp)
                    else:
                        for element in data:
                            currentTimestamp = returnTimestamp(element).replace(microsecond=0, second=0, minute=0, hour=0)
                            if subcategory in ["manamiDBTitleVectorLookups", "erinaDatabaseLookups", "responsePolarity", "storedImages", "cacheFilesCount"]:
                                addValue(currentTimestamp, element)
                            else:    
                                addValue(currentTimestamp)
                else:
                    for element in data:
                        currentTimestamp = returnTimestamp(element).replace(microsecond=0, second=0, minute=0, hour=0, day=0)
                        if subcategory in ["manamiDBTitleVectorLookups", "erinaDatabaseLookups", "responsePolarity", "storedImages", "cacheFilesCount"]:
                            addValue(currentTimestamp, element)
                        else:    
                            addValue(currentTimestamp)
            else:
                results[category][subcategory]["success"] = False
                return False

        else:
            results[category][subcategory]["values"] = {}
            for i in range(10):
                results[category][subcategory]["values"][currentTime.replace(microsecond=0, second=0, minute=0).timestamp() - (86400 * i)] = 0
            results[category][subcategory]["success"] = True
            return False

        return True


    _retrieveStats('search', 'anilistIDSearchCount', search_anilistIDSearchCount)
    _retrieveStats('search', 'imageSearchCount', search_imageSearchCount)
    _retrieveStats('search', 'titleSearchCount', search_titleSearchCount)
    _retrieveStats('twitter', 'responses', twitter_responses)
    
    animeSearchStats = {}
    for line in search_titleSearchCount:
        currentAnime = str(line.split("    ")[1]).replace("\n", "").capitalize()
        if currentAnime in animeSearchStats:
            animeSearchStats[currentAnime] += 1
        else:
            animeSearchStats[currentAnime] = 1
    
    for line in search_anilistIDSearchCount:
        currentAnime = str(line.split("    ")[1])
        if isfile(erina_dir + "/ErinaCaches/AniList_Cache/" + currentAnime + ".erina"):
            currentAnime = str(AnilistCache(TextFile(erina_dir + "/ErinaCaches/AniList_Cache/" + currentAnime + ".erina").read()).title)
            if currentAnime in animeSearchStats:
                animeSearchStats[currentAnime] += 1
            else:
                animeSearchStats[currentAnime] = 1

    animeSearchRank = []

    for anime in sorted(animeSearchStats, key=animeSearchStats.get, reverse=True):
        animeSearchRank.append({anime: animeSearchStats[anime]})

    results["animeSearchRank"] = animeSearchRank


    searchCountKeys = sorted(results["search"]["searchCount"]["values"].keys())
    finalSearchCountResult = {}
    for timestamp in searchCountKeys:
        finalSearchCountResult[timestamp] = results["search"]["searchCount"]["values"][timestamp]

    results["search"]["searchCount"]["values"] = finalSearchCountResult

    return results



def pastMonthErrors():
    erina_stats.erina.errorsCount.blocking = True
    errorsCount = erina_stats.erina.errorsCount.readlines()
    erina_stats.erina.errorsCount.blocking = False
    
    currentTime = time()
    
    results = []
    for error in errorsCount:
        error = error.replace("\n", "")
        errorTimestamp = returnTimestamp(error).timestamp()
        if errorTimestamp - currentTime <= 2600000:
            results.append({errorTimestamp: error.split("    ")[1]})
    return results


def biggestUsers():
    
    erina_stats.discord.descriptionHit.blocking = True
    discord_descriptionHit = erina_stats.discord.descriptionHit.readlines()
    if discord_descriptionHit is None:
        erina_stats.discord.descriptionHit.blocking = True
        discord_descriptionHit = erina_stats.discord.descriptionHit.readlines()
        if discord_descriptionHit is None:
            erina_stats.discord.descriptionHit.blocking = True
            discord_descriptionHit = erina_stats.discord.descriptionHit.readlines()    
    erina_stats.discord.descriptionHit.blocking = False
    erina_stats.discord.descriptionHit.blocking = False
    erina_stats.discord.descriptionHit.blocking = False

    erina_stats.discord.imageSearchHit.blocking = True
    discord_imageSearchHit = erina_stats.discord.imageSearchHit.readlines()
    if discord_imageSearchHit is None:
        erina_stats.discord.imageSearchHit.blocking = True
        discord_imageSearchHit = erina_stats.discord.imageSearchHit.readlines()
        if discord_imageSearchHit is None:
            erina_stats.discord.imageSearchHit.blocking = True
            discord_imageSearchHit = erina_stats.discord.imageSearchHit.readlines()
    erina_stats.discord.imageSearchHit.blocking = False
    erina_stats.discord.imageSearchHit.blocking = False
    erina_stats.discord.imageSearchHit.blocking = False
    
    erina_stats.discord.infoHit.blocking = True
    discord_infoHit = erina_stats.discord.infoHit.readlines()
    if discord_infoHit is None:
        erina_stats.discord.infoHit.blocking = True
        discord_infoHit = erina_stats.discord.infoHit.readlines()
        if discord_infoHit is None:
            erina_stats.discord.infoHit.blocking = True
            discord_infoHit = erina_stats.discord.infoHit.readlines()
    erina_stats.discord.infoHit.blocking = False
    erina_stats.discord.infoHit.blocking = False
    erina_stats.discord.infoHit.blocking = False

    erina_stats.line.descriptionHit.blocking = True
    line_descriptionHit = erina_stats.line.descriptionHit.readlines()
    if line_descriptionHit is None:
        erina_stats.line.descriptionHit.blocking = True
        line_descriptionHit = erina_stats.line.descriptionHit.readlines()
        if line_descriptionHit is None:
            erina_stats.line.descriptionHit.blocking = True
            line_descriptionHit = erina_stats.line.descriptionHit.readlines()
    erina_stats.line.descriptionHit.blocking = False
    erina_stats.line.descriptionHit.blocking = False
    erina_stats.line.descriptionHit.blocking = False

    erina_stats.line.imageSearchHit.blocking = True
    line_imageSearchHit = erina_stats.line.imageSearchHit.readlines()
    if line_imageSearchHit is None:
        erina_stats.line.imageSearchHit.blocking = True
        line_imageSearchHit = erina_stats.line.imageSearchHit.readlines()
        if line_imageSearchHit is None:
            erina_stats.line.imageSearchHit.blocking = True
            line_imageSearchHit = erina_stats.line.imageSearchHit.readlines()
    erina_stats.line.imageSearchHit.blocking = False
    erina_stats.line.imageSearchHit.blocking = False
    erina_stats.line.imageSearchHit.blocking = False

    erina_stats.line.infoHit.blocking = True
    line_infoHit = erina_stats.line.infoHit.readlines()
    if line_infoHit is None:
        erina_stats.line.infoHit.blocking = True
        line_infoHit = erina_stats.line.infoHit.readlines()
        if line_infoHit is None:
            erina_stats.line.infoHit.blocking = True
            line_infoHit = erina_stats.line.infoHit.readlines()
    erina_stats.line.infoHit.blocking = False
    erina_stats.line.infoHit.blocking = False
    erina_stats.line.infoHit.blocking = False

    erina_stats.twitter.askingHit.blocking = True
    twitter_askingHit = erina_stats.twitter.askingHit.readlines()
    if twitter_askingHit is None:
        erina_stats.twitter.askingHit.blocking = True
        twitter_askingHit = erina_stats.twitter.askingHit.readlines()
        if twitter_askingHit is None:
            erina_stats.twitter.askingHit.blocking = True
            twitter_askingHit = erina_stats.twitter.askingHit.readlines()
    erina_stats.twitter.askingHit.blocking = False
    erina_stats.twitter.askingHit.blocking = False
    erina_stats.twitter.askingHit.blocking = False
    
    erina_stats.twitter.directMessagingHit.blocking = True
    twitter_directMessagingHit = erina_stats.twitter.directMessagingHit.readlines()
    if twitter_directMessagingHit is None:
        erina_stats.twitter.directMessagingHit.blocking = True
        twitter_directMessagingHit = erina_stats.twitter.directMessagingHit.readlines()
        if twitter_directMessagingHit is None:
            erina_stats.twitter.directMessagingHit.blocking = True
            twitter_directMessagingHit = erina_stats.twitter.directMessagingHit.readlines()
    erina_stats.twitter.directMessagingHit.blocking = False
    erina_stats.twitter.directMessagingHit.blocking = False
    erina_stats.twitter.directMessagingHit.blocking = False

    results = {}
    ### DISCORD
    for line in discord_descriptionHit:
        user = line.replace("\n", "").split("    ")[1].split(" >>> ")[1]
        if user in results:
            results[user] += 1
        else:
            results[user] = 1
    
    for line in discord_infoHit:
        user = line.replace("\n", "").split("    ")[1].split(" >>> ")[1]
        if user in results:
            results[user] += 1
        else:
            results[user] = 1
    
    for line in discord_imageSearchHit:
        user = line.replace("\n", "").split("    ")[1]
        if user in results:
            results[user] += 1
        else:
            results[user] = 1
    
    ### LINE
    for line in line_descriptionHit:
        user = line.replace("\n", "").split("    ")[1].split(" >>> ")[1]
        if user in results:
            results[user] += 1
        else:
            results[user] = 1
    
    for line in line_infoHit:
        user = line.replace("\n", "").split("    ")[1].split(" >>> ")[1]
        if user in results:
            results[user] += 1
        else:
            results[user] = 1
    
    for line in line_imageSearchHit:
        user = line.replace("\n", "").split("    ")[1]
        if user in results:
            results[user] += 1
        else:
            results[user] = 1

    ### TWITTER    
    for line in twitter_askingHit:
        user = line.replace("\n", "").split("    ")[1]
        if user in results:
            results[user] += 1
        else:
            results[user] = 1

    for line in twitter_directMessagingHit:
        user = line.replace("\n", "").split("    ")[1]
        if user in results:
            results[user] += 1
        else:
            results[user] = 1

    rankingResults = []

    for user in sorted(results, key=results.get, reverse=True):
        rankingResults.append({user: results[user]})

    return rankingResults
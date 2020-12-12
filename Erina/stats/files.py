from safeIO import TextFile

from Erina.env_information import erina_dir

statsFilePath = erina_dir + "/Erina/stats/"


class apiStats():
    """
    API Stats Files
    """
    def __init__(self) -> None:
        self.path = statsFilePath + "apiStats/"
        self.searchEndpointCall = TextFile(self.path + "searchEndpointCall.erinalog", blocking=False)

class dbStats():
    """
    Database Stats Files
    """
    def __init__(self) -> None:
        self.path = statsFilePath + "dbStats/"
        self.erinaDatabaseLookups = TextFile(self.path + "erinaDatabaseLookups.erinalog", blocking=False)
        self.manamiDBTitleVectorLookups = TextFile(self.path + "manamiDBTitleVectorLookups.erinalog", blocking=False)

class discordStats():
    """
    Discord Stats Files
    """
    def __init__(self) -> None:
        self.path = statsFilePath + "discordStats/"
        self.descriptionHit = TextFile(self.path + "descriptionHit.erinalog", blocking=False)
        self.imageSearchHit = TextFile(self.path + "imageSearchHit.erinalog", blocking=False)
        self.infoHit = TextFile(self.path + "infoHit.erinalog", blocking=False)

class erinahashStats():
    """
    ErinaHash Stats Files
    """
    def __init__(self) -> None:
        self.path = statsFilePath + "erinahashStats/"
        self.createdBase64String = TextFile(self.path + "createdBase64String.erinalog", blocking=False)
        self.createdHashes = TextFile(self.path + "createdHashes.erinalog", blocking=False)

class erinaStats():
    """
    Erina Stats Files
    """
    def __init__(self) -> None:
        self.path = statsFilePath + "erinaStats/"
        self.cacheFilesCount = TextFile(self.path + "cacheFilesCount.erinalog", blocking=False)
        self.erinaParsingCount = TextFile(self.path + "erinaParsingCount.erinalog", blocking=False)
        self.errorsCount = TextFile(self.path + "errorsCount.erinalog", blocking=False)
        self.fileIOCounter = TextFile(self.path + "fileIOCounter.erinalog", blocking=False)

class externalStats():
    """
    External Stats Files
    """
    def __init__(self) -> None:
        self.path = statsFilePath + "externalStats/"
        self.anilistAPICalls = TextFile(self.path + "anilistAPICalls.erinalog", blocking=False)
        self.iqdbCalls = TextFile(self.path + "iqdbCalls.erinalog", blocking=False)
        self.saucenaoAPICalls = TextFile(self.path + "saucenaoAPICalls.erinalog", blocking=False)
        self.tracemoeAPICalls = TextFile(self.path + "tracemoeAPICalls.erinalog", blocking=False)
        

class lineStats():
    """
    Line Stats Files
    """
    def __init__(self) -> None:
        self.path = statsFilePath + "lineStats/"
        self.descriptionHit = TextFile(self.path + "descriptionHit.erinalog", blocking=False)
        self.imageSearchHit = TextFile(self.path + "imageSearchHit.erinalog", blocking=False)
        self.infoHit = TextFile(self.path + "infoHit.erinalog", blocking=False)
        self.storedImages = TextFile(self.path + "storedImages.erinalog", blocking=False)
        

class searchStats():
    """
    Search Stats Files
    """
    def __init__(self) -> None:
        self.path = statsFilePath + "searchStats/"
        self.searchCount = TextFile(self.path + "searchCount.erinalog", blocking=False)
        self.anilistIDSearchCount = TextFile(self.path + "anilistIDSearchCount.erinalog", blocking=False)
        self.imageSearchCount = TextFile(self.path + "imageSearchCount.erinalog", blocking=False)
        self.titleSearchCount = TextFile(self.path + "titleSearchCount.erinalog", blocking=False)
        
class twitterStats():
    """
    Twitter Stats Files
    """
    def __init__(self) -> None:
        self.path = statsFilePath + "twitterStats/"
        self.askingHit = TextFile(self.path + "askingHit.erinalog", blocking=False)
        self.directMessagingHit = TextFile(self.path + "directMessagingHit.erinalog", blocking=False)
        self.responsePolarity = TextFile(self.path + "responsePolarity.erinalog", blocking=False)
        self.responses = TextFile(self.path + "responses.erinalog", blocking=False)
        self.streamHit = TextFile(self.path + "streamHit.erinalog", blocking=False)
import random
import string

from safeIO import TextFile
import hashlib
from Erina.env_information import erina_dir
from filecenter import files_in_dir

currentSalt = None
currentToken = None
salts = []
expiredTokens = []
tempCode = None
class TokenVerification():
    def __init__(self, success=False, expired=False, wrong=False, no_token=False, not_set=False) -> None:
        self.success = success
        self.expired = expired
        self.wrong = wrong
        self.no_token = no_token

    def __repr__(self) -> str:
        if self.success:
            return "Success"
        elif self.expired:
            return "Expired Token"
        elif self.wrong:
            return "Wrong Token"
        elif self.no_token:
            return "No Token Provided"
        elif self.not_set:
            return "No Password Is Set"
        else:
            return "Error"

def createRandomID(length):
    idResult = ''
    for _ in range(length):
        choice = random.randint(0,1)
        if choice == 0:
            idResult += str(random.randint(0,9))
        else: 
            idResult += str(random.choice(string.ascii_letters))
    return idResult

if currentSalt is None:
    salts = TextFile(erina_dir + "/ErinaServer/Erina/auth/salt.erina").readlines()
    currentSalt = createRandomID(8)
    while currentSalt in salts:
        currentSalt = createRandomID(8)
    TextFile(erina_dir + "/ErinaServer/Erina/auth/salt.erina").append(currentSalt + "\n")
    lastTokenFile = TextFile(erina_dir + "/ErinaServer/Erina/auth/lastToken.erina")
    if lastTokenFile.read().replace(" ", "").replace("\n", "") != "":
        currentToken = lastTokenFile.read().replace(" ", "").replace("\n", "")
    lastTokenFile.write("")

def createToken(lengthWithoutSalt):
    global currentToken
    global expiredTokens
    lastTokenFile.write("")
    tokenResult = str(currentSalt) + createRandomID(lengthWithoutSalt)
    if tokenResult in expiredTokens:
        tokenResult = createToken(lengthWithoutSalt)
    expiredTokens.append(currentToken)
    currentToken = tokenResult
    return tokenResult

def createAPIKey():
    tokenResult = createRandomID(32)
    if tokenResult + ".erina" in files_in_dir(erina_dir + "/ErinaServer/Erina/auth/apiAuth"):
        tokenResult = createAPIKey()
    return tokenResult    

def verifyToken(args):
    """
    Verifies that the given token is equal to the one currently authorized
    """
    if "token" in args:
        token = args["token"]
        if token == currentToken:
            return TokenVerification(success=True)
        elif token in expiredTokens or token[:8] in salts:
            return TokenVerification(expired=True)
        else:
            return TokenVerification(wrong=True)
    else:
        return TokenVerification(no_token=True)

def createTempCode():
    global tempCode
    tempCode = createRandomID(8)
    return tempCode

def setPassword(password):
    hashing = hashlib.sha512()
    hashing.update(str(password).encode("utf-8"))
    TextFile(erina_dir + "/ErinaServer/Erina/auth/password.erina").write(hashing.hexdigest())

def verifyPassword(password):
    hashing = hashlib.sha512()
    hashing.update(str(password).encode("utf-8"))
    return TextFile(erina_dir + "/ErinaServer/Erina/auth/password.erina").read().replace(" ", "").replace("\n", "") == hashing.hexdigest().replace(" ", "").replace("\n", "")

def logout():
    global currentToken
    global expiredTokens
    expiredTokens.append(currentToken)
    currentToken = None
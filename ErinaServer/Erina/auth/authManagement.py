import random
import string

from safeIO import TextFile
import hashlib
from Erina.env_information import erina_dir

currentSalt = None
currentToken = None
salts = []
expiredTokens = []
tempCode = None
class TokenVerification():
    def __init__(self, success=False, expired=False, wrong=False, no_token=False) -> None:
        self.success = success
        self.expired = expired
        self.wrong = wrong
        self.no_token = no_token

    def __repr__(self) -> str:
        if self.success:
            return "Success"
        elif self.expired:
            return "Expired"
        elif self.wrong:
            return "Wrong"
        elif self.no_token:
            return "No Token Provided"
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

def createToken(lengthWithoutSalt):
    global currentToken
    global expiredTokens
    tokenResult = str(currentSalt) + createRandomID(lengthWithoutSalt)
    if tokenResult in expiredTokens:
        tokenResult = createToken(lengthWithoutSalt)
    expiredTokens.append(currentToken)
    currentToken = tokenResult
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
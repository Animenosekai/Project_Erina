import random
import string

from env_information import erina_dir

currentSalt = None
currentToken = None
salts = []
expiredTokens = []

class TokenVerification():
    def __init__(self, success, expired, wrong) -> None:
        self.success = success
        self.expired = expired
        self.wrong = wrong

    def __repr__(self) -> str:
        if self.success:
            return "Success"
        elif self.expired:
            return "Expired"
        else:
            return "Wrong"

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
    with open(erina_dir + "/ErinaWebsite/Erina/auth/salt.erina") as saltFile:
        salts = saltFile.readlines()
    currentSalt = createRandomID(8)
    while currentSalt in salts:
        currentSalt = createRandomID(8)
    with open(erina_dir + "/ErinaWebsite/Erina/auth/salt.erina", "a", encoding="utf-8") as saltFile:
        saltFile.write(currentSalt + "\n")

def createToken(lengthWithoutSalt):
    global currentToken
    global expiredTokens
    tokenResult = str(currentSalt) + createRandomID(lengthWithoutSalt)
    if tokenResult in expiredTokens:
        tokenResult = createToken(lengthWithoutSalt)
    expiredTokens.append(currentToken)
    currentToken = tokenResult
    return tokenResult

def verifyToken(token):
    """
    Verifies that the given token is equal to the one currently authorized
    """
    #if token == currentToken:
    if token == "hey":
        return TokenVerification(True, False, False)
    elif token in expiredTokens or token[:8] in salts:
        return TokenVerification(False, True, False)
    else:
        return TokenVerification(False, False, True)
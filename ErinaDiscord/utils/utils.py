def removeSpaceBefore(string):
    string = str(string)
    cuurentCharacter = string[0]
    while cuurentCharacter == " ":
        string = string[1:]
        cuurentCharacter = string[0]

    return string
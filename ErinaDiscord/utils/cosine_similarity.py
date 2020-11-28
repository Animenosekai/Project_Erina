
import math
import operator
from collections import Counter

class StringVector():
    def __init__(self, string) -> None:
        self.string = str(string)
        self.count = Counter(self.string)
        self.set = set(self.count)
        self.length = math.sqrt(sum(char_count ** 2 for char_count in self.count.values()))

    def __repr__(self) -> str:
        return f"Vector: {str(self.string)}"

commandVectors = {
    StringVector("search"): "search",
    StringVector("info"): "search",
    StringVector("animeinfo"): "search",
    StringVector("information"): "search",
    StringVector("animesearch"): "search",
    
    StringVector("description"): "description",
    StringVector("desc"): "description",
    StringVector("describe"): "description",
    StringVector("animedescription"): "description",
    
    StringVector("dev"): "dev",
    StringVector("development"): "dev",
    StringVector("code"): "dev",
    StringVector("program"): "dev",
    StringVector("github"): "dev",

    StringVector("donate"): "donate",
    StringVector("donation"): "donate",

    StringVector("help"): "help",
    StringVector("helpcenter"): "help",

    StringVector("stats"): "stats",
    StringVector("statistics"): "stats",

    StringVector("invite"): "invite",
    StringVector("invitation"): "invite",
    StringVector("share"): "invite",
}


def searchCommand(userCommand):
    """
    Finds the most similar command
    """
    results_dict = {}
    InputVector = StringVector(userCommand)
    for vector in commandVectors:
        summation = sum(vector.count[character] * InputVector.count[character] for character in vector.set.intersection(InputVector.set))
        length = vector.length * InputVector.length
        similarity = (0 if length == 0 else summation/length)
        results_dict[vector] = similarity
    
    bestResult = max(results_dict.items(), key=operator.itemgetter(1))[0] # Returns the max value
    return commandVectors[bestResult], results_dict[bestResult]

import math
import operator
from collections import Counter

from ErinaDB.ManamiDB.manami_db_data import Database
from Erina.erina_stats import StatsAppend
from Erina.erina_stats import db as DatabaseStats

class StringVector():
    def __init__(self, string) -> None:
        self.string = str(string)
        self.count = Counter(self.string)
        self.set = set(self.count)
        self.length = math.sqrt(sum(char_count ** 2 for char_count in self.count.values()))

    def __repr__(self) -> str:
        return f"Vector: {str(self.string)}"


def search(query):
    """
    Finds the most similar title
    """
    results_dict = {}
    InputVector = StringVector(query)
    for vector in Database.vectors:
        summation = sum(vector.count[character] * InputVector.count[character] for character in vector.set.intersection(InputVector.set))
        length = vector.length * InputVector.length
        similarity = (0 if length == 0 else summation/length)
        results_dict[vector] = similarity
    StatsAppend(DatabaseStats.manamiDBTitleVectorLookups, len(Database.vectors))
    bestResult = max(results_dict.items(), key=operator.itemgetter(1))[0] # Returns the max value
    return Database.vectors[bestResult], results_dict[bestResult]
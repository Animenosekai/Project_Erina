import json
from Erina.env_information import erina_dir
from collections import Counter
import math

class StringVector():
    def __init__(self, string) -> None:
        self.string = str(string)
        self.count = Counter(self.string)
        self.set = set(self.count)
        self.length = math.sqrt(sum(char_count ** 2 for char_count in self.count.values()))

    def __repr__(self) -> str:
        return f"Vector: {str(self.string)}"


class ManamiDB():
    def __init__(self) -> None:
        with open(erina_dir + "/ErinaDB/ManamiDB/manami_database_data.json", "r", encoding="utf-8") as dataFile:
            data = json.load(dataFile)

        self.number_of_animes = len(data)
        self.vectors = {}
        for anime in data:
            for title in data[anime]:
                self.vectors[StringVector(title)] = anime
        
    def updateData(self, data):
        self.number_of_animes = len(data)
        self.vectors = {}
        for anime in data:
            for title in data[anime]:
                self.vectors[StringVector(title)] = anime
    
    def __repr__(self) -> str:
        return f"Manami Database ({str(self.number_of_animes)} animes)"

Database = ManamiDB()
import json
from env_information import erina_dir

class ManamiDB():
    def __init__(self) -> None:
        with open(erina_dir + "/ErinaDB/ManamiDB/manami_database_data.json", "r", encoding="utf-8") as dataFile:
            self.data = json.load(dataFile)
        
    def updateData(self, data):
        self.data = data
    
    def __repr__(self) -> str:
        return f"Manami Database ({len(self.data)} elements)"

Database = ManamiDB()
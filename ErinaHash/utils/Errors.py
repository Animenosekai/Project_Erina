from time import time
from datetime import datetime

class HashingError():
    """
    A hash error
    """
    def __init__(self, type, message) -> None:
        self.type = str(type)
        self.message = str(message)
        self.timestamp = time()
        self.datetime = datetime.fromtimestamp(self.timestamp)
        self.formatted_timestamp = f"{str(self.datetime.year)}-{str(self.datetime.month)}-{str(self.datetime.day)} at {str(self.datetime.hour)}:{str(self.datetime.minute)}:{str(self.datetime.second)}"
    
    def __repr__(self) -> str:
        return f"{str(self.formatted_timestamp)} ErinaHash >> [{self.type}] {self.message}"
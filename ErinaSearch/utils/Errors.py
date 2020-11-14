class SearchingError():
    """
    A search error
    """
    def __init__(self, type, message) -> None:
        self.type = str(type)
        self.message = str(message)
    
    def __repr__(self) -> str:
        return f"ErinaSearch >> [{self.type}] {self.message}"
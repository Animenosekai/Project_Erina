class CachingError():
    """
    A caching error
    """
    def __init__(self, type, message) -> None:
        self.type = str(type)
        self.message = str(message)
    
    def __repr__(self) -> str:
        return f"ErinaCaches >> [{self.type}] {self.message}"
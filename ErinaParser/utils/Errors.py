"""
When an error occurs while parsing a .erina file
"""

class ParserError():
    """
    An error with the parser
    """
    def __init__(self, type, message) -> None:
        self.type = str(type)
        self.message = str(message)

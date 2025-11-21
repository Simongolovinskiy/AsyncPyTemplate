
class DomainError(Exception):
    def __init__(self, message: str, code: int = None, details: dict = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}

    def __str__(self):
        return self.message

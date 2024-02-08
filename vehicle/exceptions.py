# custom_exceptions.py

class ExternalAPIError(Exception):
    def __init__(self, details):
        self.details = details
        super().__init__(f"{details}")

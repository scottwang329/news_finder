class InvalidRequestException(Exception):
    def __init__(self, message="Invalid argument in request"):
        super().__init__(message)

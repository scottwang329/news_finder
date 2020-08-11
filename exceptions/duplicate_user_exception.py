class DuplicateUserException(Exception):
    def __init__(self, message="A user with that username already exists"):
        super().__init__(message)

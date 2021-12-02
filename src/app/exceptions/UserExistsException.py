class UserExistsException(Exception):
    def __init__(self, message="User already exists in the database"):
        super().__init__(message)
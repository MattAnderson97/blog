from database.DatabaseController import DatabaseController

class UserController:
    def __init__(self):
        self.db = DatabaseController("data.db")
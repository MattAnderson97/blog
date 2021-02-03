from database.DatabaseController import DatabaseController

class PostsController:
    def __init__(self):
        self.db = DatabaseController("data.db")

    def get_posts(self):
        return []

    def get_post(self, post_id):
        pass

    def save_post(self, post_title, post_description, post_thumbnail, post_categories, post_date, post_content, author_id, update=False):
        pass
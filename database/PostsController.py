from database.DatabaseController import DatabaseController
import json

class PostsController:
    def __init__(self):
        self.db = DatabaseController("data.db")

    def parse_data(self, post_data) -> dict:
        author_name = self.db.execute_query('SELECT name FROM users WHERE UUID like ?', post_data[7])[0]
        name = post_data[1]
        description = post_data[2]
        thumbnail = post_data[3]
        categories = json.loads(post_data[4])
        date = post_data[5]
        content = post_data[6]
        return {'title': name, 'description': description, 'image': thumbnail, 'categories': categories, 'date': date, 'content': content, 'author': author_name}

    def get_posts(self) -> list:
        query = "SELECT * FROM posts"
        result = self.db.execute_query(query)
        posts = []
        for post in result:
            posts.append(parse_data(post))
        return posts

    def get_post(self, post_id) -> dict:
        query = "SELECT * FROM posts WHERE post_id like ?"
        result = self.db.execute_query(query, post_id)
        return parse_data(result[0]) if len(result) >= 1 else {}

    def save_post(self, post_title, post_description, post_thumbnail, post_categories, post_date, post_content, author_id, update=False):
        pass
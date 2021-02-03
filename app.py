from flask import Flask

from DatabaseController import DatabaseController
from routes import routes

app = Flask(__name__)
app.register_blueprint(routes)

db = DatabaseController("data")


def create_tables():
    db.create_table(
        'users', 
        'UUID INTEGER PRIMARY KEY NOT NULL', 
        'name TEXT NOT NULL', 
        'password_hash TEXT NOT NULL', 
        'password_salt TEXT NOT NULL'
    )
    db.create_table(
        'posts', 
        'post_id INTEGER PRIMARY KEY NOT NULL AUTOINCREMENT', 
        'post_title TEXT NOT NULL', 
        'post_description TEXT', 
        'post_thumbnail BLOB', 
        'post_categories TEXT', 
        'post_date TEXT NOT NULL', 
        'post_content TEXT NOT NULL',
        'author_id INTEGER NOT NULL', 
        'FOREIGN KEY (author_id) REFERENCES Users(UUID)'
    )


if __name__ == "__main__":
    create_tables()
    app.run(host='0.0.0.0', debug=True)
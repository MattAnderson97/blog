from src.app.models.Model import Model
from src.database.database import db


class Comment(db.Model, Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    content = db.Column(db.Text)

    @classmethod
    def new(cls, data):
        comment = cls(
            user_id = data['user_id'],
            post_id = data['post_id'],
            content = data['content']
        )

        db.session.add(comment)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_by_author(cls, author_id):
        return cls.query.fliter_by(user_id=author_id).all()

    @classmethod
    def all(cls):
        return cls.query.all()
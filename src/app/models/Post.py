from src.app.models.Model import Model
from src.app.models.Category import Category
from src.database.database import db


class Post(db.Model, Model):
    title = db.Column(db.String(20))
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.Text)
    categories = db.relationship('Category', secondary='post_categories', back_populates='posts', lazy='dynamic')

    @classmethod
    def new(cls, data):
        post = cls(
            title = data['title'],
            description = data['description'],
            user_id = data['user_id'],
            content = data['content']
        )

        for category_name in data['categories']:
            category = Category.get_by_name(category_name)
            if (category):
                post.categories.append(category)

        db.session.add(post)
        db.session.commit()
        return post

    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)
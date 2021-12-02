from src.app.models.Model import Model
from src.database.database import db


class Category(db.Model, Model):
    name = db.Column(db.String(20), unique=True)
    posts = db.relationship('Post', secondary='post_categories', back_populates='categories', lazy='dynamic')

    @classmethod
    def new(cls, name):
        category = cls(name=name)
        db.session.add(category)
        db.session.commit()
        return category

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def all(cls):
        return cls.query.all()
            

        
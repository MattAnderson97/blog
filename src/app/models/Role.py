from src.app.models.Model import Model
from src.database.database import db
from datetime import datetime


class Role(db.Model, Model):
    name = db.Column(db.String(20))
    can_write = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    users = db.relationship('User', backref='role', lazy=True)

    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def new(cls, data):
        role = cls(
            name=data['name'],
            can_write=data['can_write'],
            is_admin=data['is_admin']
        )
        db.session.add(role)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    def update(self, name, can_write, is_admin):
        self.name = name
        self.can_write = can_write
        self.is_admin = is_admin
        self.date_modified = datetime.now()
        db.session.commit()
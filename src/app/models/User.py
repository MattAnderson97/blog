from flask_login import UserMixin
# Local imports
from src.app.models.Model import Model
from src.app.models.Post import Post
from src.app.models.Role import Role
from src.app.exceptions.UserExistsException import UserExistsException
from src.database.database import db


class User(db.Model, Model, UserMixin):
    name = db.Column(db.String(50))
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    profile_picture = db.Column(db.String(100))
    role_id = db.Column(db.Integer, db.ForeignKey(Role.id))
    posts = db.relationship(Post, backref='author', lazy=True)

    @classmethod
    def new(cls, user_data):
        """Create a new user object

        Args:
            user_data (dictionary): dictionary that expects keys for 'name', 'username', 'email', and 'password'
        """
        if (
            cls.get_by_username(user_data['username'].lower()) 
            or cls.get_by_email(user_data['email'].lower())
        ): raise UserExistsException()

        user = cls(
            name=user_data['name'].lower(),
            username=user_data['username'].lower(),
            email=user_data['email'].lower(),
            password=user_data['password']
        )
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def get_by_id(cls, id):
        """Get a user by their ID

        Args:
            id (int): the user's ID

        Returns:
            User
        """
        return cls.query.get(id)

    @classmethod
    def get_by_username(cls, username):
        """Get a user by their username

        Args:
            username (string): the user's username

        Returns:
            User
        """
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_by_email(cls, email):
        """Get a user by their email address

        Args:
            email (string): the user's email address

        Returns:
            User
        """
        return cls.query.filter_by(email=email).first()

    @classmethod
    def all(cls):
        return cls.query.all()

    def can_write(self):
        if self.role:
            return self.role.can_write
        return False

    def is_admin(self):
        if (self.role):
            return self.role.is_admin
        return False
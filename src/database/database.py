from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from os.path import join


db  = SQLAlchemy()
migrate = Migrate(directory=join('src', 'database', 'migrations'))
from os import environ

SECRET_KEY = environ.get('SECRET_KEY')

#Database
SQLALCHEMY_TRACK_MODIFICATIONS = False # suppress warnings

# get database details
db_type = environ.get('SQLALCHEMY_DATABASE_TYPE')
SQLALCHEMY_DATABASE_URI = None

if (db_type.lower() == "sqlite"):
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{environ.get("SQLALCHEMY_DATABASE_PATH")}'
else:
    db_user = environ.get('SQLALCHEMY_DATABASE_USER')
    db_password = environ.get('SQLALCHEMY_DATABASE_PASSWORD')
    db_host = (environ.get('SQLALCHEMY_DATABASE_HOST') or 'localhost')
    db_port = (environ.get('SQLALCHEMY_DATABASE_PORT') or 3306)
    db_name = environ.get('SQLALCHEMY_DATABASE_NAME')
    SQLALCHEMY_DATABASE_URI = f'{db_type}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'


# Custom blog

A custom blog written with Flask, Flask-Login, Flask-SQLAlchemy and Bootstrap

Docker is being used for a mysql database

## Requirements
--

the requirements can be installed with the command `pip install -r requirements.txt`

- Flask
- Flask-Bootstrap
- Flask-Login
- Flask-Migrate
- Flask-SQLAlchemy
- Flask-WTF
- python-dotenv
- SQLAlchemy
- WTForms
- email-validator
- requests

## Installation

- install dependencies (See requirements section above)
- copy and configure `.env.example` and `.flask.example` 

### To setup mysql with docker-compose

- reconfigure mysql environment settings in `docker-compose.yml` (make sure it's the same as in the `.env` file)
- run the command `docker-compose up` to build/start the database in docker
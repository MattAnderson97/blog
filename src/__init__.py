from dotenv import load_dotenv
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
# local imports
from src.database.database import db, migrate
from src.app.models.Category import Category
from src.app.models.Post import Post
from src.app.models.User import User
from src.routes.routes import routes


# env vars
load_dotenv('.env')

#=============#
# Flask setup #
#=============#

app = Flask(__name__)
app.config.from_pyfile('settings.py')
app.url_map.strict_slashes = False
Bootstrap(app)

@app.before_request
def clear_trailing():
    from flask import redirect, request

    path = request.path
    if path != '/' and path.endswith('/'):
        return redirect(path[:-1])


#================#
# Database setup #
#================#

db.init_app(app)
migrate.init_app(app, db)

post_categories = db.Table(
    'post_categories',
    db.Column('post_id', db.Integer, db.ForeignKey(Post.id, ondelete="cascade")),
    db.Column('category_id', db.Integer, db.ForeignKey(Category.id, ondelete="cascade"))
)

#=============#
# Login Setup #
#=============#

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

#=================#
# register routes #
#=================#

app.register_blueprint(routes)

from flask import abort, Blueprint, render_template, request
from jinja2 import TemplateNotFound
from datetime import datetime

from database.PostsController import PostsController
from database.UserController import UserController

routes = Blueprint('routes', __name__)


@routes.route('/test')
def test_page():
    return render_template('test.html')


@routes.route('/submit_login', methods=['POST'])
def submit_login():
    pass


@routes.route('/submit_regsiter', methods=['POST'])
def submit_register():
    pass


@routes.route('/')
@routes.route('/index')
def index():
    # posts=[
    #     {'title': 'Why Python is great!', 'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer vel justo vel velit feugiat tincidunt vel in dui. Proin sit amet felis semper, euismod ligula eu, interdum augue.', 'image':'https://solidgeargroup.com/wp-content/uploads/2016/08/technology-1283624_770.jpg', 'category': 'code', 'author': 'Matt', 'date': datetime.now().strftime("%d %B, %Y")},
    #     {'title': 'Nvidia RTX 3000 series - Latest and Greatest', 'description': 'Fusce tempus est sed purus facilisis fringilla. Phasellus pulvinar, justo quis posuere blandit, nisl diam interdum sem, a bibendum est purus a arcu.', 'image':'https://cdn.vox-cdn.com/thumbor/AgIu_n_6Ths1IVgV0namvmxdalM=/0x0:2640x1749/2070x1164/filters:focal(1128x940:1550x1362):format(webp)/cdn.vox-cdn.com/uploads/chorus_image/image/67414958/twarren_rtx3080.0.jpg', 'category': 'hardware', 'author': 'Matt', 'date': datetime.now().strftime("%d %B, %Y")}
    # ]
    posts_controller = PostsController()
    posts = posts_controller.get_posts()
    return render_template('index.html', title='home', logged_in=False, posts=posts)


@routes.route('/<page>')
def default(page):
    posts_controller = PostsController()
    post = posts_controller.get_post(page)
    if post != {}:
        return render_template('post.html', title=post['title'], logged_in=False, post=post)
    else:
        title = page
        try:
            return render_template(f'{page}.html', title=title, logged_in=False)
        except TemplateNotFound:
            abort(404)
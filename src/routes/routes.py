from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_user, login_required, logout_user
from flask_migrate import current
from werkzeug.security import check_password_hash, generate_password_hash
import json
# local imports
from src.app.decorators import admin_required, write_required
from src.app.forms.roles.NewRoleForm import NewRoleForm
from src.app.forms.users.LoginForm import LoginForm
from src.app.forms.users.RegisterForm import RegisterForm
from src.app.forms.comments.NewCommentForm import NewCommentForm
from src.app.exceptions.UserExistsException import UserExistsException
from src.app.models.Category import Category
from src.app.models.Post import Post
from src.app.models.Role import Role
from src.app.models.User import User
from src.app.models.Comment import Comment


routes = Blueprint('main', __name__)


@routes.route("/", methods=["GET"])
def home():
    return render_template('index.html', current_user=current_user)


@routes.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegisterForm()
    
    if form.validate_on_submit():
        data = {
            "name": form.name.data,
            "username": form.username.data,
            "email": form.email.data,
            "password": generate_password_hash(form.password.data, method='sha256')
        }

        try:
            login_user(User.new(data))
            return redirect(url_for('main.home'))
        except UserExistsException:
            return render_template('users/register.html', form=form, error="Username or Email already exists")

    return render_template('users/register.html', form=form)


@routes.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()

    if form.validate_on_submit():
        user =  User.get_by_email(form.email.data)
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('main.home'))
        return render_template('users/login.html', form=form, error='Incorrect email or password')    

    return render_template('users/login.html', form=form)


@login_required
@routes.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@login_required
@admin_required
@routes.route("/admin", methods=["GET", "POST"])
def admin_panel():
    # display = request.args.get('display')
    # if not display:
    #     display = 'roles'
    return render_template('admin/admin_panel.html')


@login_required
@admin_required
@routes.route("/roles/create", methods=["GET", "POST"])
def new_role():
    form = NewRoleForm()

    if form.validate_on_submit():
        data = {
            "name": form.name.data,
            "is_admin": form.is_admin.data,
            "can_write": form.can_write.data
        }
        Role.new(data)
        return redirect(url_for('main.roles'))

    return render_template('admin/new_role.html', form=form, current_user=current_user)


@login_required
@admin_required
@routes.route("/roles/update/<role_id>", methods=["POST"])
def update_role(role_id):
    print("update: " + role_id)
    role = Role.get_by_id(int(role_id))
    if (role):
        data = request.form
        if (data):
            name = data.get('name')
            can_write = data.get('can_write') == 'on'
            is_admin = data.get('is_admin') == 'on'
            role.update(name, can_write, is_admin)
    return redirect(url_for('main.roles'))


@login_required
@admin_required
@routes.route("/roles", methods=["GET"])
def roles():
    return render_template("admin/roles.html", roles=Role.all())


@login_required
@admin_required
@routes.route("/users/update/<user_id>", methods=["POST"])
def update_user(user_id):
    user = User.get_by_id(int(user_id))
    if (user):
        pass
    return redirect(url_for('main.manage_users'))


@login_required
@admin_required
@routes.route("/users/manage")
def manage_users():
    return render_template("admin/manage_users.html", users=User.all(), current_user=current_user)


@login_required
@write_required
@routes.route("/posts/create")
def create_post():
    return render_template("posts/create_post.html", categories=Category.all(), current_user=current_user)


@login_required
@write_required
@routes.route("/posts/create/save", methods=["POST"])
def save_post():
    data = request.form
    categories = []

    for key in data.keys():
        if key.startswith("category-"):
            if data[key]:
                categories.append(key.replace("category-", ""))

    post_data = {
        "title": data["title"],
        "description": data["description"],
        "user_id": current_user.id,
        "content": json.dumps(data["content"]),
        "categories": categories
    }

    Post.new(post_data)
    return url_for('main.home')


@routes.route("/comment", methods=["POST"])
def comment():
    form = NewCommentForm()

    if form.validate_on_submit():
        data = {
            'user_id': current_user.id,
            'post_id': form.post.data,
            'content': form.content.data,
            'parent': form.parent.data
        }
        # print(data)
        Comment.new(data)

        return redirect(url_for('main.show_post', post_id=form.post.data))
    return redirect(url_for('main.home'))


@routes.route("/posts")
def posts():
    return render_template('posts/posts.html', posts=Post.all(), current_user=current_user)


@routes.route("/posts/<post_id>")
def show_post(post_id):    
    post = Post.get_by_id(int(post_id))

    if (post):
        content = post.content[1:-1].replace("\\\"", "\"")
        content = json.loads(content)
        # print(content)
        timestamps = {}
        timestamps["published"] = post.date_created.strftime("%B %d, %Y")
        timestamps["modified"] = post.date_modified.strftime("%B %d, %Y")
        
        comment_form = NewCommentForm(post=int(post_id))

        return render_template("posts/post.html", post=post, timestamps=timestamps, content=content, comment_form=comment_form)
    return redirect(url_for('main.home'))

@routes.errorhandler(401)
def unauthorised(e):
    return redirect(url_for('main.login'))

from functools import partial, wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if current_user.is_admin():
            return f(*args, **kwargs)
        else:
            flash("You need to be an admin to view this page")
            return redirect(url_for('main.home'))
    return wrapper



def write_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if current_user.can_write():
            return f(*args, **kwargs)
        else:
            flash("Write access required")
            return redirect(url_for("main.home"))
    return wrapper
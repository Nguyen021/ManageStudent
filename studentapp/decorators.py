from functools import wraps
from flask_login import current_user
from flask import redirect, url_for, abort
from studentapp.models import UserRole


def annonynous_user(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect('/')

        return f(*args, **kwargs)

    return decorated_func


def teacher_requirement(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):

        if current_user.user_role == UserRole.TEACHER or current_user.user_role == UserRole.ADMIN:
            return f(*args, **kwargs)

        else:
            return redirect(url_for('access_denied'))

    return decorated_func


def staff_requirement(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):

        if current_user.user_role == UserRole.STAFF or current_user.user_role == UserRole.ADMIN:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('access_denied'))

    return decorated_func


def admin_requirement(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if current_user.is_authenticated and current_user.user_role == UserRole.ADMIN:
            return redirect('/admin')

        return f(*args, **kwargs)

    return decorated_func

from functools import wraps
from markupsafe import Markup
from flask import flash, redirect, url_for
from flask_login import current_user


def logout_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            flash(Markup('Vous êtes déjà authentifié. <a href = {}> Déconnectez vous</a>'.format(url_for('auth.logout'))))
            return redirect(url_for("main.index"))
        return func(*args, **kwargs)

    return decorated_function

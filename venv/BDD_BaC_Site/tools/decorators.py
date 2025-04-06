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

def admin_required(func):
    @wraps(func)
    def decorated_function(*args,**kwargs):
        if not current_user.is_admin:
            flash("Vous ne pouvez pas accéder à cette page")
            return redirect(url_for('main.index'))
        return func(*args,**kwargs)
    return decorated_function

def confirmed_required(func):
    @wraps(func)
    def decorated_function(*args,**kwargs):
        if not current_user.is_confirmed:
            flash("Vous ne pouvez pas accéder à cette page, il faut vous confirmer")
            return redirect(url_for('auth.resend_confirmation'))
        return func(*args,**kwargs)
    return decorated_function
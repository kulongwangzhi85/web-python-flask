# -*- coding:utf-8 -*-

from functools import wraps
from flask import abort, g
# from flask_login import current_user
from models import Permssion


def permssion_required(permssions):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.user.can(permssions):
                return abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    return permssion_required(Permssion.ADMINISTER)(f)
from werkzeug.local import LocalProxy
from functools import wraps
from flask import request, g
from playmate.models.authentications import Authentication
from playmate.models.users import get_user_by_id
from playmate.exceptions import MissingSessionID, MissingAppToken, \
    AccessUserPermissionDenied


try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


def required_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        session_id = request.headers.get('X-SESSION-ID', None)
        do_auth = Authentication()
        if session_id is None:
            raise MissingSessionID
        else:
            session = do_auth.validate_session(session_id)
        app_token = request.headers.get('X-APP-TOKEN', None)
        if app_token is None:
            raise MissingAppToken
        else:
            do_auth.validate_token(app_token)
        ctx = stack.top
        ctx.login_user = session.user.view()
        if not hasattr(g, '_session'):
            g._session = []
        g._session = session.__dict__
        return f(*args, **kwargs)
    return decorated


def required_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        app_token = request.headers.get('X-APP-TOKEN', None)
        do_auth = Authentication()
        if app_token is None:
            raise MissingAppToken
        else:
            do_auth.validate_token(app_token)
        return f(*args, **kwargs)
    return decorated


def _get_login_user():
    ctx = stack.top
    return getattr(ctx, 'login_user', None)


current_user = LocalProxy(lambda: _get_login_user())


def allow_access(target, role):
    def outer_decorated_function(f):

        def decorated_function(*args, **kwargs):
            if not hasattr(g, '_allow_access'):
                g._allow_access = []

            g._allow_access.append((target, role))
            return f(*args, **kwargs)

        return decorated_function
    return outer_decorated_function


def check_permission(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(g, '_allow_access'):
            g._allow_access = []

        caller_user = get_user_by_id(current_user['user_id'])
        allow = False
        for allow_access in g._allow_access:
            if allow_access[0] == caller_user.roles.role_name:
                if allow_access[1] == "USER":
                    if caller_user.user_id == current_user['user_id']:
                        allow = True
                        break
                if allow_access[1] == "ADMIN":
                    if caller_user.roles.role_name == 'ADMIN':
                        allow = True
                        break
                if allow_access[1] == "SUPERADMIN":
                    if caller_user.roles.role_name == 'SUPERADMIN':
                        allow = True
                        break
        if not allow:
            raise AccessUserPermissionDenied
        else:
            return f(*args, **kwargs)

    return decorated_function

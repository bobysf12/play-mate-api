from werkzeug.local import LocalProxy
from functools import wraps
from flask import request, g
from playmate.models.authentications import Authentication
from playmate.exceptions import MissingSessionID


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

        session = do_auth.validate_session(session_id)

        ctx = stack.top
        ctx.login_user = session
        if not hasattr(g, '_session'):
            g._session = []
        g._session = session
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

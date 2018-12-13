from bson import ObjectId
from playmate import mongo
from playmate.exceptions import UnAuthorized


class Authentication(object):
    """docstring for Authentication"""

    def validate_session(self, session_id):
        session = mongo.db.sessions.find_one({'session_id': session_id})
        if session is None:
            raise UnAuthorized
        user = mongo.db.users.find_one({'_id': ObjectId(session['user_id'])})
        return {
            'user_id': str(user['_id']),
            'name': user['name'],
            'username': user['username']
        }


class ForgotPassword(object):
    """docstring for ForgotPassword"""

    def generate_otp(self, email=None, username=None):
        pass
        # if email is not None:
        #     user = get_user_by_email(email)
        # if username is not None:
        #     user = get_user_by_username(username)
        # if user is None:
        #     raise UnAuthorized

from flask import current_app
from playmate.helpers.cryptographs import generate_session_id
from mallsini.exceptions import UnAuthorized, SessionExpired, IncorrectPassword, InvalidTokenType
from mallsini.helpers.cryptographs import generate_password, validate_password

import md5
import bcrypt
import threading

hash_semaphore = threading.Semaphore(4)


class Authentication(object):
    """docstring for Authentication"""

    def do_login(self, user, password):
        with hash_semaphore:
            # Migrate encrypted password method, then will deprecated when all data has migrated
            match = False
            try:
                match = validate_password(password, user.password)
            except ValueError:
                password = bcrypt.hashpw(password, user.password.encode('utf8'))
                match = (password == user.password)
                if match:
                    user.password = generate_password(password)
                    user.save()
                current_app.logger.info('AES: {}'.format(password))
                current_app.logger.info('BYCRYPT: {}'.format(user.password))
            if not match:
                raise IncorrectPassword
            else:
                hashed_username = md5.new(user.email.lower()).hexdigest() + str(user.user_id)
                session = get_session_by_user_id(user.user_id)
                if session is None:
                    session = generate_session(user.user_id)
                # if session.is_expired:
                session = update_session(user.user_id)
                session_id = session.session_id
                redis.hset('user_sessions', hashed_username, session_id)
        return session_id

    def validate_session(self, session_id):
        session = get_session_by_id(session_id)
        if session is None:
            raise UnAuthorized
        if session.is_expired:
            raise SessionExpired
        return session

    def validate_token(self, token):
        token = get_application_by_token(token)
        if token is None:
            raise InvalidTokenType
        return token

    def get_session_from_cache(self, key):
        return redis.hget('user_sessions', key)

    def delete_session_in_cache(self, email, user_id):
        hashed_username = md5.new(email.lower()).hexdigest() + str(user_id)
        redis.hdel('user_sessions', hashed_username)
        return True


class ForgotPassword(object):
    """docstring for ForgotPassword"""

    def generate_otp(self, email=None, username=None):
        if email is not None:
            user = get_user_by_email(email)
        if username is not None:
            user = get_user_by_username(username)
        if user is None:
            raise UnAuthorized

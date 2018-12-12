import hmac
import uuid
import hashlib
import threading
from flask import current_app

hash_semaphore = threading.Semaphore(4)


class InvalidSalt(Exception):
    """docstring for InvalidSalt"""
    def __init__(self, data, msg=None):
        if msg is None:
            # Set some default useful error message
            msg = "An error occured with car %s" % data
        super(InvalidSalt, self).__init__(msg)
        self.data = data


class Hash256:
    """docstring for Hash256"""

    def hash_password(self, password):
        # uuid is used to generate a random number
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

    def extract_salt(self, hashed_password):
        return hashed_password.split(':')

    def check_password(self, user_password, hashed_password):
        password, salt = self.extract_salt(hashed_password)
        current_app.logger.info('password: {}'.format(password))
        return password == hashlib.sha256(salt.encode('utf8') + user_password.encode('utf8')).hexdigest()


def generate_password(plain_text):
    hash = Hash256()
    return hash.hash_password(plain_text)


def validate_password(user_password, hashed_password):
    hash = Hash256()
    return hash.check_password(user_password, hashed_password)


def generate_session_id(expired):
    session_id = hmac.new(current_app.config.get('APP_SECRET'), expired.strftime('%Y-%m-%d %H:%m:%s'))
    return session_id.digest().encode("hex")

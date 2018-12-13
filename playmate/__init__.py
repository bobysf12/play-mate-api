from flask import Flask, jsonify, request
from flask_restful import Api
from flask_restful_swagger import swagger
from flask_pymongo import PyMongo
# from flask_fcm import FCM
from raven.contrib.flask import Sentry
from playmate.exceptions import BaseExceptions, SessionExpired, MissingSessionID
from playmate.config import config

import logging
import os


app = Flask(__name__, instance_relative_config=True)

environment = os.getenv('APP_CONFIGURATION', 'development')
config_file = environment + '.cfg'
app.config.from_object(config[environment])
app.config.from_pyfile(config_file, silent=True)

api = swagger.docs(Api(app), apiVersion='0.1', api_spec_url='/spec', description="playmate-api")
sentry = Sentry(app, logging=True, level=logging.ERROR)
mongo = PyMongo(app)
# fcm = FCM(app)

# app.config['SQLALCHEMY_ECHO'] = False


app.config['SENTRY_CONFIG'] = {
    'ignore_exceptions': ['werkzeug.exceptions.HTTPException', 'IOError']
}

from playmate.resources.users import RegisterAPI  # noqa: E402
from playmate.resources.events import EventListAPI, EventCreate, EventDetail, EventJoin, EventLeave, EventClose  # noqa: E402

# User Register
api.add_resource(RegisterAPI, '/user/create')
api.add_resource(EventCreate, '/event/create')
api.add_resource(EventListAPI, '/event/list')
api.add_resource(EventDetail, '/event/detail/<string:event_id>')
api.add_resource(EventJoin, '/event/join/<string:event_id>')
api.add_resource(EventLeave, '/event/leave/<string:event_id>')
api.add_resource(EventClose, '/event/close/<string:event_id>')
# api.add_resource(AuthAPI, '/login')


@app.errorhandler(BaseExceptions)
def handler_senseauth_exception(error):
    session_id = request.headers.get('X-SESSION-ID', None)
    if session_id:
        new_error = SessionExpired(session_id=session_id)
    else:
        new_error = MissingSessionID()
    data = {
        "code": new_error.code,
        "reason": new_error.message,
        "extra_info": new_error.extra
    }
    response = jsonify(data)
    response.status_code = new_error.status_code
    return response


@app.errorhandler(BaseExceptions)
def handle_exception(error):
    data = {
        "code": error.code,
        "reason": error.message,
        "extra_info": error.extra
    }
    response = jsonify(data)
    response.status_code = error.status_code
    return response

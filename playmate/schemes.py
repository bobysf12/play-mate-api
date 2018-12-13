from flask_restful import fields
from flask_restful_swagger import swagger


@swagger.model
class User(object):
    """docstring for CreateUser"""

    resource_fields = {
        'user_id': fields.String(),
        'username': fields.String(),
        'password': fields.String(),
        'name': fields.String(),
    }

    required = ['email', 'password']


@swagger.model
class UserResponse(object):
    """docstring for CreateUser"""

    resource_fields = {
        'user_id': fields.String(),
        'username': fields.String(),
        'name': fields.String(),
    }

    required = ['username', 'password']


@swagger.model
@swagger.nested(
    users=User.__name__)
class UserList(object):
    """docstring for ClassName"""

    resource_fields = {
        "data": fields.List(fields.Nested(User.resource_fields)),
        'count': fields.Integer()
    }

    required = ['data']


@swagger.model
class Auth(object):
    """docstring for CreateUser"""

    resource_fields = {
        'username': fields.String(),
        'password': fields.String(),
    }

    required = ['username', 'password']


@swagger.model
class AuthResponse(object):
    """docstring for CreateUser"""

    resource_fields = {
        'session_id': fields.String(),
        'user': fields.Raw(),
    }

    required = ['session_id', 'user']


@swagger.model
class Event(object):
    """docstring for CreateUser"""

    resource_fields = {
        'title': fields.String(),
        'description': fields.String(),
        'location_detail': fields.String(),
        'start_time': fields.String(),
        'end_time': fields.String(),
        'longitude': fields.Float(),
        'latitude': fields.Float(),
        'max_person': fields.Integer()
    }

    required = ['title', 'longitude', 'latitude', 'max_person']


@swagger.model
class EventResponse(object):
    """docstring for CreateUser"""

    resource_fields = {
        'id': fields.String(),
        'title': fields.String(),
        'description': fields.String(),
        'location_detail': fields.String(),
        'start_time': fields.String(),
        'end_time': fields.String(),
        'location': fields.Raw(),
        'max_person': fields.Integer(),
        'participants': fields.Raw()
    }

    required = ['title', 'longitude', 'latitude', 'max_person']


@swagger.model
@swagger.nested(
    event=Event.__name__)
class Eventlist(object):
    """docstring for ClassName"""

    resource_fields = {
        "data": fields.List(fields.Nested(EventResponse.resource_fields)),
        'count': fields.Integer()
    }

    required = ['data']

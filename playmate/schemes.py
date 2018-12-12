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
@swagger.nested(
    users=User.__name__)
class UserList(object):
    """docstring for ClassName"""

    resource_fields = {
        "users": fields.List(fields.Nested(User.resource_fields)),
        'count': fields.Integer()
    }

    required = ['users']

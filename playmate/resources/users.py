from flask_restful_swagger import swagger
from flask_restful import Resource, reqparse, marshal_with
# from flask import current_app
# from playmate.helpers.utilities import email_validator, notify_user
# from playmate.helpers.decorators import required_auth, required_token, current_user, allow_access, check_permission
from playmate.exceptions import FieldRequired
from playmate import mongo
from playmate.schemes import User


create_user_parser = reqparse.RequestParser()
create_user_parser.add_argument('username', type=str)
create_user_parser.add_argument('password', type=str)
create_user_parser.add_argument('name', type=str)


STATUS = {'active': 1, 'inactive': 2}


class RegisterAPI(Resource):
    """docstring for Users"""

    @swagger.operation(
        notes="""Add user / registered new user""",
        parameters=[
            {
                "name": "X-SESSION-ID",
                "description": "",
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "header"
            },
            {
                "name": "user",
                "description": "",
                "required": True,
                "allowMultiple": False,
                "dataType": User.__name__,
                "paramType": "body"
            }
        ],
        responseClass=User.__name__,
        responseMessages=[
            {
                "code": 200,
                "message": "OK"
            },
            FieldRequired.to_swagger(),
        ]
    )
    # @required_token
    @marshal_with(User.resource_fields)
    def post(self):
        "user register"
        args = create_user_parser.parse_args()
        if args['password'] is None:
            raise FieldRequired(required_field='password')
        if args['name'] is None:
            raise FieldRequired(required_field='name')
        doc = {
            'username': args['username'],
            'name': args['name'],
            'password': args['password'],
        }

        user = mongo.db.users.insert_one(doc)
        user = mongo.db.users.find_one({'_id': user.inserted_id})

        return user, 200

import md5
from datetime import datetime
from flask_restful_swagger import swagger
from flask_restful import Resource, reqparse, marshal_with
from playmate import mongo
from playmate.schemes import Auth, AuthResponse
from playmate.exceptions import FieldRequired, IncorrectPassword, UserNotFound
from playmate.helpers.cryptographs import generate_session_id

auth_parser = reqparse.RequestParser()
auth_parser.add_argument('username', type=str)
auth_parser.add_argument('password', type=str)


class LoginAPI(Resource):

    @swagger.operation(
        notes="""Authentication API""",
        parameters=[
            {
                "name": "user",
                "description": "",
                "required": True,
                "allowMultiple": False,
                "dataType": Auth.__name__,
                "paramType": "body"
            }
        ],
        responseClass=AuthResponse.__name__,
        responseMessages=[
            {
                "code": 200,
                "message": "OK"
            },
            FieldRequired.to_swagger(),
        ]
    )
    @marshal_with(AuthResponse.resource_fields)
    def post(self):
        "Login"
        args = auth_parser.parse_args()
        if args['password'] is None:
            raise FieldRequired(required_field='password')
        if args['username'] is None:
            raise FieldRequired(required_field='username')

        user = mongo.db.users.find_one({'username': args['username']})
        if not user:
            raise UserNotFound

        if md5.new(args['password']).hexdigest() != user['password']:
            raise IncorrectPassword

        session_id = generate_session_id(datetime.utcnow())
        mongo.db.sessions.insert_one({
            'user_id': str(user['_id']),
            'session_id': session_id
        })

        return {
            'session_id': session_id,
            'user': {
                'username': user['username'],
                'name': user['name'],
                'user_id': str(user['_id']),
            }
        }, 200


class LogoutAPI(Resource):
    pass

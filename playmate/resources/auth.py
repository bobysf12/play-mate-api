from playmate import mongo
from playmate.schemes import User
from flask_restful_swagger import swagger
from flask_restful import Resource, reqparse, marshal_with
from playmate.exceptions import FieldRequired

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
        "Login"
        args = auth_parser.parse_args()
        if args['password'] is None:
            raise FieldRequired(required_field='password')
        if args['username'] is None:
            raise FieldRequired(required_field='username')

        user = mongo.db.users.find_one({'username': args['username']})
        if not user:
            raise Exception()

        if args['password'] != user['password']:
            raise Exception()

        return user, 200


class LogoutAPI(Resource):
    pass

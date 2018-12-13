import md5
from flask_restful_swagger import swagger
from flask_restful import Resource, reqparse, marshal_with
# from flask import current_app
from playmate.exceptions import FieldRequired, UserExist
from playmate import mongo
from playmate.schemes import User, UserResponse


create_user_parser = reqparse.RequestParser()
create_user_parser.add_argument('username', type=str)
create_user_parser.add_argument('password', type=str)
create_user_parser.add_argument('name', type=str)


class RegisterAPI(Resource):
    """docstring for Users"""

    @swagger.operation(
        notes="""Add user / registered new user""",
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
        responseClass=UserResponse.__name__,
        responseMessages=[
            {
                "code": 200,
                "message": "OK"
            },
            FieldRequired.to_swagger(),
        ]
    )
    @marshal_with(UserResponse.resource_fields)
    def post(self):
        "user register"
        args = create_user_parser.parse_args()
        if args['password'] is None:
            raise FieldRequired(required_field='password')
        if args['name'] is None:
            raise FieldRequired(required_field='name')
        old_user = mongo.db.users.find_one({'username': args['username']})
        if old_user and len(old_user) > 0:
            raise UserExist

        doc = {
            'username': args['username'],
            'name': args['name'],
            'password': md5.new(args['password']).hexdigest(),
        }

        user = mongo.db.users.insert_one(doc)
        user = mongo.db.users.find_one({'_id': user.inserted_id})
        user['user_id'] = user['_id']
        return user, 200

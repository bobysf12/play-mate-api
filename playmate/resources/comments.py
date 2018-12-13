from bson import ObjectId
from datetime import datetime
from flask_restful_swagger import swagger
from flask_restful import Resource, reqparse, marshal_with
from playmate import mongo
from playmate import schemes
from playmate.helpers.decorators import current_user, required_auth
from playmate.exceptions import FieldRequired


comment_parser = reqparse.RequestParser()
comment_parser.add_argument('text', type=str)
comment_parser.add_argument('type', type=str, default='chat')

comment_get_parser = reqparse.RequestParser()
comment_get_parser.add_argument('type', type=str, location='args', default='chat')


class CommentPost(Resource):
    """docstring for Comment"""

    @swagger.operation(
        notes="""Post a comment""",
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
                "name": "data",
                "description": "",
                "required": True,
                "allowMultiple": False,
                "dataType": schemes.Comment.__name__,
                "paramType": "body"
            }
        ],
        responseClass=schemes.CommentResponse.__name__,
        responseMessages=[
            {
                "code": 200,
                "message": "OK"
            },
            FieldRequired.to_swagger(),
        ]
    )
    @required_auth
    @marshal_with(schemes.CommentResponse.resource_fields)
    def post(self, event_id=None):
        "Post comment"
        args = comment_parser.parse_args()
        if args['text'] is None:
            raise FieldRequired(required_field='text')

        doc = {
            'text': args['text'],
            'type': args['type'],
            'created_at': datetime.utcnow(),
            'user_id': current_user['user_id'],
            'event_id': event_id
        }

        comment = mongo.db.comments.insert_one(doc)
        comment = mongo.db.comments.find_one({'_id': comment.inserted_id})
        comment['id'] = comment['_id']
        comment['user'] = {
            'user_id': current_user['user_id'],
            'username': current_user['username'],
            'name': current_user['name'],
        }
        return comment, 200


class Commentlist(Resource):
    """docstring for event list"""

    @swagger.operation(
        notes="""Retrieve list of comment""",
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
                "name": "type",
                "description": "",
                "required": False,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "query"
            }
        ],
        responseClass=schemes.CommentList.__name__,
        responseMessages=[
            {
                "code": 200,
                "message": "OK"
            },
        ]
    )
    @required_auth
    @marshal_with(schemes.CommentList.resource_fields)
    def get(self, event_id=None):
        "get list event"
        args = comment_get_parser.parse_args()
        comments_cursor = mongo.db.comments.find({'event_id': event_id, 'type': args['type']})
        comments = []
        for comment in comments_cursor:
            user = mongo.db.users.find_one({'_id': ObjectId(comment['user_id'])})
            comment['user'] = {
                'username': user['username'],
                'user_id': str(user['_id']),
                'name': user['name']
            }

            comment['id'] = str(comment.get('_id'))
            comments.append(
                comment
            )
        return {'data': comments, 'count': len(comments)}

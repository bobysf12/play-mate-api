from bson import ObjectId
from flask import current_app
from flask_restful_swagger import swagger
from flask_restful import Resource, reqparse, marshal_with
from playmate import mongo
from playmate import schemes
from playmate.exceptions import FieldRequired, DataNotfound, AlreadyJoin

event_create_parser = reqparse.RequestParser()
event_create_parser.add_argument('title', type=str)
event_create_parser.add_argument('description', type=str)
event_create_parser.add_argument('location_detail', type=str)
event_create_parser.add_argument('start_time', type=str)
event_create_parser.add_argument('end_time', type=str)
event_create_parser.add_argument('longitude', type=float)
event_create_parser.add_argument('latitude', type=float)
event_create_parser.add_argument('max_person', type=int)
event_create_parser.add_argument('status', type=str)

event_get_parser = reqparse.RequestParser()
event_get_parser.add_argument('start_time', type=str)
event_get_parser.add_argument('end_time', type=str)
event_get_parser.add_argument('longitude', type=float)
event_get_parser.add_argument('latitude', type=float)
event_get_parser.add_argument('status', type=str)


class EventListAPI(Resource):
    """docstring for event list"""

    @swagger.operation(
        notes="""Retrieve list of users""",
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
                "name": "start_time",
                "description": "",
                "required": False,
                "allowMultiple": False,
                "dataType": "iso string",
                "paramType": "query"
            },
            {
                "name": "end_time",
                "description": "",
                "required": False,
                "allowMultiple": False,
                "dataType": "iso string",
                "paramType": "query"
            },
            {
                "name": "longitude",
                "description": "",
                "required": False,
                "allowMultiple": False,
                "dataType": "float",
                "paramType": "query"
            },
            {
                "name": "latitude",
                "description": "",
                "required": False,
                "allowMultiple": False,
                "dataType": "float",
                "paramType": "query"
            }
        ],
        responseClass=schemes.Eventlist.__name__,
        responseMessages=[
            {
                "code": 200,
                "message": "OK"
            },
        ]
    )
    # @required_auth
    @marshal_with(schemes.Eventlist.resource_fields)
    def get(self):
        "get list event"
        args = event_get_parser.parse_args()
        filters = {}
        if filters:
            args

        events_cursor = mongo.db.events.find(filters)
        events = []
        for event in events_cursor:
            event['participants'] = [
                mongo.db.users.find_one({'_id': user._id for user in event.get('participants', [])})
            ]
            event['id'] = event.get('_id')
            events.append(
                event
            )
        # events = [data for data in events_cursor]

        return {'data': events, 'count': len(events)}


class EventCreate(Resource):
    """docstring for event creation"""

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
                "name": "data",
                "description": "",
                "required": True,
                "allowMultiple": False,
                "dataType": schemes.Event.__name__,
                "paramType": "body"
            }
        ],
        responseClass=schemes.Event.__name__,
        responseMessages=[
            {
                "code": 200,
                "message": "OK"
            },
            FieldRequired.to_swagger(),
        ]
    )
    # @required_token
    @marshal_with(schemes.EventResponse.resource_fields)
    def post(self):
        "register new event"
        args = event_create_parser.parse_args()
        if args['title'] is None:
            raise FieldRequired(required_field='title')
        if args['description'] is None:
            raise FieldRequired(required_field='description')
        doc = {
            'title': args['title'],
            'description': args['description'],
            'location_detail': args['location_detail'],
            'start_time': args['start_time'],
            'end_time': args['end_time'],
            'location': {
                'type': 'Point',
                'coordinates': [
                    args['longitude'],
                    args['latitude']
                ]
            },
            'max_person': args['max_person'],
            # 'creator_id': args['creator_id'],
        }

        event = mongo.db.events.insert_one(doc)
        current_app.logger.info(type(event.inserted_id))
        event = mongo.db.events.find_one({'_id': event.inserted_id})

        event['location'] = {
            'longitude': args['longitude'],
            'latitude': args['latitude']
        }

        event['id'] = event['_id']

        return event, 200


class EventDetail(Resource):
    @swagger.operation(
        notes="""get event detail""",
        parameters=[
            {
                "name": "X-SESSION-ID",
                "description": "",
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "header"
            }
        ],
        responseClass=schemes.Event.__name__,
        responseMessages=[
            {
                "code": 200,
                "message": "OK"
            }
        ]
    )
    # @required_token
    @marshal_with(schemes.EventResponse.resource_fields)
    def get(self, event_id=None):
        "get new event"
        current_app.logger.info(event_id)
        event = mongo.db.events.find_one({'_id': ObjectId(event_id)})

        if event is None:
            raise DataNotfound

        return event, 200


class EventJoin(Resource):

    @swagger.operation(
        notes="""get event detail""",
        parameters=[
            {
                "name": "X-SESSION-ID",
                "description": "",
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "header"
            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "OK"
            }
        ]
    )
    # @required_token
    def put(self, event_id=None):
        "join new event"
        current_event = mongo.db.events.find_one({'_id': ObjectId(event_id)})
        user_id = 1
        if user_id in current_event.get('participant', []):
            raise AlreadyJoin

        event = mongo.db.events.update({'_id': ObjectId(event_id)}, {'$set': {'participant': current_event.get('participant', []) + [user_id]}})
        current_app.logger.info(event_id)

        if event is None:
            raise DataNotfound

        return 200


class EventLeave(Resource):

    @swagger.operation(
        notes="""leave current event""",
        parameters=[
            {
                "name": "X-SESSION-ID",
                "description": "",
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "header"
            }
        ],
        responseClass=schemes.Event.__name__,
        responseMessages=[
            {
                "code": 200,
                "message": "OK"
            }
        ]
    )
    # @required_token
    def delete(self, event_id=None):
        "leave new event"
        current_event = mongo.db.events.find_one({'_id': ObjectId(event_id)})
        user_id = 1
        participant = current_event.get('participant', [])
        if user_id not in participant:
            raise DataNotfound

        participant.remove(user_id)
        current_app.logger.info(participant)

        mongo.db.events.update({'_id': ObjectId(event_id)}, {'$set': {'participant': participant}})

        return 200


class EventClose(Resource):

    @swagger.operation(
        notes="""close current event""",
        parameters=[
            {
                "name": "X-SESSION-ID",
                "description": "",
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "header"
            }
        ],
        responseClass=schemes.Event.__name__,
        responseMessages=[
            {
                "code": 200,
                "message": "OK"
            }
        ]
    )
    # @required_token
    def delete(self, event_id=None):
        "close new event"
        current_event = mongo.db.events.find_one({'_id': ObjectId(event_id)})
        if not current_event:
            raise DataNotfound

        mongo.db.events.update({'_id': ObjectId(event_id)}, {'$set': {'status': 'closed'}})

        return 200

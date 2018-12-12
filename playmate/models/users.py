from playmate import db


class Users(db.Document):
    user_id = db.StringField(required=True)
    username = db.StringField(max_length=50)
    password = db.StringField(max_length=50)
    name = db.StringField(max_length=50)

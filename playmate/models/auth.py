from playmate import db


class Sessions(db.Document):
    user_id = db.StringField(required=True)
    session_id = db.StringField(max_length=50)

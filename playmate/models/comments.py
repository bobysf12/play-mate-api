from playmate import db


class Comments(db.Document):
    comm_id = db.StringField(required=True)
    text = db.StringField()
    type = db.StringField(max_length=50)
    created_at = db.DateTimeField()
    user_id = db.StringField(max_length=50)
    event_id = db.StringField(max_length=50)

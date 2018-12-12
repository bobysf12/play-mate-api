from playmate import db


class Events(db.Document):
    event_id = db.StringField(required=True)
    title = db.StringField(max_length=50)
    description = db.StringField(max_length=50)
    start_time = db.DateTimeField()
    end_time = db.DateTimeField()
    location = db.DictField()
    max_person = db.FieldList()
    participan = db.FieldList()

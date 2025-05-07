import datetime
from enum import Enum
from mongoengine import Document, StringField, EnumField, ObjectIdField, DateTimeField # type: ignore


class UserType(Enum):
    ANONYMOUS = 'anonymous'
    REGISTERED = 'registered'


class User(Document):

    meta = {'collection': 'users'}

    username = StringField(required=True, unique=True)
    password_hash = StringField(required=True)
    name = StringField(required=True)
    email = StringField(required=True)
    type = EnumField(UserType, required=True)
    plan = ObjectIdField()
    registered_at = DateTimeField(default=datetime.datetime.now())

    def to_json(self) -> dict:
        return {
            'username' : self.username,
            'password_hash': self.password_hash,
            'name': self.name,
            'email': self.email,
            'type': self.type.value,
            'plan': str(self.plan),
            'registered_at': str(self.registered_at),
        }
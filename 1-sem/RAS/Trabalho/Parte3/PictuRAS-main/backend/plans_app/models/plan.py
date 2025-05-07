import datetime
from enum import Enum
from mongoengine import Document # type: ignore
from mongoengine.fields import EnumField, StringField, DecimalField, DateTimeField # type: ignore


class PlanType(Enum):
    DAILY = 'daily'
    MONTHLY = 'monthly'
    ANNUAL = 'annual'


class Plan(Document):

    meta = {'collection': 'plans'}

    name = StringField(required=True)
    price = DecimalField(required=True)
    type = EnumField(PlanType, default=PlanType.MONTHLY)
    inserted_at = DateTimeField(default=datetime.datetime.now())

    def to_json(self) -> dict:
        return {
            'id': str(self.id),
            'name': self.name,
            'price': self.price,
            'type': self.type.value,
            'inserted_at': str(self.inserted_at),
        }
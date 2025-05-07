import datetime
from enum import Enum
from mongoengine import Document, StringField, DateTimeField, ListField, EmbeddedDocument, EmbeddedDocumentField, EnumField, DynamicField, BooleanField, ObjectIdField # type: ignore


class InputOutputType(Enum):
    IMAGE = 'image'
    TEXT = 'text'


class ParameterType(Enum):
    INT = 'int'
    FLOAT = 'float'
    STRING = 'string'
    HEX = 'hex'


class Parameter(EmbeddedDocument):
    name = StringField(required=True)
    type =  EnumField(ParameterType, required=True)
    value = DynamicField(required=True)
    min_value = DynamicField()
    max_value = DynamicField()

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'type': self.type.value,
            'value': self.value,
            'min_value': self.min_value,
            'max_value': self.max_value,
        }


class Tool(EmbeddedDocument):
    id = ObjectIdField(required=False)
    name = StringField(required=True) 
    input_type = EnumField(InputOutputType, required=True)
    output_type = EnumField(InputOutputType, required=True)
    premium = BooleanField(required=False)
    parameters = ListField(EmbeddedDocumentField(Parameter), default=[])

    def to_json(self) -> dict:
        return {
            'id': str(self.id),
            'name': self.name,
            'input_type': self.input_type.value,
            'output_type': self.output_type.value,
            'parameters': [parameter.to_json() for parameter in self.parameters],
        }


class Project(Document):

    meta = {'collection': 'projects'}

    name = StringField(required=True)
    owner = StringField(required=True)
    date = DateTimeField(default=datetime.datetime.now())
    tools = ListField(EmbeddedDocumentField(Tool), default=[])

    def to_json(self) -> dict:
        return {
            'id': str(self.id),
            'name': self.name,
            'owner': self.owner,
            'date': str(self.date),
            'tools': [tool.to_json() for tool in self.tools],
        }
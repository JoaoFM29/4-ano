import json

class BorderMessageReply:

    def __init__(self, mimetype: str, data: str) -> None:
        self.mimetype = mimetype
        self.data = data


    def getMimeType(self) -> str:
        return self.mimetype


    def getData(self) -> str:
        return self.data


    def to_json(self) -> str:
        return json.dumps({
            'mimetype': self.mimetype,
            'data': self.data,
        })


    @staticmethod
    def from_json(data: str) -> 'BorderMessageReply':
        data = json.loads(data)
        return BorderMessageReply(
            mimetype=data['mimetype'],
            data=data['data'],
        )
import json

class PeopleCountingMessageRequest:

    def __init__(self, image: str) -> None:
        self.image = image

    def getImage(self) -> str:
        return self.image

    def to_json(self) -> str:
        return json.dumps({
            'image': self.image,
        })

    @staticmethod
    def from_json(data: str) -> 'PeopleCountingMessageRequest':
        data = json.loads(data)
        return PeopleCountingMessageRequest(
            image=data['image'],
        )
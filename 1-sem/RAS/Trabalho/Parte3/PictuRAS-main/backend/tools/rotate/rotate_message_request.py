import json

class RotateMessageRequest:

    def __init__(self, image: str, angle : int) -> None:
        self.image = image
        self.angle = angle


    def getImage(self) -> str:
        return self.image


    def getAngle(self) -> int:
        return self.angle


    def to_json(self) -> str:
        return json.dumps({
            'image': self.image,
            'angle': self.angle,
        })


    @staticmethod
    def from_json(data: str) -> 'RotateMessageRequest':
        data = json.loads(data)
        return RotateMessageRequest(
            image=data['image'],
            angle=data['angle'],
        )
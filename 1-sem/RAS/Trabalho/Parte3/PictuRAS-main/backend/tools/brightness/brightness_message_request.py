import json

class BrightnessMessageRequest:

    def __init__(self, image: str, brightness : float) -> None:
        self.image = image
        self.brightness = brightness


    def getImage(self) -> str:
        return self.image


    def getBrightness(self) -> float:
        return self.brightness


    def to_json(self) -> str:
        return json.dumps({
            'image': self.image,
            'brightness': self.brightness
        })


    @staticmethod
    def from_json(data: str) -> 'BrightnessMessageRequest':
        data = json.loads(data)
        return BrightnessMessageRequest(
            image=data['image'],
            brightness=data['brightness'],
        )
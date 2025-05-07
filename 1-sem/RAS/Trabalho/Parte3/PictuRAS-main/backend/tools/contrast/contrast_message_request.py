import json

class ContrastMessageRequest:

    def __init__(self, image: str, contrast : float) -> None:
        self.image = image
        self.contrast = contrast


    def getImage(self) -> str:
        return self.image


    def getContrast(self) -> float:
        return self.contrast


    def to_json(self) -> str:
        return json.dumps({
            'image': self.image,
            'contrast': self.contrast,
        })


    @staticmethod
    def from_json(data: str) -> 'ContrastMessageRequest':
        data = json.loads(data)
        return ContrastMessageRequest(
            image=data['image'],
            contrast=data['contrast'],
        )
import json

class CropMessageRequest:

    def __init__(self, image: str, width : int, height : int, x_top_left : int, y_top_left : int) -> None:
        self.image = image
        self.width = width
        self.height = height
        self.x_top_left = x_top_left
        self.y_top_left = y_top_left


    def getImage(self) -> str:
        return self.image
    

    def getWidth(self) -> int:
        return self.width
    

    def getHeight(self) -> int:
        return self.height
    

    def getXTopLeft(self) -> int:
        return self.x_top_left
    

    def getYTopLeft(self) -> int:
        return self.y_top_left


    def to_json(self) -> str:
        return json.dumps({
            'image': self.image,
            'width': self.width,
            'height': self.height,
            'x_top_left': self.x_top_left,
            'y_top_left': self.y_top_left,
        })


    @staticmethod
    def from_json(data: str) -> 'CropMessageRequest':
        data = json.loads(data)
        return CropMessageRequest(
            image=data['image'],
            width=data['width'],
            height=data['height'],
            x_top_left=data['x_top_left'],
            y_top_left=data['y_top_left'],
        )
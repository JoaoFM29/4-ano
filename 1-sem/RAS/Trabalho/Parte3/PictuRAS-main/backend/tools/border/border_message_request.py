import json

class BorderMessageRequest:

    def __init__(self, image: str, border_height : int, border_width : int, border_color : str) -> None:
        self.image = image
        self.border_height = border_height
        self.border_width = border_width
        self.border_color = border_color


    def getImage(self) -> str:
        return self.image


    def getBorderHeight(self) -> int:
        return self.border_height


    def getBorderWidth(self) -> int:
        return self.border_width


    def getBorderColor(self) -> str:
        return self.border_color


    def to_json(self) -> str:
        return json.dumps({
            'image': self.image,
            'border_height': self.border_height,
            'border_width': self.border_width,
            'border_color': self.border_color,
        })


    @staticmethod
    def from_json(data: str) -> 'BorderMessageRequest':
        data = json.loads(data)
        return BorderMessageRequest(
            image=data['image'],
            border_height=data['border_height'],
            border_width=data['border_width'],
            border_color=data['border_color'],
        )
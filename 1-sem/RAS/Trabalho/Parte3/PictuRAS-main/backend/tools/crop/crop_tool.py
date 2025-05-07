import magic
import base64
import subprocess
from crop_message_reply import CropMessageReply
from crop_message_request import CropMessageRequest

class CropTool:

    def __init__(self, request : CropMessageRequest) -> None:
        self.request = request


    def apply(self) -> CropMessageReply:

        mime = magic.Magic(mime=True)

        width = self.request.getWidth()
        height = self.request.getHeight()
        x = self.request.getXTopLeft()
        y = self.request.getYTopLeft()

        ffmpeg_command = [
            'ffmpeg',
            '-i', '-',
            '-vf', f'crop={width}:{height}:{x}:{y}',
            '-preset', 'ultrafast',
            '-f', 'image2', '-'
        ]

        result = subprocess.run(
            ffmpeg_command,
            input=base64.b64decode(self.request.getImage()),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )

        return CropMessageReply(
            mimetype=mime.from_buffer(result.stdout),
            data=base64.b64encode(result.stdout).decode('utf-8'),
        )
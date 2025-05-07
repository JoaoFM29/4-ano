import magic
import base64
import subprocess
from scale_message_reply import ScaleMessageReply
from scale_message_request import ScaleMessageRequest

class ScaleTool:

    def __init__(self, request : ScaleMessageRequest) -> None:
        self.request = request


    def apply(self) -> ScaleMessageReply:

        mime = magic.Magic(mime=True)

        ffmpeg_command = [
            'ffmpeg',
            '-i', '-',
            '-vf', f'scale={self.request.getWidth()}:{self.request.getHeight()}',
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

        return ScaleMessageReply(
            mimetype=mime.from_buffer(result.stdout),
            data=base64.b64encode(result.stdout).decode('utf-8'),
        )
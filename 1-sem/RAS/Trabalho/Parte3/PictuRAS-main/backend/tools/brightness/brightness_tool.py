import magic
import base64
import subprocess
from brightness_message_reply import BrightnessMessageReply
from brightness_message_request import BrightnessMessageRequest

class BrightnessTool:

    def __init__(self, request : BrightnessMessageRequest) -> None:
        self.request = request


    def apply(self) -> BrightnessMessageReply:

        mime = magic.Magic(mime=True)

        ffmpeg_command = [
            'ffmpeg',
            '-i', '-',
            '-vf', f'eq=brightness={self.request.getBrightness()}',
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

        return BrightnessMessageReply(
            mimetype=mime.from_buffer(result.stdout),
            data=base64.b64encode(result.stdout).decode('utf-8'),
        )
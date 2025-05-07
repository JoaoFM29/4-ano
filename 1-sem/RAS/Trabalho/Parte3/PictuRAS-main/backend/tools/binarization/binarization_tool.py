import magic
import base64
import subprocess
from binarization_message_reply import BinarizationMessageReply
from binarization_message_request import BinarizationMessageRequest

class BinarizationTool:

    def __init__(self, request : BinarizationMessageRequest) -> None:
        self.request = request


    def apply(self) -> BinarizationMessageReply:

        mime = magic.Magic(mime=True)

        ffmpeg_command = [
            'ffmpeg',
            '-i', '-',
            '-vf', 'format=gray',
            '-f', 'image2', '-'
        ]

        result = subprocess.run(
            ffmpeg_command,
            input=base64.b64decode(self.request.getImage()),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )

        return BinarizationMessageReply(
            mimetype=mime.from_buffer(result.stdout),
            data=base64.b64encode(result.stdout).decode('utf-8'),
        )
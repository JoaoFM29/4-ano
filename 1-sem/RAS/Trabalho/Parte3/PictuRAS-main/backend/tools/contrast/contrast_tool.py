import magic
import base64
import subprocess
from contrast_message_reply import ContrastMessageReply
from contrast_message_request import ContrastMessageRequest

class ContrastTool:

    def __init__(self, request : ContrastMessageRequest) -> None:
        self.request = request


    def apply(self) -> ContrastMessageReply:

        mime = magic.Magic(mime=True)

        ffmpeg_command = [
            'ffmpeg',
            '-i', '-',
            '-vf', f'eq=contrast={self.request.getContrast()}',
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
        
        return ContrastMessageReply(
            mimetype=mime.from_buffer(result.stdout),
            data=base64.b64encode(result.stdout).decode('utf-8'),
        )
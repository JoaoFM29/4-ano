import magic
import base64
import subprocess
from border_message_reply import BorderMessageReply 
from border_message_request import BorderMessageRequest

class BorderTool:

    def __init__(self, request : BorderMessageRequest) -> None:
        self.request = request


    def apply(self) -> BorderMessageReply:

        mime = magic.Magic(mime=True)

        border_width = self.request.getBorderWidth()
        border_height = self.request.getBorderHeight()
        color = self.request.getBorderColor()

        ffmpeg_command = [
            'ffmpeg',
            '-i', '-',
            '-vf', f'pad=width=iw+{border_width*2}:height=ih+{border_height*2}:x={border_width}:y={border_height}:color={color}',
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

        return BorderMessageReply(
            mimetype=mime.from_buffer(result.stdout),
            data=base64.b64encode(result.stdout).decode('utf-8'),
        )
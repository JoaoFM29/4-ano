import magic
import base64
from rembg import remove # type: ignore
from autocrop_message_reply import AutoCropMessageReply
from autocrop_message_request import AutoCropMessageRequest

class AutoCropTool:

    def __init__(self, request: AutoCropMessageRequest) -> None:
        self.request = request


    def apply(self) -> AutoCropMessageReply:

        mime = magic.Magic(mime=True)

        input_image_data = base64.b64decode(self.request.getImage())
        output_image_data = remove(input_image_data)

        return AutoCropMessageReply(
            mimetype=mime.from_buffer(output_image_data),
            data=base64.b64encode(output_image_data).decode('utf-8'),
        )

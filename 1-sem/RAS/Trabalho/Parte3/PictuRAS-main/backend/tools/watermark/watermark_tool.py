import magic
import base64
import random
import io
from PIL import Image, ImageEnhance # type: ignore
from watermark_message_reply import WatermarkMessageReply
from watermark_message_request import WatermarkMessageRequest

class WatermarkTool:

    def __init__(
        self,
        request: WatermarkMessageRequest,
        watermark_image_path: str,
        opacity: float = 0.7,
    ) -> None:
        """
        Initialize the WatermarkTool with the path to the watermark image.

        Args:
            watermark_image_path (str): Path to the watermark image.
            opacity (float): Transparency level of the watermark (0.0 to 1.0).
        """
        self.request = request
        self.watermark_image = Image.open(watermark_image_path).convert("RGBA")
        self.opacity = opacity

    def _apply_opacity(self, image: Image.Image) -> Image.Image:
        alpha = image.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(self.opacity)
        image.putalpha(alpha)
        return image

    def apply(self) -> WatermarkMessageReply:
        """
        Apply the watermark to the input image.

        Args:
            request (WatermarkMessageRequest): Request containing the image to watermark.

        Returns:
            WatermarkMessageReply: Reply containing the watermarked image.
        """
        # Decode the input image from base64
        input_image_data = base64.b64decode(self.request.getImage())
        input_image = Image.open(io.BytesIO(input_image_data)).convert("RGBA")
        # Resize and adjust the watermark's opacity
        watermark = self.watermark_image.copy()

        # Scale watermark to fit the smallest dimension of the input image
        smallest_dimension = min(input_image.size)
        scale_factor = smallest_dimension * 0.3
        new_watermark_size = (
            int(watermark.size[0] * scale_factor / smallest_dimension),
            int(watermark.size[1] * scale_factor / smallest_dimension),
        )
        watermark = watermark.resize(new_watermark_size)
        watermark = self._apply_opacity(watermark)

        # Generate random position for the watermark
        random_x = random.randint(0, max(0, input_image.size[0] - new_watermark_size[0]))
        random_y = random.randint(0, max(0, input_image.size[1] - new_watermark_size[1]))
        watermark_position = (random_x, random_y)

        # Create a transparent overlay
        overlay = Image.new("RGBA", input_image.size, (0, 0, 0, 0))
        overlay.paste(watermark, watermark_position, mask=watermark)

        # Blend the input image and the overlay
        blended_image = Image.alpha_composite(input_image, overlay)

        # Convert the final image to RGB and encode as base64
        final_image = blended_image.convert("RGB")
        output_buffer = io.BytesIO()
        final_image.save(output_buffer, format="JPEG")

        mime = magic.Magic(mime=True)

        return WatermarkMessageReply(
            mimetype=mime.from_buffer(output_buffer.getvalue()),
            data=base64.b64encode(output_buffer.getvalue()).decode('utf-8'),
        )
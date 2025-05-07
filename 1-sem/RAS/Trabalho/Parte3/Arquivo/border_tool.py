from PIL import Image, ImageOps
from .border_request_message import BorderParameters

class BorderTool:

    def __init__(self):
        """
        Inicializa o BorderTool.
        """
        pass

    def apply(self, parameters: BorderParameters):
        """
        Adiciona uma borda à imagem de entrada e salva o resultado.

        Args:
            parameters (BorderParameters): Parâmetros para a borda.
        """
        try:
            # Abrir imagem de entrada
            input_image = Image.open(parameters.inputImageURI)

            # Adicionar borda
            bordered_image = ImageOps.expand(
                input_image,
                border=parameters.borderWidth,
                fill=parameters.borderColor
            )

            # Salvar imagem de saída
            bordered_image.save(parameters.outputImageURI)
        except Exception as e:
            raise RuntimeError(f"Erro ao adicionar borda: {str(e)}")
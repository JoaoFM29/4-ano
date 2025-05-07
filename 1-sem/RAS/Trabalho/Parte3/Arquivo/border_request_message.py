from pydantic import BaseModel

from .core.messages.request_message import RequestMessage

class BorderParameters(BaseModel):
    inputImageURI: str
    outputImageURI: str
    borderWidth: int
    borderColor: str

BorderRequestMessage = RequestMessage[BorderParameters]


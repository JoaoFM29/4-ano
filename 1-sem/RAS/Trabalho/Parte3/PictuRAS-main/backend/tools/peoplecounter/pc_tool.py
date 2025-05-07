import base64
import numpy as np # type: ignore
import cv2 # type: ignore
import traceback
from detectron2.engine import DefaultPredictor # type: ignore
from pc_message_reply import PeopleCountingMessageReply
from pc_message_request import PeopleCountingMessageRequest


class PeopleCountingTool:

    def __init__(self, request: PeopleCountingMessageRequest, cfg) -> None:
        self.request = request
        self.cfg = cfg

    def apply(self) -> PeopleCountingMessageReply:

        try:

            # Decode the image from base64
            image_data = base64.b64decode(self.request.getImage())
            np_arr = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            predictor = DefaultPredictor(self.cfg)

            # Perform detection
            outputs = predictor(image)

            # Extract class IDs and count 'person' detections (COCO ID 0)
            class_ids = outputs["instances"].pred_classes.cpu().numpy()
            person_count = str(sum(1 for class_id in class_ids if class_id == 0))

            # Return the count as a reply
            return PeopleCountingMessageReply(
                mimetype='plain/text',
                data=base64.b64encode(person_count.encode('utf-8')).decode('utf-8')
            )

        except Exception:
            traceback.print_exc()
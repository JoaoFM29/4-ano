import base64
import json
import traceback
import numpy as np # type: ignore
import cv2 # type: ignore
from detectron2.engine import DefaultPredictor  # type: ignore
from detectron2.data import MetadataCatalog # type: ignore
from collections import Counter
from oc_message_reply import ObjectCountingMessageReply
from oc_message_request import ObjectCountingMessageRequest

class ObjectCountingTool:

    def __init__(self, request: ObjectCountingMessageRequest, cfg) -> None:
        self.request = request
        self.cfg = cfg

    def apply(self) -> ObjectCountingMessageReply:

        try:

            # Decode the image from base64
            image_data = base64.b64decode(self.request.getImage())
            np_arr = np.frombuffer(image_data, np.uint8)

            image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            # Setup Detectron2 configuration
            # Create a predictor
            predictor = DefaultPredictor(self.cfg)
            # Perform inference

            outputs = predictor(image)
            # Get the class names from Detectron2's COCO metadata
            metadata = MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0])
            class_names = metadata.get("thing_classes", [])

            # Extract detected classes
            detected_classes = outputs["instances"].pred_classes.cpu().numpy()
            detected_class_names = [class_names[i] for i in detected_classes]

            # Count occurrences of each class
            object_counts = dict(Counter(detected_class_names))
            object_counts = json.dumps(object_counts, indent=4)

            # Return the counts as a reply
            return ObjectCountingMessageReply(
                mimetype='plain/text',
                data=base64.b64encode(object_counts.encode('utf-8')).decode('utf-8')
            )

        except Exception:
            traceback.print_exc()
from ultralytics import YOLO
from .detector import Detector


class YoloDetector(Detector):
    # Responsibilities:
    # - Load the AI model from disk
    # - Run inference on the input image
    # - Return the raw YOLO detection results that is going to be clasified

    def __init__(self, config):

        # ai model instances
        self.model = None

        # Detection Settings
        self.model_path = config["path"]
        self.confidence = config["confidence"]
        self.image_size = config["image_size"]

    # class responsible for loading model from designated path
    def load_model(self):

        # The model is loaded only once, calling this again is safe
        if self.model is not None:
            return True

        self.model = YOLO(self.model_path)
        print("model is loading ......")

        return True

    def detect(self, frame):

        # run object detection on current frame
        result = self.model(

            frame,
            conf=self.confidence,
            imgsz=self.image_size,
            verbose=False
        )

        return result

    def get_class_names(self):

        if self.model is None:
            return []

        return list(self.model.names.values())

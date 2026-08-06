from ultralytics import YOLO
from . import settings

class Detector:

    def __init__(self):

        self.model = None

        self.model_path = settings.MODEL_PATH
        self.confidence = settings.CONFIDENCE
        self.image_size = settings.IMAGE_SIZE


    def load_model(self):
        self.model = YOLO(self.model_path)
        print("model is loading ......")
        return True

    def detect(self,frame):

        result = self.model(

            frame,
            conf = self.confidence,
            imgsz = self.image_size,
            verbose = False
        )


        return result
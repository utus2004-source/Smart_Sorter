from ultralytics import YOLO
from . import settings

class Detector:
    # Responsibilities:
    # - Load the AI model from disk
    # - Run inference on the input image
    # - Return the raw YOLO detection results that is going to be clasified

    def __init__(self):

        #ai model  instances 
        self.model = None

        #Detection Settings
        self.model_path = settings.MODEL_PATH
        self.confidence = settings.CONFIDENCE
        self.image_size = settings.IMAGE_SIZE

    #class responsible for loading model from designated path
    def load_model(self):

        self.model = YOLO(self.model_path)
        print("model is loading ......") 

        return True

    def detect(self,frame):

        #run object detection on current frame
        result = self.model(

            frame,
            conf = self.confidence,
            imgsz = self.image_size,
            verbose = False
        )


        return result
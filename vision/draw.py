import cv2
from . import settings


class Draw:
    # This class is rensposible for creating bouding boxes on frame and colors

    def __init__(self):

        self.box_thickned = settings.BOX_THICKNESS
        self.font_scale = settings.FONT_SCALE
        self.text_style = settings.TEXT_STYLE
        self.text_thickness = settings.TEXT_THICKNESS
        self.medium_confidence = settings.MEDIUM_CONFIDENCE
        self.low_confidence = settings.LOW_CONFIDENCE

    #Depending on confidece change color of  annotated_frame and label
    def get_color(self,confidence):

        if confidence < self.low_confidence :

            return(0,0,255) # Red Color
        
        elif confidence <  self.medium_confidence:

            return(0,255,255) # Yellow Color

        else:

            return(0,255,0) # Green Color


    def draw(self, frame, predictions):

        annotated_frame = frame.copy() # copy current fram to adnotate it 

        for prediction in predictions: 

            color = self.get_color(prediction.confidence) # get confidece from previus made list 

            # Image: 640 x 640 pixels
            #
            #  X →
            #       0                         640
            #       ┌───────────────────────────┐
            #     0 │                           │
            #       │       (x1, y1)            │
            #       │          ●──────────●     │
            #       │          │          │     │
            #     Y |          │  OBJECT  │     │
            #       │          │          │     │
            #       │          ●──────────●     │
            #       │                     (x2,y2)
            #       │                           │
            #   640 └───────────────────────────┘
            #
            #
            # x1 = left   edge of bounding box
            # y1 = top    edge of bounding box
            # x2 = right  edge of bounding box
            # y2 = bottom edge of bounding box


            x1 = prediction.x1
            y1 = prediction.y1
            x2 = prediction.x2
            y2 = prediction.y2

            # Creatin the Yolo Rectangle from the 

            cv2.rectangle(
                annotated_frame, # Frame to adnotate
                (x1, y1), # Object cordinates
                (x2, y2),
                (color), # colot ob the object rectangle 
                self.box_thickned# thickness of bounding box
            )

            label = (
                f"{prediction.class_name}"
                f"{prediction.confidence:.0%}"                
            )

            #show the adnotated Frame

            cv2.putText(

                annotated_frame,
                label,
                (prediction.x1, prediction.y1 - 10), # Text position on bounding box
                self.text_style, # Text font 
                self.font_scale, # Text size 
                color, # Text color
                self.text_thickness  # Text thickness
            )

        return annotated_frame
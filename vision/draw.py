import cv2


class Draw:


    #Depending on confidece change color of  annotated_frame and label
    def get_color(self,confidence):

        if confidence < 0.5:

            return(0,0,255) # Red Color
        
        elif confidence < 0.8:

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
                2 # thickness of bounding box
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
                cv2.FONT_HERSHEY_SIMPLEX, # Text font 
                0.6, # Text size 
                color, # Text color
                2 # Text thickness
            )

        return annotated_frame
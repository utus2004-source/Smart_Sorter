import cv2


class Drawer:
    # Visualisation only.
    # Draws bounding boxes, class names, confidence and the ROI so that
    # the camera and the model can be debugged. It never takes decisions
    # and never influences the logical pipeline.
    # It can be switched off completely on a Raspberry Pi.

    def __init__(self, display_config, roi_config):

        self.enabled = display_config["enabled"]
        self.window_name = display_config["window_name"]

        # box configuration and confidence configuration
        self.box_thickness = display_config["box_thickness"]
        self.font_scale = display_config["font_scale"]
        self.text_thickness = display_config["text_thickness"]
        self.low_confidence = display_config["low_confidence"]
        self.medium_confidence = display_config["medium_confidence"]

        # cv2 font constant, this is not a tuning parameter so it stays here
        self.text_style = cv2.FONT_HERSHEY_SIMPLEX

        self.roi = roi_config

    # Depending on confidence change color of annotated_frame and label
    def get_color(self, confidence):

        if confidence < self.low_confidence:

            return (0, 0, 255)  # Red Color

        elif confidence < self.medium_confidence:

            return (0, 255, 255)  # Yellow Color

        else:

            return (0, 255, 0)  # Green Color

    def draw(self, frame, predictions):

        annotated_frame = frame.copy()  # copy current frame to annotate it

        # Draw the region of interest so it can be adjusted while looking at the image
        cv2.rectangle(
            annotated_frame,
            (self.roi["x1"], self.roi["y1"]),
            (self.roi["x2"], self.roi["y2"]),
            (255, 0, 0),  # Blue Color
            self.box_thickness
        )

        for prediction in predictions:

            color = self.get_color(prediction.confidence)  # get confidence from previously made list

            # Image: 640 x 640 pixels
            #
            #  X -->
            #       0                         640
            #       +---------------------------+
            #     0 |                           |
            #       |       (x1, y1)            |
            #       |          *----------*     |
            #       |          |          |     |
            #     Y |          |  OBJECT  |     |
            #       |          |          |     |
            #       |          *----------*     |
            #       |                     (x2,y2)
            #       |                           |
            #   640 +---------------------------+
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

            # Creating the Yolo Rectangle

            cv2.rectangle(
                annotated_frame,  # Frame to annotate
                (x1, y1),  # Object cordinates
                (x2, y2),
                (color),  # color of the object rectangle
                self.box_thickness  # thickness of bounding box
            )

            label = (
                f"{prediction.class_name} "
                f"{prediction.confidence:.0%}"
            )

            # show the annotated Frame

            cv2.putText(

                annotated_frame,
                label,
                (prediction.x1, prediction.y1 - 10),  # Text position on bounding box
                self.text_style,  # Text font
                self.font_scale,  # Text size
                color,  # Text color
                self.text_thickness  # Text thickness
            )

        return annotated_frame

    def show(self, frame, predictions):

        # Nothing is displayed when the display is switched off
        if not self.enabled:
            return

        annotated_frame = self.draw(frame, predictions)

        # show camera image with boxes
        cv2.imshow(self.window_name, annotated_frame)

    def should_quit(self):

        # turn off camera if q is pressed
        if not self.enabled:
            return False

        return cv2.waitKey(1) & 0xFF == ord("q")

    def close(self):

        if self.enabled:
            cv2.destroyAllWindows()

from .prediction import Prediction


class PredictionParser:
    # Border between the concrete model and the rest of the system.
    # Its responsibilities are:
    # - Read the raw YOLO results
    # - Extract the required detection information
    # - Create Prediction objects
    # - Return a list of parsed detections

    def parse(self, results):
        # Convert raw YOLO results into Prediction objects
        detections = []

        # Get all detected bounding boxes from YOLO
        boxes = results[0].boxes

        # Process each detected object
        for box in boxes:

            x1, y1, x2, y2 = box.xyxy[0]  # Box cordinates
            confidence = float(box.conf[0])  # Confidence score
            class_id = int(box.cls[0])  # Current class
            class_name = results[0].names[class_id]  # Convert class ID into readable class

            # Create a prediction object
            detection = Prediction(
                class_id,
                class_name,
                confidence,
                x1,
                y1,
                x2,
                y2
            )

            # add the prediction object to list
            detections.append(detection)

        return detections

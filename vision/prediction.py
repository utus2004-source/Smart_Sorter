

class Prediction :

    def __init__(self,class_name,confidence,x1,y1,x2,y2):

        self.class_name = class_name
        self.confidence = confidence

        self.x1 = int(x1)
        self.y1 = int(y1)
        self.x2 = int(x2)
        self.y2 = int(y2)

class PredictionParser:

    def parse(self, results):

        detections = []

        boxes = results[0].boxes

        for box in boxes:

            x1, y1, x2, y2 = box.xyxy[0]
            confidence = float(box.conf[0])
            class_id = int(box.cls[0])
            class_name = results[0].names[class_id]

            detection = Prediction(
                class_name,
                confidence,
                x1,
                y1,
                x2,
                y2
            )

            detections.append(detection)

        return detections
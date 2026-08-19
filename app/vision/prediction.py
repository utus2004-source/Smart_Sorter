class Prediction:
    # Our own standard detection format.
    # Its responsibilities are:
    # - Store the detected object's class id and class name.
    # - Store the confidence score.
    # - Store the bounding box coordinates.

    # Storing information about one detection
    def __init__(self, class_id, class_name, confidence, x1, y1, x2, y2):

        self.class_id = class_id
        self.class_name = class_name
        self.confidence = confidence

        self.x1 = int(x1)
        self.y1 = int(y1)
        self.x2 = int(x2)
        self.y2 = int(y2)

    def center(self):
        # Center point of the bounding box
        return (self.x1 + self.x2) // 2, (self.y1 + self.y2) // 2

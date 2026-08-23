class Decision:
    # Smart Bin logic.
    # Takes stable detections and returns the bin number the system
    # Prediction[] -> bin number or None

    def __init__(self, classes):

        # Class name -> bin number, loaded from classes.yaml
        self.classes = classes

    def decide(self, predictions):

        if not predictions:
            return None

        # Stabilization returns detections of one class only,
        # so the first one is enough to read the class name
        class_name = predictions[0].class_name

        return self.classes.get(class_name)

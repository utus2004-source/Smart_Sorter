class Detector:
    # Interface for every detector implementation.
    # is running behind this interface.

    def load_model(self):
        raise NotImplementedError

    def detect(self, frame):
        raise NotImplementedError

    def get_class_names(self):
        # Class names stored inside the model file
        raise NotImplementedError

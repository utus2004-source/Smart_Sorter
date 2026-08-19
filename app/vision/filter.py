class ROIFilter:
    # Spatial filter.
    # Answers one question: is the detected object inside the area
    # where the system should take it into account?
    # Prediction[] -> Prediction[]

    def __init__(self, config):

        self.x1 = config["x1"]
        self.y1 = config["y1"]
        self.x2 = config["x2"]
        self.y2 = config["y2"]

    def contains(self, prediction):

        # A detection belongs to the ROI when its center point is inside it
        center_x, center_y = prediction.center()

        return (
            self.x1 <= center_x <= self.x2
            and self.y1 <= center_y <= self.y2
        )

    def filter(self, predictions):

        filtered_predictions = []

        for prediction in predictions:

            if self.contains(prediction):
                filtered_predictions.append(prediction)

        return filtered_predictions


class DecisionFilter:
    # Second, independent filter.
    # It does not recognise anything, it only answers:
    # should this ready decision be sent to the ESP32 right now?
    # decision -> decision or None

    def __init__(self, config):

        self.cooldown_frames = config["cooldown_frames"]
        self.send_only_on_change = config["send_only_on_change"]

        # Last decision that was actually let through
        self.last_sent = None

        # Frames counted since the last send
        self.frames_since_send = 0

    def filter(self, decision):

        self.frames_since_send += 1

        # Nothing to send
        if decision is None:
            return None

        # Block sending the same decision again
        if self.send_only_on_change and decision == self.last_sent:
            return None

        # Block sending a command in every frame
        if self.frames_since_send < self.cooldown_frames:
            return None

        self.last_sent = decision
        self.frames_since_send = 0

        return decision

from . import settings

class PredictionStabilizier:

    def __init__(self):

        self.history = []
        self.max_history = settings.STABILIZATION_FRAMES
        self.threshold = settings.STABILIZATION_THRESHOLD

    def update(self,predictions):

        if not predictions :
            return  None


        best_prediction = max(
            predictions,
            key=lambda prediction: prediction.confidence
        )

        self.history.append(best_prediction.class_name)

        # Keep only the last N frames
        if len(self.history) > self.max_history:
            self.history.pop(0)

        # Count how many times each class appeared
        class_counts = {}

        for class_name in self.history:

            if class_name not in class_counts:
                class_counts[class_name] = 0

            class_counts[class_name] += 1

        # Find the most common class
        stable_class = max(
            class_counts,
            key=class_counts.get
        )

        count = class_counts[stable_class]

        # Check if the class is stable enough
        if count / len(self.history) >= self.threshold:

            return stable_class

        return None
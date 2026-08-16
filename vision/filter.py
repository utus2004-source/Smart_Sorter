from . import settings


class PredictionFilter:

    #main resbonsibility is too filter low confident class

    def __init__(self):
        self.threshold = settings.CONFIDENCE_THRESHOLD

    def filter(self, predictions):

        filtered_predictions = []

        for prediction in predictions:

            if prediction.confidence >= self.threshold:
                filtered_predictions.append(prediction)

        return filtered_predictions
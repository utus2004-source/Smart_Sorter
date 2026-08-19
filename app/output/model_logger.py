class ModelLogger:
    # Debug logger used to check what the model sees.
    # Useful while adjusting the camera or testing a new model.

    def log(self, predictions):

        if predictions:

            print("\n========================== Yolo DETECTION =============================")
            for prediction in predictions:
                print(
                    f"Class: {prediction.class_name} | "
                    f"Confidence: {prediction.confidence:.2%} | "
                    f"Position: "
                    f"({prediction.x1}, {prediction.y1}) "
                    f"-> "
                    f"({prediction.x2}, {prediction.y2})"
                )
            print("=========================================================================\n")
        else:
            # if nothing print nothing
            print("Nothing detected")

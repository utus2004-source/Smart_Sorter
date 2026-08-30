from app.vision.stabilization import PredictionStabilizer
from app.vision.prediction import Prediction


CONFIG = {"frames": 5, "threshold": 0.6}


def make_prediction(class_name, confidence=0.9):
    return Prediction(0, class_name, confidence, 0, 0, 10, 10)


def test_empty_input_returns_empty():

    assert PredictionStabilizer(CONFIG).update([]) == []


def test_repeated_class_becomes_stable():

    stabilizer = PredictionStabilizer(CONFIG)

    for _ in range(4):
        stabilizer.update([make_prediction("Plastic")])

    result = stabilizer.update([make_prediction("Plastic")])

    assert len(result) == 1
    assert result[0].class_name == "Plastic"


def test_single_wrong_frame_is_ignored():

    stabilizer = PredictionStabilizer(CONFIG)

    for _ in range(4):
        stabilizer.update([make_prediction("Plastic")])

    # One wrong frame, the history is still dominated by Plastic
    result = stabilizer.update([make_prediction("Glass")])

    assert result == []


def test_highest_confidence_wins_in_one_frame():

    stabilizer = PredictionStabilizer({"frames": 1, "threshold": 0.6})

    result = stabilizer.update([
        make_prediction("Glass", 0.4),
        make_prediction("Plastic", 0.95)
    ])

    assert result[0].class_name == "Plastic"

def test_empty_frames_outvote_the_old_class():

    stabilizer = PredictionStabilizer(CONFIG)

    for _ in range(5):
        stabilizer.update([make_prediction("Plastic")])

    # The object left the drop zone
    for _ in range(3):
        stabilizer.update([])

    # Three empty frames out of five - no decision any more
    assert stabilizer.update([make_prediction("Plastic")]) == []




    stabilizer = PredictionStabilizer(CONFIG)

    for _ in range(5):
        stabilizer.update([make_prediction("Plastic")])

    for _ in range(50):
        stabilizer.update([])

    # A single frame must not be enough to decide again
    assert stabilizer.update([make_prediction("Plastic")]) == []

from app.decision.decision import Decision
from app.vision.prediction import Prediction


CLASSES = {"Glass": 1, "Aluminium_Metal": 2, "Plastic": 3}


def make_prediction(class_name):
    return Prediction(0, class_name, 0.9, 0, 0, 10, 10)


def test_known_class_returns_bin_number():

    decision = Decision(CLASSES)

    assert decision.decide([make_prediction("Glass")]) == 1
    assert decision.decide([make_prediction("Aluminium_Metal")]) == 2
    assert decision.decide([make_prediction("Plastic")]) == 3


def test_unknown_class_returns_none():

    assert Decision(CLASSES).decide([make_prediction("Paper")]) is None


def test_no_predictions_returns_none():

    assert Decision(CLASSES).decide([]) is None

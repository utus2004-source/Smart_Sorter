from app.vision.filter import ROIFilter, DecisionFilter
from app.vision.prediction import Prediction


ROI_CONFIG = {"x1": 100, "y1": 100, "x2": 500, "y2": 500}


def make_prediction(x1, y1, x2, y2):
    return Prediction(0, "Plastic", 0.9, x1, y1, x2, y2)


def test_roi_keeps_object_inside():

    inside = make_prediction(200, 200, 300, 300)

    assert ROIFilter(ROI_CONFIG).filter([inside]) == [inside]


def test_roi_rejects_object_outside():

    outside = make_prediction(600, 600, 620, 620)

    assert ROIFilter(ROI_CONFIG).filter([outside]) == []


def test_decision_filter_blocks_repeated_decision():

    config = {"cooldown_frames": 1, "send_only_on_change": True}
    decision_filter = DecisionFilter(config)

    assert decision_filter.filter(3) == 3
    assert decision_filter.filter(3) is None


def test_decision_filter_respects_cooldown():

    config = {"cooldown_frames": 5, "send_only_on_change": False}
    decision_filter = DecisionFilter(config)

    # The first four frames are still inside the cooldown
    for _ in range(4):
        assert decision_filter.filter(3) is None

    # The fifth frame reaches the cooldown
    assert decision_filter.filter(3) == 3


def test_decision_filter_passes_none():

    config = {"cooldown_frames": 1, "send_only_on_change": True}

    assert DecisionFilter(config).filter(None) is None

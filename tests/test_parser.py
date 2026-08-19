from app.vision.parser import PredictionParser


class FakeBox:
    # Minimal stand in for one YOLO box

    def __init__(self, xyxy, conf, cls):
        self.xyxy = [xyxy]
        self.conf = [conf]
        self.cls = [cls]


class FakeResult:
    # Minimal stand in for one YOLO result

    def __init__(self, boxes, names):
        self.boxes = boxes
        self.names = names


def test_parse_returns_predictions():

    results = [FakeResult(
        boxes=[FakeBox((10.0, 20.0, 30.0, 40.0), 0.9, 2)],
        names={2: "Plastic"}
    )]

    predictions = PredictionParser().parse(results)

    assert len(predictions) == 1
    assert predictions[0].class_id == 2
    assert predictions[0].class_name == "Plastic"
    assert predictions[0].confidence == 0.9
    assert (predictions[0].x1, predictions[0].y1) == (10, 20)
    assert (predictions[0].x2, predictions[0].y2) == (30, 40)


def test_parse_without_detections():

    results = [FakeResult(boxes=[], names={})]

    assert PredictionParser().parse(results) == []

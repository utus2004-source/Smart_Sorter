from app.config import Config
from app.camera.opencv_camera import OpenCVCamera
from app.vision.yolo_detector import YoloDetector
from app.vision.parser import PredictionParser
from app.vision.filter import ROIFilter, DecisionFilter
from app.vision.stabilization import PredictionStabilizer
from app.decision.decision import Decision
from app.output.drawer import Drawer
from app.output.model_logger import ModelLogger
from app.communication.serial_esp32 import SerialESP32
from app.pipeline.vision_pipeline import VisionPipeline


def check_classes(detector, classes):
    # The class names live inside the model file, classes.yaml only maps them
    # to bin numbers. If they stop matching, the system would silently return
    # no decision at all, so a warning is printed here.

    model_classes = detector.get_class_names()

    missing = [
        class_name
        for class_name in model_classes
        if class_name not in classes
    ]

    if missing:
        print(f"WARNING: classes.yaml has no entry for: {missing}")


def main():

    # load configuration
    config = Config()

    # create the components
    camera = OpenCVCamera(config.camera)
    detector = YoloDetector(config.model)
    parser = PredictionParser()
    roi_filter = ROIFilter(config.roi)
    stabilization = PredictionStabilizer(config.stabilization)
    decision = Decision(config.classes)
    decision_filter = DecisionFilter(config.decision_filter)
    communication = SerialESP32(config.communication)
    drawer = Drawer(config.display, config.roi)
    logger = ModelLogger()

    # load the model once so the class names can be verified before starting
    if not detector.load_model():
        print("Could not load AI model.")
        return

    check_classes(detector, config.classes)

    # connect them to the pipeline
    pipeline = VisionPipeline(
        camera,
        detector,
        parser,
        roi_filter,
        stabilization,
        decision,
        decision_filter,
        communication,
        drawer,
        logger,
        config.display["debug_log_every"]
    )

    # run the pipeline
    pipeline.run()


if __name__ == "__main__":
    main()

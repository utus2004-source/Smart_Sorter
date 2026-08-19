class VisionPipeline:
    # Orchestrator.
    # It only defines the order of the steps and works on the interfaces,
    # it does not implement camera, model, ROI, stabilization,
    # decision, communication or drawing logic.

    def __init__(
        self,
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
        debug_log_every
    ):

        self.camera = camera
        self.detector = detector
        self.parser = parser
        self.roi_filter = roi_filter
        self.stabilization = stabilization
        self.decision = decision
        self.decision_filter = decision_filter
        self.communication = communication
        self.drawer = drawer
        self.logger = logger
        self.debug_log_every = debug_log_every

    def run(self):

        # open camera
        if not self.camera.open():
            print("Could not open camera.")
            return

        # show camera information
        self.camera.print_info()

        # could not load model
        if not self.detector.load_model():
            print("Could not load AI model.")
            return

        self.communication.connect()

        # counting frames from camera
        frame_count = 0

        # Open and get frames from camera
        while True:

            ret, frame = self.camera.get_frame()

            if not ret:
                print("Camera disconnected.")
                break

            # load model results
            results = self.detector.detect(frame)
            predictions = self.parser.parse(results)

            # logical pipeline
            predictions_in_roi = self.roi_filter.filter(predictions)
            stable_predictions = self.stabilization.update(predictions_in_roi)
            decision_result = self.decision.decide(stable_predictions)
            command = self.decision_filter.filter(decision_result)

            if command is not None:
                self.communication.send(command)

            # Show information about what yolo sees.
            # All detections are passed here, also the ones rejected by the ROI,
            # so that a wrong ROI can be spotted on the image.
            if frame_count % self.debug_log_every == 0:
                self.logger.log(predictions)
                print(decision_result)

            self.drawer.show(frame, predictions)

            if self.drawer.should_quit():
                break

            # counting frames
            frame_count += 1

        self.camera.release()
        self.communication.close()
        self.drawer.close()

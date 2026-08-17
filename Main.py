from modelTest.modelTest import ModelOuput
from camera.camera import Camera
from vision.detector import Detector
from vision.prediction import PredictionParser
from vision.draw import Draw
from vision.filter import PredictionFilter
from vision.stabilization import PredictionStabilizier
from control.decision import Decision
import cv2


def main():

    #load classes
    camera = Camera()
    detector = Detector()
    parser = PredictionParser()
    drawer = Draw()
    stabilization = PredictionStabilizier()
    decision = Decision()
    model_output = ModelOuput()


    # open camera 
    if not camera.open():
        print("Could not open camera.")
        return

    # show camera information
    camera.print_info()

    #could not load model 
    if not detector.load_model():
        print("Could not load AI model.")
        return

    #couting frames from camera
    frame_count = 0

    # Open and get frames from camera
    while True:

        ret, frame = camera.get_frame()

        if not ret:
            print("Camera disconnected.")
            break

        #load model results 
        results = detector.detect(frame)
        predictions = parser.parse(results)
        stable_class = stabilization.update(predictions)
        decision_result = decision.decide(stable_class)
        
        annotated_frame = drawer.draw(frame,predictions)

        #Show information about what yolo sees
        if frame_count %30 == 0:
            model_output.ModelCheck(predictions)
            print(decision_result)
        
        #show camera image with boxes
        cv2.imshow("Smart Bin Camera",annotated_frame)


        #turn off camera if q is pressed 
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        #couting frames

        frame_count +=1

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

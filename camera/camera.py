import cv2
from . import settings


class Camera:
    # Responsibilities:
    # - Open the camera
    # - Configure camera settings
    # - Capture video frames
    # - Provide camera status
    # - Release camera resources

    def __init__(self):

        # Camera stream object
        self.stream = None

        # Camera configuration
        self.camera_id = settings.CAMERA_ID
        self.width = settings.FRAME_WIDTH
        self.height = settings.FRAME_HEIGHT
        self.fps = settings.FPS

    def open(self):
        #open camera stream 
        self.stream = cv2.VideoCapture(self.camera_id)

        # If camera not opened return false
        if not self.stream.isOpened():
            return False

        #load configuration if opened
        self.configure()

        return True

    def configure(self):

        # If camera not opened return false
        if self.stream is None:
            return

        # set camera confg
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.stream.set(cv2.CAP_PROP_FPS, self.fps)

    def get_frame(self):

        #capture single frame from camera
        return self.stream.read()

    def is_open(self):
        # Check whether the camera is currently open
        return self.stream is not None and self.stream.isOpened()

    def print_info(self):

        #show camera configuration and information
        print("------ Camera Info ------")
        print(f"Camera ID : {self.camera_id}")
        print(f"Resolution: {self.width} x {self.height}")
        print(f"FPS       : {self.fps}")
        print("-------------------------")

    def release(self):
        # close camera 

        if self.stream is not None:
            self.stream.release()
import cv2
from . import settings


class Camera:

    def __init__(self):

        self.stream = None

        self.camera_id = settings.CAMERA_ID
        self.width = settings.FRAME_WIDTH
        self.height = settings.FRAME_HEIGHT
        self.fps = settings.FPS

    def open(self):

        self.stream = cv2.VideoCapture(self.camera_id)

        # If camera not opened return false
        if not self.stream.isOpened():
            return False

        #load configuration if opened
        self.configure()

        return True

    def configure(self):

        if self.stream is None:
            return

        # Camera confg
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.stream.set(cv2.CAP_PROP_FPS, self.fps)

    def get_frame(self):

        return self.stream.read()

    def is_open(self):

        return self.stream is not None and self.stream.isOpened()

    def print_info(self):

        #show camera configuration
        
        print("------ Camera Info ------")
        print(f"Camera ID : {self.camera_id}")
        print(f"Resolution: {self.width} x {self.height}")
        print(f"FPS       : {self.fps}")
        print("-------------------------")

    def release(self):
        # close camera 

        if self.stream is not None:
            self.stream.release()
# 카메라 모듈(CSI, libcamera)과 USB 카메라를 똑같이 쓰기 위한 도우미
# 라즈베리파이 카메라 모듈은 cv2.VideoCapture(0, cv2.CAP_V4L)로 프레임을 읽을 수 없어서
# Picamera2로 촬영하되, cv2.VideoCapture와 같은 방식(read, grab, set, get, release)으로 쓸 수 있게 한다.
import cv2

class PiCamera:
    def __init__(self):
        from picamera2 import Picamera2
        self.picam = Picamera2()
        self.width, self.height, self.fps = 640, 480, None
        self.started = False

    def _start(self):
        if not self.started:
            config = self.picam.create_video_configuration(
                main={"size": (self.width, self.height), "format": "RGB888"}) # RGB888은 OpenCV의 BGR 순서
            if self.fps:
                config["controls"] = {"FrameRate": self.fps}
            self.picam.configure(config)
            self.picam.start()
            self.started = True

    def isOpened(self):
        return True

    def set(self, prop, value):
        if prop == cv2.CAP_PROP_FRAME_WIDTH:
            self.width = int(value)
        elif prop == cv2.CAP_PROP_FRAME_HEIGHT:
            self.height = int(value)
        elif prop == cv2.CAP_PROP_FPS:
            self.fps = value
        return True # BUFFERSIZE 등: Picamera2는 항상 가장 최근 프레임을 돌려주므로 필요 없음

    def get(self, prop):
        if prop == cv2.CAP_PROP_FRAME_WIDTH:
            return self.width
        if prop == cv2.CAP_PROP_FRAME_HEIGHT:
            return self.height
        if prop == cv2.CAP_PROP_BUFFERSIZE:
            return 1
        return 0

    def grab(self):
        self._start()
        return True

    def read(self):
        self._start()
        frame = self.picam.capture_array()
        return frame is not None, frame

    def release(self):
        if self.started:
            self.picam.stop()
        self.picam.close()

def open():
    """카메라 모듈이 있으면 Picamera2, 없으면 PDF와 같이 cv2.VideoCapture(0, cv2.CAP_V4L) 사용"""
    try:
        from picamera2 import Picamera2
        if Picamera2.global_camera_info():
            return PiCamera()
    except ImportError:
        pass
    return cv2.VideoCapture(0, cv2.CAP_V4L)

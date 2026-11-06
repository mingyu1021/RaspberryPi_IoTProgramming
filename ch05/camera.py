# 라즈베리파이 카메라 제어 모듈 (PDF의 camera.py)
# 사용 순서: camera.init() 호출 → camera.read() 반복 → camera.release() 호출
# 라즈베리파이 카메라 모듈(CSI, libcamera)은 cv2.VideoCapture(0)로 프레임을 읽을 수 없어서
# 카메라 모듈이 있으면 Picamera2로 촬영하고, 없으면(USB 카메라) PDF와 같이 cv2.VideoCapture를 쓴다.
import cv2

_camera = None # OpenCV의 VideoCapture 객체 참조 (카메라 모듈이면 Picamera2 객체)
_is_picam = False

def _open_picam(width, height):
    try:
        from picamera2 import Picamera2
    except ImportError:
        return None
    if not Picamera2.global_camera_info(): # 연결된 카메라 모듈 없음
        return None
    picam = Picamera2()
    config = picam.create_video_configuration(
        main={"size": (width, height), "format": "RGB888"}) # RGB888은 OpenCV의 BGR 순서
    picam.configure(config)
    picam.start()
    return picam

def init(camera_id=0, width=640, height=480, buffer_size=1):
    global _camera, _is_picam # 전역 변수 _camera 사용 선언

    if _camera is not None: # 카메라가 이미 오픈 되어 있으면
        release() # 기존 카메라 해제

    _camera = _open_picam(width, height) # 카메라 모듈 먼저 시도
    if _camera is not None:
        _is_picam = True # Picamera2는 항상 가장 최근 프레임을 주므로 버퍼 설정 불필요
        return

    _is_picam = False
    _camera = cv2.VideoCapture(camera_id) # 카메라 열기
    try:
        _camera.set(cv2.CAP_PROP_BUFFERSIZE, buffer_size) # 버퍼 크기 설정
    except Exception:
        pass # 버퍼 크기 설정 미지원 시 무시
    _camera.set(cv2.CAP_PROP_FRAME_WIDTH, width) # 프레임 가로 크기 설정
    _camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height) # 프레임 세로 크기 설정

    if not _camera.isOpened(): # 카메라 열기 실패 시
        _camera = None # 전역 변수 초기화
        raise RuntimeError(f"카메라 열기 실패: camera_id={camera_id}")

def read():
    if _camera is None: # 카메라 미초기화 시
        return None # None 반환
    if _is_picam:
        return _camera.capture_array() # 프레임 1장 읽기
    ok, frame = _camera.read() # 프레임 1장 읽기
    return frame if ok else None # 실패 시 None 반환

def release():
    global _camera # 전역 변수 사용 선언
    if _camera is not None: # 카메라가 열려있으면
        if _is_picam:
            _camera.stop()
            _camera.close()
        else:
            _camera.release() # 카메라 자원 해제
        _camera = None # 전역 변수 초기화

import os
import threading
import time
import cv2
import picam
# 예제 4-6(얼굴 인식)에 사물 인식을 더한 프로그램
# 사물 인식: OpenCV DNN + YOLOv4-tiny (COCO 데이터셋 80종: person, cup, cell phone 등)
# 얼굴은 노란색, 사물은 초록색 사각형으로 표시한다. ESC 키를 누르면 종료
# 속도 개선: 인식은 별도 스레드에서 하고, 화면은 카메라 속도대로 계속 갱신한다.

# 카메라가 옆으로 달려 있으면 영상을 돌려서 인식한다.
# None(회전 안 함), cv2.ROTATE_90_CLOCKWISE, cv2.ROTATE_90_COUNTERCLOCKWISE, cv2.ROTATE_180 중 선택
ROTATE = cv2.ROTATE_90_COUNTERCLOCKWISE
# 화면에 보여줄 때 영상을 키우는 배율 (1이면 원래 크기)
DISPLAY_SCALE = 1.5
# YOLO 입력 크기 (32의 배수). 작을수록 빠르고, 클수록 작은 물체를 잘 찾는다. (416: 약 1초, 320: 약 0.5초)
YOLO_SIZE = 320

# 얼굴 검출 객체 생성 (예제 4-6과 동일)
path = './haar-cascade-files-master/haarcascade_frontalface_default.xml'
if not os.path.exists(path):
    path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
classifier = cv2.CascadeClassifier(path)

# 사물 검출 모델 생성
net = cv2.dnn.readNetFromDarknet('./yolo/yolov4-tiny.cfg', './yolo/yolov4-tiny.weights')
model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(YOLO_SIZE, YOLO_SIZE), scale=1/255, swapRB=True)
with open('./yolo/coco.names') as f:
    names = [line.strip() for line in f]

# 카메라 객체 생성
camera = picam.open() # PDF: cv2.VideoCapture(0, cv2.CAP_V4L)
camera.set(cv2.CAP_PROP_BUFFERSIZE, 1) # 버퍼 크기를 1로 설정

# 화면 스레드와 인식 스레드가 함께 쓰는 데이터
latest_frame = None              # 카메라에서 가장 최근에 읽은 프레임
objects, faces = [], []          # 가장 최근 인식 결과
detect_fps = 0.0
lock = threading.Lock()
running = True

def detect_loop():
    """가장 최근 프레임으로 사물과 얼굴을 계속 인식한다."""
    global objects, faces, detect_fps
    while running:
        with lock:
            frame = latest_frame
        if frame is None:
            time.sleep(0.01)
            continue
        start = time.time()
        # 사물 인식: 신뢰도 0.4 이상인 것만
        class_ids, scores, boxes = model.detect(frame, confThreshold=0.4, nmsThreshold=0.4)
        found_objects = [("%s %.0f%%" % (names[int(c)], s * 100), b) for c, s, b in zip(class_ids, scores, boxes)]
        # 얼굴 인식: 1.2배씩 축소하며 찾고, 60x60보다 작은 얼굴은 건너뛰어 속도를 높인다
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        found_faces = classifier.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(60, 60))
        with lock:
            objects, faces = found_objects, found_faces
            detect_fps = 1 / (time.time() - start)

thread = threading.Thread(target=detect_loop, daemon=True)
thread.start()

cv2.namedWindow('preview')
cv2.moveWindow('preview', 600, 0) # 창이 화면 아래로 잘리지 않게 위쪽에 배치

prev = time.time()
while True:
    camera.grab() # 버퍼에 저장된 카메라의 이전 프레임 제거
    ret, image = camera.read()
    if ret == False:
        continue
    if ROTATE is not None:
        image = cv2.rotate(image, ROTATE) # 카메라 방향에 맞게 영상 회전
    with lock:
        latest_frame = image.copy() # 인식 스레드에 최신 프레임 전달
        cur_objects, cur_faces, cur_detect_fps = objects, faces, detect_fps

    # 가장 최근 인식 결과를 그린다. 사물은 초록색, 얼굴은 노란색(0, 255, 255)
    for label, (x, y, w, h) in cur_objects:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, label, (x, max(y - 8, 15)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    for x, y, w, h in cur_faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 255), 4)

    # 화면 FPS와 인식 FPS 표시
    now = time.time()
    cv2.putText(image, "Video %.1f fps / Detect %.1f fps" % (1 / (now - prev), cur_detect_fps),
                (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    prev = now

    if DISPLAY_SCALE != 1: # 인식은 원래 크기로 하고, 보여줄 때만 키운다
        image = cv2.resize(image, None, fx=DISPLAY_SCALE, fy=DISPLAY_SCALE)
    cv2.imshow('preview', image) # 이미지를 preview 이름의 창에 출력
    if cv2.waitKey(1) == 27: # ESC 키(키 값27)이면 프로그램 종료
        break

running = False
thread.join()
camera.release()
cv2.destroyAllWindows()

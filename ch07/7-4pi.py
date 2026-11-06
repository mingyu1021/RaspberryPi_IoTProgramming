import cv2
import paho.mqtt.client as mqtt

broker_ip = "localhost"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(broker_ip, 1883) # 1883 포트로 mosquitto에 접속
client.loop_start() # 메시지 루프를 실행하는 스레드 생성

# 라즈베리파이 카메라 모듈(CSI)은 libcamera를 사용하므로 Picamera2로 촬영한다.
# Picamera2가 없으면 PDF와 같이 OpenCV(V4L)로 촬영한다. (USB 웹캠 등)
try:
    from picamera2 import Picamera2
    picam = Picamera2()
    # 촬영한 사진 크기를 640x480으로 설정. RGB888은 메모리상 BGR 순서라 OpenCV와 호환
    picam.configure(picam.create_still_configuration(main={"size": (640, 480), "format": "RGB888"}))
    picam.start()
    camera = None
except (ImportError, IndexError, RuntimeError):
    picam = None
    # 카메라 객체를 생성하고 촬영한 사진 크기를 640x480으로 설정
    camera = cv2.VideoCapture(0, cv2.CAP_V4L)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    # 프레임을 임시 저장할 버퍼 개수를 1로 설정
    buffer_size = 1
    camera.set(cv2.CAP_PROP_BUFFERSIZE, buffer_size)

while True:
    key = input("사진촬영계속?(종료는 stop 입력)>>")
    if key == "stop": # stop이 입력되면 while 문을 벗어남
        break
    if picam is not None:
        frame = picam.capture_array() # 사진 촬영
        ret = frame is not None
    else:
        # 버퍼에 저장된 모든 프레임을 버리고 새 프레임 읽기
        for i in range(buffer_size + 1):
            ret, frame = camera.read()
    if not ret:
        print("카메라에서 사진을 읽지 못했습니다.")
        continue

    im_bytes = cv2.imencode('.jpg', frame)[1].tobytes() # 바이트 배열로 저장
    client.publish("jpeg", im_bytes, qos=0) # 이미지 전송
    print("이미지 전송 (%d 바이트)" % len(im_bytes))

if picam is not None:
    picam.stop() # 카메라 사용 끝내기
else:
    camera.release() # 카메라 사용 끝내기
client.loop_stop() # 메시지 루프를 실행하는 스레드 종료
client.disconnect()

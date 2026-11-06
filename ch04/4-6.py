import os
import cv2
import picam
# 검출 객체를 생성
# PDF대로 내려받은 haar-cascade-files-master가 없으면 OpenCV에 들어 있는 같은 파일을 사용
path = './haar-cascade-files-master/haarcascade_frontalface_default.xml'
if not os.path.exists(path):
    path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
classifier = cv2.CascadeClassifier(path)
# 카메라 객체 생성
camera = picam.open() # PDF: cv2.VideoCapture(0, cv2.CAP_V4L)
camera.set(cv2.CAP_PROP_BUFFERSIZE, 1) # 버퍼 크기를 1로 설정
# ESC 키가 입력될 때까지 카메라로부터 받은 영상을 실시간으로 창에 재생하고,
# 영상 속의 얼굴 부분에 사각형을 실시간으로 그린다.
while True:
    camera.grab() # 버퍼에 저장된 카메라의 이전 프레임 제거
    # 버퍼에서 현재 카메라가 촬영한 프레임 읽기
    ret, image = camera.read()
    if ret == False:
        continue
    # 이미지를 흑백으로 바꾸고 얼굴 탐지
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = classifier.detectMultiScale(image_gray)
    # faces는 배열로, 배열의 각 원소는 탐지된 얼굴의 사각형 정보 [[2, 3, 100, 150], ..., [...]]
    # faces 배열 전체를 반복하여 이미지 위에 모든 사각형을 그린다.
    # 노란색(0, 255, 255) 사각형으로 얼굴 표시
    for x, y, w, h in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 255), 4)
    cv2.imshow('preview', image) # 이미지를 preview 이름의 창에 출력
    if cv2.waitKey(1) == 27: # ESC 키(키 값27)이면 프로그램 종료
        break
camera.release()
cv2.destroyAllWindows()

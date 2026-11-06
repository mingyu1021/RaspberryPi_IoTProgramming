import cv2
import picam
camera = picam.open() # PDF: cv2.VideoCapture(0, cv2.CAP_V4L)
# 프레임 크기를 640×480으로 하고, camera가 카메라로부터 읽어오는 주기(FPS)를
# 10으로 설정
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
camera.set(cv2.CAP_PROP_FPS, 10)

fourcc = cv2.VideoWriter_fourcc(*'DIVX') # 코덱 지정
writer = cv2.VideoWriter("video_4_4.avi", fourcc, 10, (640, 480)) # 10 fps 주기로 저장

while True:
    ret, image = camera.read()
    if ret == True:
        cv2.imshow('preview', image)
        writer.write(image)
    else:
        print('카메라로부터 프레임의 캡처할 수 없습니다.')
        break

    # 1 밀리초 동안 ESC 키 입력을 기다린다.
    if cv2.waitKey(1) == 27: # 입력된 키가 ESC이면 while 반복문을 탈출
        break
writer.release()
camera.release()
cv2.destroyAllWindows()

import cv2
import picam
camera = picam.open() # PDF: cv2.VideoCapture(0, cv2.CAP_V4L)
while True:
    ret, image = camera.read() # 카메라에서 프레임 읽기
    if ret == True:
        cv2.imshow('preview', image) # 프레임을 preview 이름의 창에 출력
    else:
        print('카메라로부터 프레임의 캡처할 수 없습니다.')
        break
    # 1 밀리초 동안 ESC 키 입력을 기다린다.
    if cv2.waitKey(1) == 27: # 입력된 키가 ESC이면 while 반복문을 탈출
        break
camera.release()
cv2.destroyAllWindows()

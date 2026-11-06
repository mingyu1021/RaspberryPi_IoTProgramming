import cv2
import picam
camera = picam.open() # PDF: cv2.VideoCapture(0, cv2.CAP_V4L)
ret, image = camera.read()
if ret == True:
    # OpenCV 함수로 이미지를 파일에 저장
    cv2.imwrite('image_4_2.jpg', image)
else:
    print('카메라로부터 프레임의 캡처할 수 없습니다.')
camera.release()

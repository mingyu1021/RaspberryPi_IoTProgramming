import cv2
import picam
camera = picam.open() # 카메라 객체 생성. PDF: cv2.VideoCapture(0, cv2.CAP_V4L)
camera.set(cv2.CAP_PROP_BUFFERSIZE, 10) # 버퍼 크기를 10으로

def take_picture():
    size = camera.get(cv2.CAP_PROP_BUFFERSIZE) # 버퍼 크기를 읽어온다
    while size > 0: # 버퍼 내에 저장된 모든 프레임을 버린다
        camera.grab() # camera.read()로 해도 됨
        size -= 1
    ret, frame = camera.read() # 버퍼에 있는 현재 프레임을 읽는다.
    return frame if ret == True else None

count = 0
print("OpenCV 로딩 완료")
print("키 입력 준비 완료")
frame = take_picture() # 먼저 한 장의 이미지를 가져옴
while True:
    # 아래 show에서 picture 이름의 창을 만들어야 cv2.waitKey()가 작동함
    if frame is not None:
        cv2.imshow("picture", frame)
    # ESC 키가 입력되면 종료.
    # 다른 키가 입력되면 카메라로부터 이미지를 캡처하여 파일로 저장
    if cv2.waitKey(0) == 27: # 0의 의미는 시간 제약 없이 아무 키 입력 대기
        break
    else:
        frame = take_picture() # 현재 시점에서의 프레임을 가져옴
        count += 1
        file_name = "image_4_5_" + str(count) + ".jpg"
        cv2.imwrite(file_name, frame) # 프레임을 jpg 파일에 저장
        print(file_name, "저장")
camera.release()
cv2.destroyAllWindows()

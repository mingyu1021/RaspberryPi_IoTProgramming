import cv2
from flask import Flask, render_template
import camera # 카메라 모듈, camera.py 임포트

app = Flask(__name__)
camera.init(width=640, height=480) # 카메라 모듈 초기화

@app.route('/cctv')
def cctv():
    image = camera.take_picture(most_recent=True) # 사진 촬영
    if image is None:
        return "<h2>카메라에서 이미지를 읽을 수 없습니다.</h2>"
    cv2.imwrite('./static/cctv.jpg', image) # ./static 디렉터리에 파일로 저장
    return render_template("cctv.html", fname='/static/cctv.jpg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080) # debug=True 사용 시 카메라 중복 초기화 오류

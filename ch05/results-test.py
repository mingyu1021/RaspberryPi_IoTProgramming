# predict() 함수와 results 리스트 활용 사례
# 같은 디렉터리의 frame.jpg로 객체 인식을 하고 결과를 출력한다. (frame.jpg가 없으면 카메라로 한 장 찍어 저장)
import os
import cv2
from ultralytics import YOLO

if not os.path.exists("frame.jpg"):
    import camera
    camera.init(0, 640, 480)
    frame = None
    while frame is None:
        frame = camera.read()
    cv2.imwrite("frame.jpg", frame)
    camera.release()

model = YOLO("yolov8n.pt") # 모델 없으면 인터넷에서 자동 다운로드
results = model.predict(source="frame.jpg", imgsz=640, conf=0.25, device='cpu')

result = results[0]        # 첫 번째 이미지 결과
if result.boxes is None:
    print("인식된 객체 없음")
else:
    print(f"인식 수: {len(result.boxes)}")
    print(f"클래스 목록: {result.names}")

for b in results[0].boxes:
    conf = float(b.conf[0])              # confidence 추출
    if conf < 0.25:                     # 0.25 미만 제외
        continue

    x1, y1, x2, y2 = map(int, b.xyxy[0].tolist()) # 좌표 정수 변환
    cls_idx = int(b.cls[0])                         # 클래스 인덱스
    name = results[0].names.get(cls_idx)          # 클래스 이름 조회

    print(f"{name} ({conf:.2f}) at [{x1},{y1}]-[{x2},{y2}]")

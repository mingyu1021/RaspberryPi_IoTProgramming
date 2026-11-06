import os, sys, time, cv2
from ultralytics import YOLO
import camera

MODEL, CONF, IMGSZ = "yolov8n.pt", 0.25, 640 # 모델, 신뢰도, 이미지 크기
CAM, W, H = 0, 640, 480                 # 카메라 번호, 해상도
start_time, counter = time.time(), 0    # FPS를 위한 초기화

def draw_fps(frame):                           # FPS 화면 표시 함수
  global counter
  counter += 1
  fps = counter / (time.time() - start_time)
  cv2.putText(frame, f"FPS:{fps:.1f}", (10, 30), 0, 0.8, (255, 255, 0), 2)

def draw_detections(frame, result, conf=CONF): # 인식 결과 표시 함수
  if result.boxes is None:
      return frame
  for b in result.boxes:                     # 인식된 객체 순회
      if float(b.conf[0]) < conf:           # 신뢰도 미만 제외
          continue
      x1, y1, x2, y2 = map(int, b.xyxy[0].tolist()) # 박스 좌표 추출
      cls = int(b.cls[0])                         # 클래스 인덱스 추출
      label = f"{result.names.get(cls, cls)} {float(b.conf[0]):.2f}" # 라벨
      cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)       # 박스 그리기
      (tw, th), _ = cv2.getTextSize(label, 0, 0.6, 2)               # 라벨 크기 계산
      y = max(0, y1 - 8)
      cv2.rectangle(frame, (x1, y-th-6), (x1+tw+6, y), (0, 255, 0), -1) # 라벨 배경
      cv2.putText(frame, label, (x1+3, y-5), 0, 0.6, (0, 0, 0), 2)      # 라벨 출력
  return frame

def main():
  model = YOLO(MODEL)              # YOLO 모델 로드
  camera.init(CAM, W, H, buffer_size=1) # 카메라 초기화

  while True:
    frame = camera.read()    # 프레임 읽기
    if frame is None:
        time.sleep(0.05)
        continue

    # 이미지를 YOLO 모델에 입력하여 객체 인식 수행, 결과는 배열로 반환
    results = model.predict(source=frame, imgsz=IMGSZ, conf=CONF, verbose=False)

    vis = draw_detections(frame.copy(), results[0]) # 인식 결과 표시
    draw_fps(vis)                          # FPS 표시
    cv2.imshow("YOLOv8 (q=quit)", vis)             # 화면 출력
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

  camera.release()        # 카메라 해제
  cv2.destroyAllWindows()   # 창 닫기

if __name__ == "__main__":
   main()

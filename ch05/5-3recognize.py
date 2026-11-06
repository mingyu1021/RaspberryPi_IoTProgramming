import os, time
import cv2, numpy as np
from facenet_pytorch import MTCNN, InceptionResnetV1
import camera, face_db

os.environ["QT_QPA_PLATFORM"] = "xcb"

THRESHOLD = 0.65        # 등록자/미등록자 판별 임계값
CAM, W, H = 0, 640, 480 # 카메라 번호 및 해상도

def draw_result(frame, name, score): # 결과 화면 출력
  if name:
     cv2.putText(frame, f"{name} ({score:.2f}). Exit:q", (10, 30),
             cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2) # 성공(초록)
  else:
     cv2.putText(frame, f"UNKNOWN ({score:.2f}). Exit:q", (10, 30),
             cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2) # 실패(빨강)
  return frame

def get_emb(resnet, faces):         # 탐지된 얼굴로부터 임베딩 벡터를 추출하여 리턴
  emb_tensor = resnet(faces[0:1])  # 첫 번째 얼굴 임베딩 추출 (1, 512)
  emb_tensor = emb_tensor.squeeze(0) # (1, 512) 2차원 -> (512) 1차원 변환
  emb = emb_tensor.detach().cpu().numpy()    # numpy 변환
  emb = emb.astype(np.float32)
  emb = emb / (np.linalg.norm(emb) + 1e-9) # 정규화 (1e-9은 0 나눗셈 방지)
  return emb

def main():
  db = face_db.load() # DB 로드
  if not db:
     print("[RECOGNIZE] DB 비어있음. 5-2enroll.py로 먼저 등록하세요.")
     return

  mtcnn = MTCNN(image_size=160, margin=20, keep_all=True, device="cpu")
  resnet = InceptionResnetV1(pretrained="vggface2").eval().to("cpu")
  camera.init(CAM, W, H, buffer_size=1) # 카메라 초기화

  while True:
    frame = camera.read()
    if frame is None:
        time.sleep(0.05)
        continue

    faces = mtcnn(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)) # 얼굴 탐지

    if faces is not None:
        emb = get_emb(resnet, faces)                  # 얼굴 임베딩 추출
        name, score = face_db.match(db, emb, THRESHOLD) # DB에서 매칭
    else:
        name, score = None, -1.0                    # 미탐지
    cv2.imshow("Recognize", draw_result(frame.copy(), name, score))

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    time.sleep(0.05)     # 재시도 대기

  camera.release()       # 카메라 해제
  cv2.destroyAllWindows() # 창 닫기

if __name__ == "__main__":
   main()

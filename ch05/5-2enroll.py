import os, time, argparse
import cv2, numpy as np
from facenet_pytorch import MTCNN, InceptionResnetV1
import camera, face_db

os.environ["QT_QPA_PLATFORM"] = "xcb" # Qt 백엔드를 XCB로 설정
CAM, W, H = 0, 640, 480          # 카메라 번호, 해상도

def draw_result(frame, name, status): # 화면에 이름과 상태 메시지를 출력
  cv2.putText(frame, f"{name} | {status}", (10, 30), 0, 0.6, (255, 255, 255), 2)
  return frame

def get_emb(resnet, faces):        # 탐지된 얼굴로부터 임베딩 벡터를 추출하여 리턴
  emb_tensor = resnet(faces[0:1]) # 첫 번째 얼굴 임베딩 추출 (1, 512)
  emb_tensor = emb_tensor.squeeze(0) # (1, 512) 2차원 -> (512) 1차원 변환
  emb = emb_tensor.detach().cpu().numpy()      # numpy 변환
  emb = emb.astype(np.float32)
  emb = emb / (np.linalg.norm(emb) + 1e-9)      # 정규화 (1e-9은 0 나눗셈 방지)
  return emb

def main():
  ap = argparse.ArgumentParser()      # 명령행 인자 파서 객체 생성
  ap.add_argument("--name", required=True) # --name 인자 등록 (필수 입력)
  args = ap.parse_args()           # 명령행 인자를 args.name에 저장

  mtcnn = MTCNN(image_size=160, margin=20, keep_all=True, device="cpu")
  resnet = InceptionResnetV1(pretrained="vggface2").eval().to("cpu")
  db = face_db.load()
  camera.init(CAM, W, H, buffer_size=1)

  while True:
    frame = camera.read()
    if frame is None:
        time.sleep(0.05)
        continue
    faces = mtcnn(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)) # 얼굴인식
    status = "Face OK! Save:s, Exit:q" if faces is not None else "No Face! Exit:q"
    cv2.imshow("Enroll", draw_result(frame.copy(), args.name, status))
    key = cv2.waitKey(1) & 0xFF         # 사용자 키 입력받음
    if key == ord("q"):
        break
    if faces is None:              # 얼굴 없으면 스킵
        continue
    if key == ord("s"):
        emb = get_emb(resnet, faces) # 얼굴 임베딩 추출
        face_db.add(db, args.name, emb) # DB에 추가
        print(f"[ENROLL] 저장 완료: {args.name}")
        face_db.save(db)            # 얼굴 DB 파일에 저장

  camera.release()                  # 카메라 해제
  cv2.destroyAllWindows()             # 모든 창 닫기

if __name__ == "__main__":
   main()

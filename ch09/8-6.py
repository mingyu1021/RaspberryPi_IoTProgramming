import time
import RPi.GPIO as GPIO

def measureDistance(trig, echo):
  time.sleep(0.2) # 초음파 센서의 준비 시간을 위해 필연적인 200밀리초 지연
  GPIO.output(trig, 1) # trig 핀에 1(High) 출력
  time.sleep(0.01) # 신호 1(High)을 0.01초 동안 유지
  GPIO.output(trig, 0) # trig 핀 신호 High->Low. 초음사 발사 지시

  while(GPIO.input(echo) == 0): # echo 핀 값이 0->1로 바뀔 때까지 루프
    pass

  # echo 핀 값이 1이면 초음파가 발사되었음
  pulse_start = time.time() # 초음파 발사 시간 기록
  while(GPIO.input(echo) == 1): # echo 핀 값이 1->0으로 바뀔 때까지 루프
    pass

  # echo 핀 값이 0이 되면 초음파 수신하였음
  pulse_end = time.time() # 초음파가 되돌아 온 시간 기록
  pulse_duration = pulse_end - pulse_start # 경과 시간 계산
  return pulse_duration*340*100/2 # 거리 계산하여 리턴(단위 cm)

trig = 20 # GPIO20
echo = 16 # GPIO16
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

while True:
  distance = measureDistance(trig, echo)
  print("물체와의 거리는 %fcm 입니다." % distance)
  time.sleep(0.5) # 0.5초 간격으로 거리 측정(0.3으로 하면 정확)

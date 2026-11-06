import time
import RPi.GPIO as GPIO

def increase(pwm):
  print("increase the light")
  for value in range(0, 100): # 5초 동안 루프
      pwm.ChangeDutyCycle(value)
      time.sleep(0.05)

def decrease(pwm):
  print("decrease the light")
  for value in range(99, -1, -1): # 5초 동안 루프
     pwm.ChangeDutyCycle(value)
     time.sleep(0.05)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

led = 6 # GPIO6 핀에 LED 연결
GPIO.setup(led, GPIO.OUT) # GPIO6 핀을 출력으로 지정
GPIO.output(led, GPIO.LOW) # GPIO6 핀에 0V 출력
pwm = GPIO.PWM(led, 100) # GPIO6 핀에 100Hz의 신호를 발생하도록 설정
pwm.start(0) # GPIO6 핀에 듀티 사이클 0%, 100Hz의 신호 발생 시작
while True:
  increase(pwm) # 5초동안 듀티 사이클 증가. LED를 점점 밝게
  decrease(pwm) # 5초동안 듀티 사이클 감소. LED를 점점 어둡게

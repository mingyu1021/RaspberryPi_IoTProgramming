import RPi.GPIO as GPIO
import time

# button이 눌러질 때 호출되는 콜백 함수
def button_pressed(channel):
  print("%d 핀에 연결된 스위치 눌러짐" % channel)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

button = 21 # GPIO21
GPIO.setup(button, GPIO.IN, GPIO.PUD_DOWN)

# button을 누르면 100ms의 디바운스 후 button_pressed()가 호출되도록 설정
GPIO.add_event_detect(button, GPIO.RISING, button_pressed, bouncetime=100)
while True:
  pass # 사용자는 필요한 다른 작업을 이곳에 작성한다.

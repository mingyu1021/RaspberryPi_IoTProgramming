import time
import RPi.GPIO as GPIO

# pin에 연결된 LED에 value(0/1) 값을 출력하여 LED를 켜거나 끄는 함수
def led_on_off(pin, value):
   GPIO.output(pin, value)

GPIO.setmode(GPIO.BCM) # BCM 모드로 작동
GPIO.setwarnings(False) # 경고글이 출력되지 않게 설정

led = 6 # GPIO6 핀
GPIO.setup(led, GPIO.OUT) # GPIO6 핀을 출력으로 지정

button = 21 # GPIO21 핀
GPIO.setup(button, GPIO.IN, GPIO.PUD_DOWN) # GPIO21 핀을 입력으로 지정하고 풀다운 효과 지정

print("스위치를 누르고 있는 동안 LED가 켜지고 놓으면 꺼집니다.")
while True :
   status = GPIO.input(button) # GPIO21 핀로부터 디지털 값(0/1) 읽기
   led_on_off(led, status) # 읽은 값(0/1)을 led(GPIO6 핀)로 출력

GPIO.cleanup()

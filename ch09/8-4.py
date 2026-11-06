import time
import RPi.GPIO as GPIO

# pin에 연결된 LED에 value(0/1) 값을 출력하여 LED를 켜거나 끄는 함수
def led_on_off(pin, value):
   GPIO.output(pin, value)

# button이 눌러질 때 호출되는 콜백 함수
def button_pressed(pin):
   global btn_status # btn_status는 전역 변수임
   global led # led는 전역 변수임
   btn_status = 0 if btn_status == 1 else 1
   led_on_off(led, btn_status)

led = 6 # GPIO6
button = 21 # GPIO21
btn_status = 0 # 현재 버튼이 눌러진 상태. 1이면 눌러져 있음

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(led, GPIO.OUT) # led 핀을 출력으로 지정
GPIO.setup(button, GPIO.IN, GPIO.PUD_DOWN) # button 핀을 입력으로 지정

# button을 누르면 100ms의 디바운스 후 button_pressed()가 호출되도록 설정
GPIO.add_event_detect(button, GPIO.RISING, button_pressed, 100)

print("스위치를 누르면 LED가 On되고 다시 누르면 Off 됩니다")
while True:
   pass # 사용자는 필요한 다른 작업이 있으면 이곳에 작성한다.

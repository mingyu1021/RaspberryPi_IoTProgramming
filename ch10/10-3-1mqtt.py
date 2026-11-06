import time
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import circuit # 초음파 센서 함수와 GPIO 초기화에 사용

# 서보 모터를 angle(0~180)도로 움직이는 함수
def controlServo(angle):
  angle = max(0, min(180, angle)) # 0~180도 범위로 제한
  pwm.ChangeDutyCycle(2.5 + angle / 18) # 0도=2.5%(0.5ms), 180도=12.5%(2.5ms)
  time.sleep(0.5) # 서보가 움직일 시간
  pwm.ChangeDutyCycle(0) # 펄스를 멈추어 떨림 방지

def on_connect(client, userdata, flag, rc, prop=None):
  client.subscribe("servo") # "servo" 토픽으로 구독 신청
  client.subscribe("led") # "led" 토픽으로 구독 신청

def on_message(client, userdata, msg) :
  try:
    value = int(msg.payload) # led는 0 또는 1, servo는 0~180의 정수
  except ValueError:
    return # 숫자가 아닌 메시지는 무시
  if msg.topic == "led":
    circuit.controlLED(1 if value else 0) # LED를 켜거나 끔
  else:
    controlServo(value) # 서보 모터를 움직임

servo = 18 # GPIO18
GPIO.setup(servo, GPIO.OUT) # GPIO18 핀을 출력으로 지정
pwm = GPIO.PWM(servo, 50) # 서보 모터는 50Hz 신호 사용
pwm.start(0) # 듀티 사이클 0%로 시작
controlServo(90) # 시작할 때 90도로 이동
circuit.controlLED(0) # 시작할 때 LED 끄기

ip = "localhost" # 현재 브로커는 이 컴퓨터에 설치되어 있음

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

client.connect(ip, 1883) # 브로커에 연결
client.loop_start() # 메시지 루프를 실행하는 스레드 생성

# 도착하는 메시지는 on_message() 함수에 의해 처리되어 LED와 서보 모터를 제어하는 작업과
# 병렬적으로 1초 단위로 초음파 센서로부터 거리를 읽어 전송하는 무한 루프 실행
while True:
  distance = circuit.measure_distance() # 초음파 센서로부터 거리 읽기
  client.publish("ultrasonic", distance) # “ultrasonic” 토픽으로 거리 전송
  time.sleep(1) # 1초 동안 잠자기

client.loop_stop() # 메시지 루프를 실행하는 스레드 종료
client.disconnect()

import time
import paho.mqtt.client as mqtt
import circuit # circuit.py는 초음파 센서로부터 거리를 측정하는 모듈 포함

ip = "localhost" # 현재 브로커는 이 컴퓨터에 설치되어 있음

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(ip, 1883) # 브로커에 연결
client.loop_start() # 메시지 루프를 실행하는 스레드 생성

while True:
  distance = circuit.measure_distance() # 초음파 센서로부터 거리 측정
  client.publish("ultrasonic", distance) # “ultrasonic” 토픽으로 거리 전송
  time.sleep(1) # 1초 동안 잠자기

client.loop_stop() # 메시지 루프를 실행하는 스레드 종료
client.disconnect()

import time
import paho.mqtt.client as mqtt

ip = "localhost" # 브로커는 이 컴퓨터에 설치되어 있음

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(ip, 1883) # 브로커의 1883 포트에 연결
client.loop_start() # 메시지 루프를 실행하는 스레드 생성

count = 0
while True:
  message = input("문자메시지>>") # 사용자로부터 문자열 입력
  if message == "exit" :
     break
  client.publish("letter", message) # “letter” 토픽과 함께 메시지 전송
  print("메시지 전송: %s" % message)

client.loop_stop() # 메시지 루프를 실행하는 스레드 종료
client.disconnect() # 브로커와 연결 종료

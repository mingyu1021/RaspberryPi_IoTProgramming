import time
import paho.mqtt.client as mqtt

ip = input("브로커의 IP 주소>>")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(ip, 1883) # 브로커에 연결
client.loop_start() # 메시지 루프를 실행하는 스레드 생성

while True:
    message = input("문자메시지>>") # 사용자로부터 문자열 입력
    if message == "exit":
        break
    client.publish("letter", message)
    print("메시지 전송: %s" % message)

client.loop_stop() # 메시지 루프를 실행하는 스레드 종료
client.disconnect()

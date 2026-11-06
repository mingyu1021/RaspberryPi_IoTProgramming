import os
import time
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flag, rc, prop=None):
    print("jpeg 토픽으로 메시지 구독 신청")
    client.subscribe("jpeg")

def on_message(client, userdata, msg):
    filename = './data/image%d.jpg' % (time.time()*10)
    file = open(filename, "wb") # 파일 열기. 없으면 새로 생성
    file.write(msg.payload) # 수신한 이미지를 파일에 쓰기
    file.close() # 파일 닫기
    print("이미지수신 %s" % filename)

os.makedirs("./data", exist_ok=True) # 이미지를 저장할 data 디렉터리 생성
ip = input("브로커의 IP>>") # 브로커 IP 주소 입력

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect(ip, 1883)
client.loop_forever() # 메시지 루프 실행

import paho.mqtt.client as mqtt

def on_connect(client, userdata, flag, rc, prop=None):
    print("접속 결과: " + str(rc)) # 접속 결과 출력, rc가 0이면 성공
    client.subscribe("letter") # letter 토픽으로 구독 신청

def on_message(client, userdata, msg):
    print(msg.topic, end=", ") # 토픽 출력
    print(str(msg.payload.decode("utf-8"))) # 메시지 출력

ip = input("브로커의 IP 주소>>")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect # on_connect 콜백 함수 등록
client.on_message = on_message # on_message 콜백 함수 등록
client.connect(ip, 1883)
client.loop_forever() # 메시지 루프

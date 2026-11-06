import paho.mqtt.client as mqtt

broker_ip = "localhost" # 이 컴퓨터의 브로커에 접속

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(broker_ip, 1883) # 1883 포트로 브로커에 접속
client.loop_start() # 메시지 루프를 실행하는 스레드 생성

while True:
    temperature = input("온도>>>") # 사용자로부터 온도 입력
    temperature = int(temperature) # 문자열을 정수로 변환
    if temperature == 0: # 온도에 0이 입력되면 while 문 벗어남
        break
    client.publish("room/temp", temperature) # 온도 전송

client.loop_stop() # 메시지 루프를 실행하는 스레드 종료
client.disconnect()
print("프로그램 종료")

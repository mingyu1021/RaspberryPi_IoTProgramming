import time
import RPi.GPIO as GPIO

try:
   # pin에 연결된 LED에 value(0/1) 값을 출력하여 LED를 켜거나 끄는 함수
   def led_on_off(pin, value):
      GPIO.output(pin, value)

   GPIO.setmode(GPIO.BCM) # BCM 모드로 작동
   GPIO.setwarnings(False) # 경고글이 출력되지 않게 설정

   led = 6 # GPIO6 핀
   GPIO.setup(led, GPIO.OUT) # GPIO6 핀을 출력으로 지정

   on_off = 1 # 1은 디지털 출력 값. 1 = 5V
   print("LED를 지켜보세요.")

   # 5번 LED를 깜박임
   for i in range(5):
      led_on_off(led, on_off) # led가 연결된 핀에 1또는 0 값 출력
      time.sleep(1) # 1초 동안 잠자기
      print(i, end=' ', flush=True)
      on_off = 0 if on_off == 1 else 1 # 0과 1의 토글링

except KeyboardInterrupt:
   print("Ctrl+C 종료")
finally:
   print("cleanup")
   GPIO.cleanup()

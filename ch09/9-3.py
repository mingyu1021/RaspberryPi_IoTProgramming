import busio
import time
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D12) # board.D12는 GPIO 12번 핀을 의미

mcp = MCP.MCP3008(spi, cs) # MCP3202 칩을 제어할 객체 생성
mcp_chan0 = AnalogIn(mcp, MCP.P0) # MCP.P0은 MCP3202의 0번 채널을 뜻함

print("*** 조도 센서로부터 조도 값 읽기 시작 ***")
try:
   while True:
      # mcp_chan0에는 읽는 밝기 값이 16비트(0-65535) 크기로 저장됨
      # MCP3202는 12비트(0~4095)로 밝기를 출력하므로 읽은 값을 16으로 나눔
      light = mcp_chan0.value //16

      # 12비트 값(0~4095)으로 밝기 출력
      print("밝기: ", light)
      time.sleep(1)

except KeyboardInterrupt:
   print("\n사용자에 의해 프로그램이 종료되었습니다.")

#!/bin/bash
# 7주차 MQTT 예제 7-1 ~ 7-4를 한 터미널에서 순서대로 시연한다.
# 사용자 입력은 자동으로 넣고, 구독자(subscriber) 출력은 초록색으로 표시한다.
cd "$(dirname "$0")"
PY=~/myenv/bin/python
AMQTT=~/.local/share/mqtt-test-broker/bin/amqtt   # mosquitto가 없을 때 사용할 대체 브로커

G=$'\033[1;32m'; Y=$'\033[1;33m'; C=$'\033[1;36m'; N=$'\033[0m'

title() { echo; echo -e "${C}========== $1 ==========${N}"; sleep 1.5; }

# 구독자 실행: 출력 앞에 [구독자]를 붙여 초록색으로 표시
sub() { (echo localhost; exec sleep 300) | $PY -u "$1" 2>&1 | sed -u "s/^/    ${G}[구독자] /;s/\$/${N}/" & SUB=$!; sleep 2; }
stop_sub() { sleep 2; pkill -f "$PY -u $1"; pkill -P $$ -x sleep; wait $SUB 2>/dev/null; }

# 발행자에 입력을 한 줄씩 천천히 넣으면서 화면에도 보여준다
feed() { for v in "$@"; do sleep 2; echo -e "${Y}$v${N}" > /dev/tty; echo "$v"; done; sleep 1; }

# 브로커 실행
if command -v mosquitto > /dev/null; then
    title "mosquitto 브로커 실행 (포트 1883)"
    mosquitto -c mos.conf > /dev/null 2>&1 & BROKER=$!
else
    title "대체 MQTT 브로커 실행 (포트 1883, mosquitto 미설치)"
    $AMQTT > /dev/null 2>&1 & BROKER=$!
fi
# 1883 포트가 열릴 때까지 최대 20초 대기
for i in $(seq 40); do ss -ltn | grep -q ":1883 " && break; sleep 0.5; done
echo "브로커 준비 완료"

title "예제 7-1  텍스트 메시지 전송 (토픽: letter)"
sub 7-1sub.py
feed localhost "Good Morning!" "즐거운 날입니다." "MQTT 전송 재밌다." exit | $PY -u 7-1pub.py
stop_sub 7-1sub.py

title "예제 7-2  온도 값 전송 (토픽: room/temp)"
sub 7-2win.py
feed 23 34 66 61 0 | $PY -u 7-2pi.py
stop_sub 7-2win.py

title "예제 7-3  start/stop 명령으로 온도 전송 제어 (토픽: command, room/temp)"
$PY -u 7-3pi.py 2>&1 | sed -u "s/^/    ${G}[라즈베리파이 7-3pi] /;s/\$/${N}/" & PI73=$!
sleep 2
(feed localhost start; sleep 9; feed stop; sleep 2; feed exit) | $PY -u 7-3win.py
pkill -f "$PY -u 7-3pi.py"; wait $PI73 2>/dev/null
echo

title "예제 7-4  카메라 사진 전송 (토픽: jpeg)"
rm -f data/*.jpg
sub 7-4win.py
feed yes yes yes stop | $PY -u 7-4pi.py 2>/dev/null
stop_sub 7-4win.py

kill $BROKER 2>/dev/null

# 수신한 사진을 브라우저로 보여준다
{
    echo '<html><head><meta charset="utf-8"><title>예제 7-4 수신 이미지</title></head>'
    echo '<body style="font-family:sans-serif;background:#222;color:#eee">'
    echo '<h1>예제 7-4: MQTT로 수신한 카메라 이미지</h1>'
    for f in data/*.jpg; do echo "<figure style=\"display:inline-block\"><img src=\"$f\" width=\"600\"><figcaption>$f</figcaption></figure>"; done
    echo '</body></html>'
} > result.html
echo; echo -e "${C}모든 예제 완료. 수신한 사진을 브라우저로 엽니다.${N}"
chromium --password-store=basic --no-first-run --user-data-dir=/tmp/ch07-demo-browser "file://$PWD/result.html" > /dev/null 2>&1 &
read -p "엔터를 누르면 창이 닫힙니다."

#!/bin/bash
# 예제 서버들을 8081~8093 포트에, 대시보드를 8080에 띄운다.  종료: ./run_all.sh stop
cd "$(dirname "$0")"
PY=~/myenv/bin/python
pkill -f "[m]yenv/bin/python -m flask --app" ; pkill -f "[m]yenv/bin/python dashboard.py"
[ "$1" = stop ] && exit 0
mkdir -p logs
port=8081
for f in hello_flask.py 6-1.py 6-2.py 6-3.py 6-4.py 6-5.py 6-6.py 6-7.py 6-8.py 6-9.py 6-10.py 6-11.py 6-12.py; do
  nohup $PY -m flask --app $f run --host 0.0.0.0 --port $port > logs/$f.log 2>&1 &
  port=$((port+1))
done
nohup $PY dashboard.py > logs/dashboard.log 2>&1 &
sleep 3
echo "대시보드: http://$(hostname -I | awk '{print $1}'):8080"

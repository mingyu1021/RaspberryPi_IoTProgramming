#!/bin/bash
# 예제 3-2 다중 사용자들 사이의 파일 허가 실습
# pi가 hello.c를 복사해 hello2.c를 만들고, kitae가 hello2.c를 읽지 못하게 허가 속성을 바꾼다.
# 예제 3-1로 kitae 계정을 먼저 만들어야 한다. 실행: ./3-2.sh
cd "$(dirname "$0")"
cp hello.c hello2.c
ls -l
chmod 711 hello2.c # rwx--x--x: 나만 읽기/쓰기, 그룹·기타 사용자는 실행만
ls -l

# 터미널2에서 kitae로 로그인했다고 보고, kitae 권한으로 두 파일을 읽어 본다.
# (kitae가 /home/pi 안으로 들어갈 수 있어야 hello.c가 보인다)
echo "--- kitae로 hello.c 읽기"
sudo -u kitae cat "$PWD/hello.c"
echo "--- kitae로 hello2.c 읽기 (허가 거부가 나와야 정상)"
sudo -u kitae cat "$PWD/hello2.c"

#!/bin/bash
# 예제 3-1 사용자 kitae와 jmlee 추가 실습
# useradd로 계정을 만들고(-c 설명, -m 홈 디렉터리 생성), passwd로 암호를 설정한다.
# 시스템 계정을 바꾸므로 sudo 권한이 필요하다. 실행: ./3-1.sh
sudo useradd kitae -c student -m
sudo useradd jmlee -c student -m
sudo passwd kitae # 입력된 암호는 보이지 않음
sudo passwd jmlee
ls /home
grep -E '^(kitae|jmlee):' /etc/passwd

# 실습 후 계정을 지우려면 (홈 디렉터리, 메일 스풀까지 삭제)
# sudo userdel -r kitae
# sudo userdel -r jmlee

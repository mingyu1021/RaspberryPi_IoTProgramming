#!/bin/bash
# 예제 4-1 사진을 촬영하여 images/image.jpg에 저장
# PDF는 USB 카메라용 fswebcam을 사용한다. 카메라 모듈(CSI)은 rpicam-still로 촬영한다.
cd "$(dirname "$0")/images"
if rpicam-hello --list-cameras 2>/dev/null | grep -q "^0 :"; then
    rpicam-still -n -t 1000 --width 640 --height 480 -o image.jpg
else
    fswebcam image.jpg
fi
ls

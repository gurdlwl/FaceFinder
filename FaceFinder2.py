# 내장 또는 외장 카메라 영상 띄우는 코드
# https://076923.github.io/posts/Python-opencv-2/

import cv2
import sys

# VideoCapture(n)을 이용, 내장이나 외장 영상 받아옴.
capture = cv2.VideoCapture(0)

# set(option, n)을 이용하여 width, height를 설정.
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    ret, frame = capture.read()
    cv2.imshow("Video Frame", frame)
    # 만약 어느 키라도 눌리면 while문 탈출
    if cv2.waitKey(1)>0 : break;

# .release()로 메모리 해재
capture.release()
# .destroyAllWindows()로 모든 윈도우창 닫기
cv2.destroyAllWindows()

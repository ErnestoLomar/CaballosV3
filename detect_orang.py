import cv2
import numpy as np

hsv_orange_min1 = np.array([10, 100,20], np.uint8)
hsv_orange_max1 = np.array([15,255,255], np.uint8)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        break
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, hsv_orange_min1, hsv_orange_max1)

    cnts, chain = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    c = max(cnts, key=cv2.contourArea)

    x,y,w,h = cv2.boundingRect(c)

    cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255),2)

    cv2.imshow("Frame", mask)
    cv2.imshow("Frame2s", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break
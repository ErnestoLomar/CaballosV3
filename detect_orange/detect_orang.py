import cv2
import numpy as np

hsv_orange_min1 = np.array([10, 100,20], np.uint8)
hsv_orange_max1 = np.array([15,255,255], np.uint8)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

i = 0

while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        break
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, hsv_orange_min1, hsv_orange_max1)

    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    for c in cnts:
        
        area = cv2.contourArea(c)

        if area > 3000:

            nuevo_contorno = cv2.convexHull(c)
            cv2.drawContours(frame, [nuevo_contorno], 0, (255,0,0), 3)

    cv2.imshow("Frame", mask)
    cv2.imshow("Frame2s", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break
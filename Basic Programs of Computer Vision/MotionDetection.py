import cv2
import numpy as np
import os

cap = cv2.VideoCapture(0)

# Lower resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

if not cap.isOpened():
    print("Error: Could not open webcam")
    exit()

ret, frame1 = cap.read()
if not ret:
    print("Error: Could not read frame")
    cap.release()
    exit()

gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
gray1 = cv2.GaussianBlur(gray1, (21, 21), 0)

try:
    while True:
        ret, frame2 = cap.read()
        if not ret:
            print("Error: Could not read frame")
            break

        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)

        delta = cv2.absdiff(gray1, gray2)
        thresh = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False
        for contour in contours:
            if cv2.contourArea(contour) > 500:
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)
                motion_detected = True

        if motion_detected:
            cv2.putText(frame2, "Motion Detected!", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            os.system('beep -f 1000 -l 100')  # replace with pygame if needed

        cv2.imshow("Motion Detection", frame2)
        cv2.imshow("Threshold", thresh)

        gray1 = gray2

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Program terminated by user")

finally:
    cap.release()
    cv2.destroyAllWindows()

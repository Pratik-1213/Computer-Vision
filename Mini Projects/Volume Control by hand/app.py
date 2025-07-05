import cv2

cap = cv2.VideoCapture(0)  # Use 0 if your webcam doesn't show

while True:
    success, img = cap.read()
    if not success:
        break

    cv2.imshow("Webcam Feed", img)
    cv2.waitKey(1)


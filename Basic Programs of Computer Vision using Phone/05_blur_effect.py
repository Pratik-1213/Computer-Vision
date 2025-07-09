import cv2

url = 'http://192.168.31.118:8080/video'
cap = cv2.VideoCapture(url)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    blur = cv2.GaussianBlur(frame, (15, 15), 0)
    cv2.imshow("Blur Effect", blur)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
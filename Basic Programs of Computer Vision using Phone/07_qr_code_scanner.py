import cv2

url = 'http://192.168.31.118:8080/video'
cap = cv2.VideoCapture(url)
detector = cv2.QRCodeDetector()

while True:
    ret, frame = cap.read()
    if not ret:
        break
    data, bbox, _ = detector.detectAndDecode(frame)
    if bbox is not None:
        cv2.putText(frame, data, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
    cv2.imshow("QR Code Scanner", frame)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
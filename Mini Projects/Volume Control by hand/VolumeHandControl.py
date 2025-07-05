import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# -----------------------------------
# Configuration
# -----------------------------------
FRAME_WIDTH, FRAME_HEIGHT = 640, 480

# -----------------------------------
# Webcam Initialization
# -----------------------------------
cap = cv2.VideoCapture(0)
cap.set(3, FRAME_WIDTH)
cap.set(4, FRAME_HEIGHT)

# -----------------------------------
# Hand Detector
# -----------------------------------
detector = htm.handDetector(detectionCon=0.7)

# -----------------------------------
# Pycaw Volume Setup (Scalar for accurate %)
# -----------------------------------
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volumeControl = cast(interface, POINTER(IAudioEndpointVolume))

# -----------------------------------
# Variables
# -----------------------------------
prevTime = 0
volBar = 400
volPercent = 0
smoothness = 5  # Lower = smoother control

# -----------------------------------
# Main Loop
# -----------------------------------
while True:
    success, img = cap.read()
    if not success:
        print("Camera not found.")
        break

    img = detector.findHands(img)
    lmList, _ = detector.findPosition(img, draw=False)

    if len(lmList) >= 9:
        x1, y1 = lmList[4][1], lmList[4][2]  # Thumb tip
        x2, y2 = lmList[8][1], lmList[8][2]  # Index tip
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # Visual markers
        cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

        # Measure distance
        length = math.hypot(x2 - x1, y2 - y1)

        # Map distance to 0.0 - 1.0 (scalar volume)
        volScalar = np.interp(length, [50, 250], [0.0, 1.0])
        volScalar = np.clip(volScalar, 0.0, 1.0)  # Ensure valid bounds
        volumeControl.SetMasterVolumeLevelScalar(volScalar, None)

        # Visuals
        volBar = np.interp(volScalar, [0.0, 1.0], [400, 150])
        targetVolPercent = volScalar * 100
        volPercent = smoothness * round(targetVolPercent / smoothness)

        if length < 50:
            cv2.circle(img, (cx, cy), 12, (0, 255, 0), cv2.FILLED)

    # Draw Volume Bar and Percentage
    cv2.rectangle(img, (50, 150), (85, 400), (0, 122, 255), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 122, 255), cv2.FILLED)
    cv2.putText(img, f'{int(volPercent)} %', (40, 450),
                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 122, 255), 3)

    # FPS
    currTime = time.time()
    fps = 1 / (currTime - prevTime + 1e-6)
    prevTime = currTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 255, 0), 3)

    # Show
    cv2.imshow("Volume Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

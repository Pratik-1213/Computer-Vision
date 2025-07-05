import cv2
import numpy as np
import mediapipe as mp

# Mediapipe hand setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Webcam
cap = cv2.VideoCapture(0)

# Canvas for painting
canvas = np.zeros((480, 640, 3), dtype=np.uint8)

# Previous coordinates
prev_x, prev_y = 0, 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Mirror image
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get index finger tip (landmark 8)
            h, w, c = frame.shape
            x = int(hand_landmarks.landmark[8].x * w)
            y = int(hand_landmarks.landmark[8].y * h)

            # If previous point is valid, draw line
            if prev_x == 0 and prev_y == 0:
                prev_x, prev_y = x, y

            cv2.line(canvas, (prev_x, prev_y), (x, y), (255, 0, 0), 5)
            prev_x, prev_y = x, y

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    else:
        # Reset previous points if hand not detected
        prev_x, prev_y = 0, 0

    # Combine frame and canvas
    blended = cv2.addWeighted(frame, 0.5, canvas, 0.5, 0)

    cv2.imshow("Virtual Painter", blended)

    key = cv2.waitKey(1)
    if key == ord('c'):  # Clear canvas
        canvas = np.zeros((480, 640, 3), dtype=np.uint8)
    elif key == ord('q'):  # Quit
        break

cap.release()
cv2.destroyAllWindows()

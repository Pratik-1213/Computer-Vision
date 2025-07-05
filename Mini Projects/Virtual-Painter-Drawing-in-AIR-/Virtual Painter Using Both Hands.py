import cv2
import numpy as np
import mediapipe as mp

# Mediapipe hand setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)  # 👈 Allow 2 hands
mp_draw = mp.solutions.drawing_utils

# Webcam
cap = cv2.VideoCapture(0)

# Canvas for painting
canvas = np.zeros((480, 640, 3), dtype=np.uint8)

# Previous coordinates for both hands
prev_coords = {0: (0, 0), 1: (0, 0)}

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks and results.multi_handedness:
        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            h, w, _ = frame.shape
            x = int(hand_landmarks.landmark[8].x * w)
            y = int(hand_landmarks.landmark[8].y * h)

            prev_x, prev_y = prev_coords.get(idx, (0, 0))
            if prev_x == 0 and prev_y == 0:
                prev_coords[idx] = (x, y)

            cv2.line(canvas, (prev_x, prev_y), (x, y), (255, 0, 0), 5)
            prev_coords[idx] = (x, y)

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    else:
        # Reset both hands if not detected
        prev_coords = {0: (0, 0), 1: (0, 0)}

    # Blend canvas and camera
    blended = cv2.addWeighted(frame, 0.5, canvas, 0.5, 0)
    cv2.imshow("Virtual Painter - Two Hands", blended)

    key = cv2.waitKey(1)
    if key == ord('c'):  # Clear canvas
        canvas = np.zeros((480, 640, 3), dtype=np.uint8)
    elif key == ord('q'):  # Quit
        break

cap.release()
cv2.destroyAllWindows()

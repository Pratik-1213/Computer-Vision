import cv2
import numpy as np
import mediapipe as mp

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Start webcam
cap = cv2.VideoCapture(0)
cap.set(3, 950)
cap.set(4, 550)

# Variables for calculator
number1 = None
number2 = None
operator = None
result = None
mode = "WAITING"
evaluated = False  # Flag to prevent repeated evaluation

def count_fingers(landmarks):
    fingers = []

    # Thumb
    if landmarks[4][0] < landmarks[3][0]:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers
    for id in [8, 12, 16, 20]:
        if landmarks[id][1] < landmarks[id - 2][1]:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    landmarks_list = []
    gesture_text = ""

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            for id, lm in enumerate(hand_landmarks.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmarks_list.append((cx, cy))

        if len(landmarks_list) == 21:
            fingers = count_fingers(landmarks_list)
            total_fingers = sum(fingers)

            # Clear gesture: Closed palm (Fist)
            if fingers == [0, 0, 0, 0, 0]:
                number1 = None
                number2 = None
                operator = None
                result = None
                mode = "WAITING"
                evaluated = False
                gesture_text = "Clear All"

            # Evaluate gesture: Full palm (All fingers open)
            elif fingers == [1, 1, 1, 1, 1] and number1 is not None and number2 is not None and operator:
                if not evaluated:
                    try:
                        expression = f"{number1}{operator}{number2}"
                        result = eval(expression)
                        gesture_text = f"{expression} = {result}"
                        mode = "RESULT"
                        evaluated = True  # prevent repeat
                    except:
                        gesture_text = "Error"
                        result = None
                        mode = "ERROR"

            # Operator gestures
            elif fingers == [1, 1, 0, 0, 1]:
                operator = "+"
                gesture_text = "Add (+)"
                mode = "OPERATOR SELECTED"
                evaluated = False

            elif fingers == [1, 0, 0, 0, 1]:
                operator = "-"
                gesture_text = "Subtract (-)"
                mode = "OPERATOR SELECTED"
                evaluated = False

            elif fingers == [0, 1, 0, 0, 1]:
                operator = "*"
                gesture_text = "Multiply (*)"
                mode = "OPERATOR SELECTED"
                evaluated = False

            elif fingers == [0, 0, 0, 0, 1]:
                operator = "/"
                gesture_text = "Divide (/)"
                mode = "OPERATOR SELECTED"
                evaluated = False

            # Number input
            elif total_fingers in [1, 2, 3, 4, 5]:
                if number1 is None:
                    number1 = total_fingers
                    gesture_text = f"Number 1: {number1}"
                    mode = "NUMBER 1"
                    evaluated = False
                elif operator and number2 is None:
                    number2 = total_fingers
                    gesture_text = f"Number 2: {number2}"
                    mode = "NUMBER 2"
                    evaluated = False

    # Display info
    cv2.putText(img, f"Mode: {mode}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    cv2.putText(img, f"Num1: {number1}", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 200, 0), 2)
    cv2.putText(img, f"Op: {operator}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 0, 200), 2)
    cv2.putText(img, f"Num2: {number2}", (10, 160), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 150, 255), 2)
    cv2.putText(img, f"Result: {result}", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 100, 100), 2)
    cv2.putText(img, f"Gesture: {gesture_text}", (10, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("🤖 Virtual Calculator", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

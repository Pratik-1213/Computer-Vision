import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
) as hands:

    while cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Example: count how many fingers are open
                tips = [4, 8, 12, 16, 20]
                h, w, _ = frame.shape
                landmarks = hand_landmarks.landmark
                fingers = []

                if landmarks[tips[0]].x < landmarks[tips[0] - 1].x:  # Thumb
                    fingers.append(1)
                else:
                    fingers.append(0)

                for tip in tips[1:]:
                    if landmarks[tip].y < landmarks[tip - 2].y:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                total = fingers.count(1)
                cv2.putText(frame, f'Fingers: {total}', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        cv2.imshow("Hand Gesture", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()

import cv2
import mediapipe as mp
import numpy as np
import time 

class FingerStateDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.tip_ids = [4, 8, 12, 16, 20]
        self.pip_ids = [3, 7, 11, 15, 19]
        self.lm_list = []
        self.p_time = 0
        self.running = True

    def find_hands(self, img):
        if img is None:
            print("Error: No image captured from the camera.")
            return img
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    img,
                    hand_lms,
                    self.mp_hands.HAND_CONNECTIONS,
                    landmark_drawing_spec=self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4),
                    connection_drawing_spec=self.mp_drawing.DrawingSpec(color=(255, 0, 255), thickness=2)
                )
        return img

    def find_position(self, img):
        self.lm_list = []
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[0]
            h, w, _ = img.shape
            for id, lm in enumerate(hand.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lm_list.append([id, cx, cy])
                if id in self.tip_ids:
                    cv2.circle(img, (cx, cy), 8, (255, 0, 0), cv2.FILLED)

    def fingers_up(self):
        fingers = []
        if len(self.lm_list) < 21:
            return [0, 0, 0, 0, 0]
        thumb_tip = self.lm_list[4]
        thumb_mcp = self.lm_list[2]
        pinky_mcp = self.lm_list[17]
        dist_tip_to_pinky = np.hypot(thumb_tip[1] - pinky_mcp[1], thumb_tip[2] - pinky_mcp[2])
        dist_mcp_to_pinky = np.hypot(thumb_mcp[1] - pinky_mcp[1], thumb_mcp[2] - pinky_mcp[2])
        fingers.append(1 if dist_tip_to_pinky > dist_mcp_to_pinky else 0)
        for id in range(1, 5):
            if self.lm_list[self.tip_ids[id]][2] < self.lm_list[self.pip_ids[id]][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers

    def draw_finger_states(self, frame):
        if not self.lm_list:
            return frame
        h, w, _ = frame.shape
        y_offset = h - 120
        fingers = self.fingers_up()
        finger_names = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
        cv2.rectangle(frame, (10, y_offset-20), (200, y_offset+100), (0, 0, 0, 128), -1)
        cv2.putText(frame, "FINGER STATES", (20, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)
        for i, (name, status) in enumerate(zip(finger_names, fingers)):
            color = (0, 255, 0) if status == 1 else (0, 0, 255)
            cv2.putText(frame, f"{name}: {'UP' if status == 1 else 'DOWN'}",
                       (20, y_offset + 20 + i*20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        return frame

    def run(self):
        try:
            while self.running:
                success, frame = self.cap.read()
                if not success:
                    print("Failed to capture frame from camera. Retrying...")
                    continue
                frame = cv2.flip(frame, 1)
                frame = self.find_hands(frame)
                self.find_position(frame)
                frame = self.draw_finger_states(frame)
                c_time = time.time()
                fps = 1 / (c_time - self.p_time) if c_time != self.p_time else 0
                self.p_time = c_time
                cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.imshow("Finger State Detector", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == 27:  # ESC key to exit
                    self.running = False
        except Exception as e:
            print(f"Error in main loop: {e}")
        finally:
            print("Cleaning up resources...")
            self.cap.release()
            cv2.destroyAllWindows()

    def cleanup(self):
        if self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()

def main():
    print("Starting Finger State Detector...")
    print("Press 'ESC' to exit")
    detector = FingerStateDetector()
    try:
        detector.run()
    except KeyboardInterrupt:
        print("Application interrupted by user.")
    finally:
        detector.cleanup()

if __name__ == "__main__":
    main()
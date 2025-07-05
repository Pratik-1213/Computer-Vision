
import cv2
from fer import FER
import numpy as np

# Initialize the FER detector (using MTCNN for face detection)
detector = FER(mtcnn=True)

# Start the webcam feed
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Detect emotions in the frame
    result = detector.detect_emotions(frame)

    # Process detected faces and emotions
    for face in result:
        # Get facial coordinates
        x, y, w, h = face['box']
        
        # Draw rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Get emotions and find the dominant one
        emotions = face['emotions']
        dominant_emotion = max(emotions, key=emotions.get)
        emotion_score = emotions[dominant_emotion]
        
        # Display the dominant emotion and its score
        text = f"{dominant_emotion}: {emotion_score:.2f}"
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Live Emotion Detection', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()

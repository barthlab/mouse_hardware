# TODO convert wheel ticks to speed? here rather than in the code?

import cv2
import numpy as np

# Constants for circle detection
# Function to detect circle in the selected area
def detect_circle(frame, rect):
    x1, y1, x2, y2 = rect
    roi = frame[y1:y2, x1:x2]  # Extract the region of interest

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        print(contour)
        if area > MIN_RADIUS ** 2 * np.pi and area < MAX_RADIUS ** 2 * np.pi:
            (x, y), radius = cv2.minEnclosingCircle(contour)
            center = (int(x) + x1, int(y) + y1)  # Calculate the center coordinates in the original frame
            
            # Draw circle outline
            cv2.circle(frame, center, int(radius), CIRCLE_COLOR, OUTLINE_THICKNESS)
            
            # Draw dot at the center of the circle
            cv2.circle(frame, center, 1, DOT_COLOR, -1)
            
            return int(radius)

    return None

# Load video file
video_path = '../data/mouse_video_pupil_alex.h264'
cap = cv2.VideoCapture(video_path)

# Create window and set mouse callback
cv2.namedWindow('Video')

# Loop through video frames
while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to read frame from the video")
        break


    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, frame_thresh = cv2.threshold(frame_gray, 70, 255, cv2.THRESH_BINARY)

    cv2.imshow('Video', frame_thresh)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()


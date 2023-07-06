# TODO convert wheel ticks to speed? here rather than in the code?

import cv2
import numpy as np



# Constants for circle detection
MIN_RADIUS = 10
MAX_RADIUS = 100
CIRCLE_COLOR = (0, 0, 255)  # Red



# Global variables for selected rectangle
selected_rectangle = None
rectangle_selected = False



# Mouse callback function to select rectangle
def select_rectangle(event, x, y, flags, param):
    global selected_rectangle, rectangle_selected

    if event == cv2.EVENT_LBUTTONDOWN:
        selected_rectangle = (x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        selected_rectangle = (selected_rectangle[0], x, selected_rectangle[1], y)
        rectangle_selected = True



# Function to detect circle in the selected area
def detect_circle(frame, rect):
    x1, y1, x2, y2 = rect
    roi = frame[y1:y2, x1:x2]  # Extract the region of interest

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > MIN_RADIUS ** 2 * np.pi and area < MAX_RADIUS ** 2 * np.pi:
            (x, y), radius = cv2.minEnclosingCircle(contour)
            center = (int(x), int(y))
            radius = int(radius)
            cv2.circle(roi, center, radius, CIRCLE_COLOR, 2)
            return radius

    return None



# Load video file
video_path = 'path/to/your/video.mp4'
cap = cv2.VideoCapture(video_path)



# Set codec configuration for H.264
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'avc1'))



# Create window and set mouse callback
cv2.namedWindow('Video')
cv2.setMouseCallback('Video', select_rectangle)



# Loop through video frames
while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Draw selected rectangle if available
    if selected_rectangle is not None:
        x1, y1, x2, y2 = selected_rectangle
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Detect circle in selected area
        if rectangle_selected:
            radius = detect_circle(frame, selected_rectangle)
            if radius is not None:
                print("Radius:", radius)

    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



# Release resources
cap.release()
cv2.destroyAllWindows()

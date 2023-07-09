# TODO convert wheel ticks to speed? here rather than in the code?

import cv2
import numpy as np

# Constants for circle detection
MIN_RADIUS = 10
MAX_RADIUS = 1000
CIRCLE_COLOR = 50
OUTLINE_THICKNESS = 1

# Global variables for rectangle selection
start_point = None
end_point = None
rectangle_selected = False

# Mouse callback function for rectangle selection
def select_rectangle(event, x, y, flags, param):
    global start_point, end_point, rectangle_selected

    if event == cv2.EVENT_LBUTTONDOWN:
        start_point = (x, y)
        rectangle_selected = False
    elif event == cv2.EVENT_LBUTTONUP:
        end_point = (x, y)
        rectangle_selected = True

# Function to detect circle in the selected area
def detect_circle(frame, rect):
    x1, y1, x2, y2 = rect
    roi = frame[y1:y2, x1:x2]  # Extract the region of interest

    contours, _ = cv2.findContours(roi, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        print(contour)
        area = cv2.contourArea(contour)

        (x, y), radius = cv2.minEnclosingCircle(contour)
        center = (int(x) + x1, int(y) + y1)  # Calculate the center coordinates in the original frame

        if area > MIN_RADIUS ** 2 * np.pi and area < MAX_RADIUS ** 2 * np.pi:
            # Draw circle outline
            cv2.circle(frame, center, int(radius), CIRCLE_COLOR, OUTLINE_THICKNESS)

            return int(radius)


    return None

# Load video file
video_path = '../data/mouse_video_pupil_alex.h264'
cap = cv2.VideoCapture(video_path)

# Create window and set mouse callback
cv2.namedWindow('Video')
cv2.setMouseCallback('Video', select_rectangle)

# Loop through video frames
while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to read frame from the video")
        break

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, frame_thresh = cv2.threshold(frame_gray, 60, 255, cv2.THRESH_BINARY)

    if not ret:
        print("Error: Failed to convert frame to grayscale and threshold")
        break

    # Draw selected rectangle if available
    if start_point is not None and end_point is not None:
        cv2.rectangle(frame, start_point, end_point, (0, 255, 0), 2)

        # Detect circle in selected area
        if rectangle_selected:
            x1, y1 = start_point
            x2, y2 = end_point
            rect = (x1, y1, x2, y2)
            radius = detect_circle(frame_thresh, rect)
            if radius is not None:
                print("Radius:", radius)

    cv2.imshow('Video', frame_thresh)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()

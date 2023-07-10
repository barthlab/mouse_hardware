# TODO convert wheel ticks to speed? here rather than in the code?

import sys

import cv2



# Constants for circle detection
MIN_RADIUS = 15
MAX_RADIUS = 100
GRAYSCALE_THRESHOLD = 58
DEBUG_CIRCLE_COLOR = 50
OUTLINE_THICKNESS = 1



# Global variables for rectangle selection
point_a = None
point_b = None
rectangle_selected = False



def select_rectangle(event, x, y, flags, param):
    global point_a, point_b, rectangle_selected

    if not rectangle_selected:
        if event == cv2.EVENT_LBUTTONDOWN:
            point_a = (x, y)
        elif event == cv2.EVENT_LBUTTONUP:
            point_b = (x, y)
            rectangle_selected = True



def detect_circle(frame, point_a, point_b):
    (x1, y1), (x2, y2) = point_a, point_b
    # Extract the region of interest
    roi = frame[y1:y2, x1:x2]

    contours, _ = cv2.findContours(roi, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)

        (x, y), radius = cv2.minEnclosingCircle(contour)

        # Calculate the center coordinates in the original frame
        center = (int(x) + x1, int(y) + y1)

        if MIN_RADIUS < radius and radius < MAX_RADIUS:
            return (center, radius)

    return None, -1



def process_capture(capture):
    # Default
    ret1 = False

    # Grab the frame
    ret0, frame = capture.read()

    # If frame successfully grabbed
    if ret0:
        # Process frame into grayscale
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Process frame into binary threshold
        ret1, frame = cv2.threshold(frame, GRAYSCALE_THRESHOLD, 255, cv2.THRESH_BINARY)

    return(ret0, ret1, frame)



def main():
    # Input vars
    debug = True
    video_path = '../data/mouse_video_pupil_alex.h264'

    # Load video file
    cap = cv2.VideoCapture(video_path)

    # Get 100th frame to display preview
    for _ in range(100):
        ret0, ret1, frame = process_capture(cap)
        if not (ret0 and ret1):
            sys.exit("Error parsing video")

    # Make preview window to get region of interest
    cv2.namedWindow("Preview")
    cv2.imshow("Preview", frame)
    cv2.setMouseCallback("Preview", select_rectangle)

    # Wait until we have our region of interest
    while not rectangle_selected:
        cv2.waitKey(1)

    # Clear
    cv2.destroyAllWindows()


    # Because the old cap had the first 100 frames dropped
    cap = cv2.VideoCapture(video_path)

    # Loop through video frames
    while True:
        ret0, ret1, frame = process_capture(cap)

        if not ret0:
            print("Error: Failed to read frame from the video")
            break

        if not ret1:
            print("Error: Failed to threshold frame")
            break

        # Draw selected rectangle
        cv2.rectangle(frame, point_a, point_b, (0, 255, 0), 2)

        center, radius = detect_circle(frame, point_a, point_b)

        if radius != -1:
            cv2.circle(frame, center, int(radius), DEBUG_CIRCLE_COLOR, OUTLINE_THICKNESS)

        if debug:
            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


    # Release resources
    cap.release()
    cv2.destroyAllWindows()



if "__main__" == __name__:
    main()

import argparse
import csv
import sys

import cv2
import tkinter as tk
from tkinter import filedialog



# Constants for circle detection
MIN_RADIUS = 15
MAX_RADIUS = 100
GRAYSCALE_THRESHOLD = 58
DEBUG_CIRCLE_COLOR = 50
OUTLINE_THICKNESS = 1



def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path



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
            return(center, radius)

    return(None, None)



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
        # Any pixel over the GRAYSCALE_THRESHOLD will be turned to 255 (black)
        ret1, frame = cv2.threshold(frame, GRAYSCALE_THRESHOLD, 255, cv2.THRESH_BINARY)

    return(ret0, ret1, frame)



def save_to_csv(radius_values_path, radius_list):
    with open(radius_values_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Time", "Radius"])

        for row in radius_list:
            writer.writerow(row)



def main(debug, video_path, radius_path, preview_frame_num):
    # Load video file
    cap = cv2.VideoCapture(video_path)

    # Get the preview frame
    for _ in range(preview_frame_num):
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

    cv2.namedWindow("Video")

    # Because the old cap had the first 100 frames dropped
    cap = cv2.VideoCapture(video_path)

    time_radius_list = []
    time_base = 1 / cap.get(cv2.CAP_PROP_FPS)
    frame_count = -1

    # Loop through video frames
    while True:
        frame_count += 1
        ret0, ret1, frame = process_capture(cap)

        if not ret0:
            print("Error: Failed to read frame from the video")
            break

        if not ret1:
            print("Error: Failed to threshold frame")
            break

        # Get circle and time
        center, radius = detect_circle(frame, point_a, point_b)
        time_in_video = frame_count * time_base
        time_radius_list.append([time_in_video, radius])

        if debug:
            # Draw selected rectangle
            cv2.rectangle(frame, point_a, point_b, (0, 255, 0), 2)

            # Draw circle if found
            if radius is not None:
                cv2.circle(frame, center, int(radius), DEBUG_CIRCLE_COLOR, OUTLINE_THICKNESS)

            cv2.imshow("Video", frame)
            cv2.waitKey(1)

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

    # Save radius values to CSV file
    save_to_csv(radius_path, time_radius_list)



if "__main__" == __name__:
    parser = argparse.ArgumentParser(description="Circle Detection")
    parser.add_argument("--no_debug", action="store_true", help="Disable debug mode")
    parser.add_argument("--video_path", type=str, help="Path to video file")
    parser.add_argument("--radius_path", type=str, help="Path to write radius data")
    parser.add_argument("--preview_frame_num", type=int, default=100, help="Frame number to preview")
    args = parser.parse_args()

    if args.video_path is None:
        args.video_path = select_file()

    if args.radius_path is None:
        args.radius_path = args.video_path.replace("mouse_video_", "pupil_data_").replace(".h264", ".csv")

    main(not args.no_debug, args.video_path, args.radius_path, args.preview_frame_num)


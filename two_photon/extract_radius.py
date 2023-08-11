#!/bin/env python3

import argparse
import csv
import sys

import cv2
import tkinter as tk
from tkinter import filedialog



# Constants for circle detection
MIN_RADIUS = 8
MAX_RADIUS = 100
GRAYSCALE_THRESHOLD = 90
DEBUG_CIRCLE_COLOR = 50
OUTLINE_THICKNESS = 1



# Global variable for clicked point
clicked_point = None

def on_mouse_click(event, x, y, flags, param):
    global clicked_point
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_point = (x, y)



def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path



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



def detect_closest_circle(frame, clicked_point):
    if clicked_point is None:
        return None, None

    contours, _ = cv2.findContours(frame, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    closest_center = None
    closest_radius = None
    min_distance = float('inf')

    for contour in contours:
        (x, y), radius = cv2.minEnclosingCircle(contour)
        distance = cv2.norm((x, y), clicked_point)

        if MIN_RADIUS < radius < MAX_RADIUS and distance < min_distance:
            min_distance = distance
            closest_center = (int(x), int(y))
            closest_radius = radius

    return closest_center, closest_radius



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
    cv2.setMouseCallback("Preview", on_mouse_click)

    # Wait until we have our region of interest
    while None == clicked_point:
        cv2.waitKey(1)

    # Clear
    cv2.destroyAllWindows()

    cv2.namedWindow("Video")

    time_radius_list = []
    time_base = 1 / cap.get(cv2.CAP_PROP_FPS)
    frame_count = -1

    while True:
        frame_count += 1
        ret0, ret1, frame = process_capture(cap)

        if not ret0 or not ret1:
            print("Error: Failed to read frame from the video")
            break

        center, radius = detect_closest_circle(frame, clicked_point)
        time_in_video = frame_count * time_base
        time_radius_list.append([time_in_video, radius])

        if debug:
            if center is not None:
                cv2.circle(frame, center, int(radius), DEBUG_CIRCLE_COLOR, OUTLINE_THICKNESS)

            cv2.imshow("Video", frame)
            cv2.waitKey(1)

    cap.release()
    cv2.destroyAllWindows()

    save_to_csv(radius_path, time_radius_list)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect a mouse's pupil radius given video of a mouse")
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


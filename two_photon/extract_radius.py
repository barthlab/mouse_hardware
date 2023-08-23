#!/bin/env python3

import argparse
import csv
import sys

import numpy as np
import cv2
import tkinter as tk
from tkinter import filedialog



# Constants for circle detection
MIN_RADIUS = 3
MAX_RADIUS = 35
DEBUG_CIRCLE_COLOR = 0
DEBUG_CIRCLE_THICKNESS = 1



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
    # Grab the frame
    ret0, frame = capture.read()

    # If frame successfully grabbed
    if ret0:
        # Process frame into grayscale
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    return(ret0, frame)



def detect_circle(frame, clicked_point, fill_diff_threshold):
    if clicked_point is None:
        return frame, None, None

    height, width = frame.shape[:2]
    mask = np.zeros((height + 2, width + 2), np.uint8)

    # Perform flood fill starting from the clicked point
    cv2.floodFill(frame, mask, seedPoint=clicked_point, newVal=(255, 255, 255), loDiff=(fill_diff_threshold, fill_diff_threshold, fill_diff_threshold), upDiff=(fill_diff_threshold, fill_diff_threshold, fill_diff_threshold))

    # get the contour for the clicked point
    contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    closest_center = None
    closest_radius = None
    min_distance = float('inf')

    # if there are somehow multiple contours, we get the closest one
    # if there are no contours, return frame, None, None
    # if there are contours, but they are too large/small return frame, None, None
    for contour in contours:

        (x, y), radius = cv2.minEnclosingCircle(contour)
        distance = cv2.norm((x, y), clicked_point)

        if MIN_RADIUS < radius < MAX_RADIUS and distance < min_distance:
            min_distance = distance
            closest_center = (int(x), int(y))
            closest_radius = radius

    return frame, closest_center, closest_radius



def save_to_csv(radius_values_path, radius_list):
    with open(radius_values_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["time", "radius"])

        for row in radius_list:
            writer.writerow(row)



def main(video_path, radius_path, fill_diff_threshold):
    global clicked_point

    cap = cv2.VideoCapture(video_path)

    cv2.namedWindow("Video")
    cv2.setMouseCallback("Video", on_mouse_click)

    time_radius_list = []
    time_base = 1 / cap.get(cv2.CAP_PROP_FPS)
    frame_count = -1

    while True:

        frame_count += 1
        ret0, frame = process_capture(cap)

        if not ret0:
            print("Error: Failed to read frame from the video")
            break

        mask, center, radius = detect_circle(frame, clicked_point, fill_diff_threshold)

        while center is None:
            mask, center, radius = detect_circle(frame, clicked_point, fill_diff_threshold)
            cv2.imshow("Video", mask)
            cv2.waitKey(1)

        time_in_video = frame_count * time_base
        time_radius_list.append([time_in_video, radius])

        cv2.circle(frame, center, int(radius), DEBUG_CIRCLE_COLOR, DEBUG_CIRCLE_THICKNESS)

        cv2.imshow("Video", frame)
        cv2.waitKey(1)


    cap.release()
    cv2.destroyAllWindows()

    save_to_csv(radius_path, time_radius_list)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect a mouse's pupil radius given video of a mouse")
    parser.add_argument("--video_path", type=str, help="Path to video file")
    parser.add_argument("--radius_path", type=str, help="Path to write radius data")
    parser.add_argument("--fill_diff_threshold", default=4, type=int, help="Threshold for the difference in pixel values [0, 255]")
    args = parser.parse_args()

    if args.video_path is None:
        args.video_path = select_file()

    if args.radius_path is None:
        args.radius_path = args.video_path.replace("mouse_video_", "pupil_data_").replace(".h264", ".csv")

    main(args.video_path, args.radius_path, args.fill_diff_threshold)


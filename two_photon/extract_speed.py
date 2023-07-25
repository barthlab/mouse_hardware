#!/bin/env python3

import argparse
import csv



WHEEL_PERIMETER = 46.5 / 100 # Meters
ENCODER_DIVISIONS = 1250 # Divisions



def extract_speeds_from_distance_marker_times(times):
    num_datapoints = len(times)
    time_diffs = [times[i + 1] - times[i] for i in range(num_datapoints - 1)]
    speeds = [WHEEL_PERIMETER / ENCODER_DIVISIONS / time_diffs[i] for i in range(num_datapoints - 1)]
    return speeds



def save_to_csv(speed_path, time_speed_list):
    with open(speed_path, "w+", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Time", "Speed"])

        for time, speed in time_speed_list:
            writer.writerow([time, speed])



def main(times_path, speed_path):
    with open(times_path, "r") as file:
        reader = csv.reader(file)
        times = [float(row[0]) for row in reader]

    speeds = extract_speeds_from_distance_marker_times(times)
    save_to_csv(speed_path, zip(times, speeds))



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert the time that the mouse moved a certain distance to the speed")
    parser.add_argument("--distance_path", required=True, type=str, help="Path to distance data file")
    args = parser.parse_args()

    main(args.distance_path, args.distance_path.replace("distance_data_", "speed_data_"))

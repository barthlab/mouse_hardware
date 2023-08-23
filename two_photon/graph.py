#!/bin/env python3

import argparse
import matplotlib.pyplot as plt
import csv
import constants

SAVE_DIR = "../data/"



def main():
    parser = argparse.ArgumentParser(description="Process data and create plots.")
    parser.add_argument("name", help="Name for data files")
    args = parser.parse_args()

    name = args.name
    ttl_data_path = f"{SAVE_DIR}{constants.TTL_PREFIX}{name}.csv"
    puff_file_path = f"{SAVE_DIR}{constants.PUFF_PREFIX}{name}.csv"
    lick_file_path = f"{SAVE_DIR}{constants.LICK_PREFIX}{name}.csv"
    speed_file_path = f"{SAVE_DIR}{constants.SPEED_PREFIX}{name}.csv"
    pupil_data_path = f"{SAVE_DIR}{constants.PUPIL_PREFIX}{name}.csv"

    # The rest of your code remains unchanged
    speed_times = []
    speed_values = []

    # Read speed data from CSV file
    with open(speed_file_path, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        headers = next(csv_reader)
        for row in csv_reader:
            if len(row) >= 2 and row[0] and row[1]:
                speed_times.append(float(row[0]))
                speed_values.append(float(row[1]))


    puff_times = []
    puff_types = []

    # Read "puff" times from CSV file
    with open(ttl_data_path, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for row in csv_reader:
            if len(row) >= 2:
                puff_time = float(row[1])
                puff_times.append(puff_time)

    # Read "puff" types from CSV file
    with open(puff_file_path, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for row in csv_reader:
            if len(row) >= 2:
                puff_type = row[0]
                puff_types.append(puff_type)


    lick_on_times = []
    lick_off_times = []

    # Read lick data from CSV file
    with open(lick_file_path, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            if len(row) == 2:
                signal_type = row[0]
                timestamp = float(row[1])
                if "start" == signal_type:
                    lick_on_times.append(lick_on_time)

                elif "stop" == signal_type:
                    lick_off_times.append(lick_off_time)

                else:
                    raise ValueError(f"error: Unknown signal type {signal_type} at timestamp {timestamp}")


    pupil_times = []
    pupil_sizes = []

    # Read data from CSV file
    with open(pupil_data_path, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        headers = next(csv_reader)
        for row in csv_reader:
            if len(row) >= 2 and row[0] and row[1]:
                pupil_times.append(float(row[0]))
                pupil_sizes.append(float(row[1]))


    speed_times = list(map(lambda x: (x - puff_times[0]) / 1e3, speed_times))
    lick_on_times = list(map(lambda x: (x - puff_times[0]) / 1e3, lick_on_times))
    lick_off_times = list(map(lambda x: (x - puff_times[0]) / 1e3, lick_off_times))


    # Create the plot
    plt.figure(figsize=(12, 8))  # Adjust the figure size as needed

    # Subplot 1: Pupil Data
    plt.subplot(3, 1, 1)  # 3 rows, 1 column, subplot 1
    plt.plot(pupil_times, pupil_sizes, linestyle="-", color="b", label="Pupil Data")
    plt.title(name)
    plt.xlabel(headers[0])
    plt.ylabel(headers[1])
    plt.grid(True)
    plt.legend()

    # Plot vertical lines for "puff" times with appropriate colors
    for i, puff_time in enumerate(puff_times[1:]):
        if puff_types[i] == "real":
            line_color = 'g'  # Green for real puffs
        else:
            line_color = 'r'  # Red for fake puffs
        plt.axvline(x=(puff_time - puff_times[0]) / 1e3, color=line_color, linestyle='--')


    # Subplot 2: Speed Data
    plt.subplot(3, 1, 2, sharex=plt.gca())  # 3 rows, 1 column, subplot 2
    plt.plot(speed_times, speed_values, linestyle="-", color="r", label="Speed Data")
    plt.xlabel(headers[0])  # Assuming "time" is the header for x-axis
    plt.ylabel("Speed")
    plt.grid(True)
    plt.legend()

    # Plot vertical lines for "puff" times with appropriate colors
    for i, puff_time in enumerate(puff_times[1:]):
        if puff_types[i] == "real":
            line_color = 'g'  # Green for real puffs
        else:
            line_color = 'r'  # Red for fake puffs
        plt.axvline(x=(puff_time - puff_times[0]) / 1e3, color=line_color, linestyle='--')


    # Subplot 3: Lick Data
    plt.subplot(3, 1, 3, sharex=plt.gca())  # 3 rows, 1 column, subplot 3
    plt.plot(lick_on_times, [1] * len(lick_on_times), marker="o", linestyle="", color="r", label="Lick On")
    plt.plot(lick_off_times, [0] * len(lick_off_times), marker="x", linestyle="", color="g", label="Lick Off")
    plt.xlabel("Time")
    plt.ylabel("Lick Sensor State")
    plt.grid(True)
    plt.legend()


    # Plot vertical lines for "puff" times with appropriate colors
    for i, puff_time in enumerate(puff_times[1:]):
        if puff_types[i] == "real":
            line_color = 'g'  # Green for real puffs
        else:
            line_color = 'r'  # Red for fake puffs
        plt.axvline(x=(puff_time - puff_times[0]) / 1e3, color=line_color, linestyle='--')


    # Adjust spacing between subplots
    plt.tight_layout()

    # Show the plot
    plt.show()



if __name__ == "__main__":
    main()

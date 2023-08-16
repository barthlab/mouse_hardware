#!/bin/env python3

import matplotlib.pyplot as plt
import csv

import constants

SAVE_DIR = "../data/"

name = "alex_with_air" # TODO make command line parameter
ttl_data_path = f"{SAVE_DIR}{constants.TTL_PREFIX}ttl_data_{name}.csv"
puff_file_path = f"{SAVE_DIR}{constants.PUFF_PREFIX}{name}.csv"
dist_file_path = f"{SAVE_DIR}{constants.DIST_PREFIX}{name}.csv"
lick_file_path = f"{SAVE_DIR}{constants.LICK_PREFIX}{name}.csv"
pupil_data_path = f"{SAVE_DIR}{constants.PUPIL_PREFIX}{name}.csv"

puff_times = []
puff_types = []

# Read "puff" times from CSV file
with open(ttl_data_path, "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip the header row
    for row in csv_reader:
        if len(row) >= 2:
            puff_time = float(row[1])
            puff_times.append(puff_time)

# Read "puff" types from CSV file
with open(puff_file_path, "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        if len(row) >= 2:
            puff_type = row[0]
            puff_types.append(puff_type)

x_data = []
y_data = []

# Read data from CSV file
with open(pupil_data_path, "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    headers = next(csv_reader)  # Read the headers from the first row
    for row in csv_reader:
        if len(row) >= 2 and row[0] and row[1]:
            x_data.append(float(row[0]))
            y_data.append(float(row[1]))

# Create the plot
plt.figure(figsize=(10, 6))  # Adjust the figure size as needed
plt.plot(x_data, y_data, linestyle="-", color="b", label="Data")
plt.title(name)
plt.xlabel(headers[0])
plt.ylabel(headers[1])

# Plot vertical lines for "puff" times with appropriate colors
for i, puff_time in enumerate(puff_times[1:]):
    if puff_types[i] == "real":
        line_color = 'g'  # Green for real puffs
    else:
        line_color = 'r'  # Red for fake puffs
    plt.axvline(x=(puff_time - puff_times[0]) / 1e3, color=line_color, linestyle='--')

plt.legend()
plt.grid(True)

# Show the plot
plt.show()

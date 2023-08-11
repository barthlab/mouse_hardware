#!/bin/env python3

import matplotlib.pyplot as plt
import csv

# Replace "your_csv_file.csv" with the actual path to your CSV file
name = "alex_with_air"
csv_file_path = f"../data/pupil_data_{name}.csv"
csv_file_path_2 = f"../data/pupil_data_{name}.csv"

x_data = []
y_data = []

# Read data from CSV file
with open(csv_file_path, "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    headers = next(csv_reader)  # Read the headers from the first row
    for row in csv_reader:
        if len(row) >= 2 and row[0] and row[1]:
            x_data.append(float(row[0]))  # Assuming the first column contains numeric data
            y_data.append(float(row[1]))  # Assuming the second column contains numeric data

# Create the plot
plt.figure(figsize=(10, 6))  # Adjust the figure size as needed
plt.plot(x_data, y_data, linestyle="-", color="b", label="Data")
plt.title("CSV Data Plot")
plt.xlabel(headers[0])  # Use the first column name as x-axis label
plt.ylabel(headers[1])  # Use the second column name as y-axis label
plt.legend()
plt.grid(True)

# Show the plot
plt.show()

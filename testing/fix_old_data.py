#!/bin/env python3

"""
Convert all old format files to new format files
"""



import ast
import csv



original_file_name = input("what is the name of the csv file?\n")

puff_file_name = "puff_data_" + csv_file_name
run_file_name = "run_data_" + csv_file_name

with open(original_file_name, "r") as original_data_file:
    with open(puff_file_name, "w+") as puff_data_file:
        with open(run_file_name, "w+") as run_data_file:

            reader = csv.reader(original_data_file)
            puff_writer = csv.writer(puff_data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            run_writer = csv.writer(run_data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for row in reader:
                # NOTE: not safe, but as long as we run it on our own files, it's fine
                puff_writer.writerow(row[:6])
                for data in ast.literal_eval(row[6]):
                    run_writer.writerow(data)
    

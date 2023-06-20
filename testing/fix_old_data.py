#!/bin/env python3

"""
Convert all old format files to new format files
"""

import argparse
import ast
import csv
import sys



def convert_files(original_file_names):
    for original_file_name in original_file_names:
        puff_file_name = "puff_data_" + original_file_name
        run_file_name = "run_data_" + original_file_name

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

if __name__ == "__main__":
    csv.field_size_limit(sys.maxsize)

    parser = argparse.ArgumentParser(description="Convert all old format files to new format files")
    parser.add_argument("names", metavar="N", type=str, nargs="+", help="the names of the CSV files")

    args = parser.parse_args()
    original_file_names = args.names
    convert_files(original_file_names)       

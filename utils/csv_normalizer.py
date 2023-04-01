"""
This code takes an input file and an output file as arguments from the command line. It reads the input file, which has a custom delimiter |, and converts it into a CSV format and writes it to the output file.
The input file can have multiple lines, each line contains data separated by the | delimiter.
The code also checks if the last field in any row ends with a backslash, which indicates that the next line contains the continuation of the same field.
It concatenates the lines to form a complete row and then writes it to the output file in CSV format.

:arg input
:arg output

example: python csv_normalizer.py input.csv output.csv
"""

import csv
import sys

if len(sys.argv) < 3:
    print("Usage: python csv_normalizer.py input_file output_file")
    sys.exit()

input_file = sys.argv[1]
output_file = sys.argv[2]
delimiter = "|"


def _count_generator(reader):
    b = reader(1024 * 1024)
    while b:
        yield b
        b = reader(1024 * 1024)


def get_count(file_path):
    count = 0
    with open(file_path, "rb") as f:
        c_generator = _count_generator(f.raw.read)
        # count each \n
        count = sum(buffer.count(b'\n') for buffer in c_generator) + 1
    return count


count = get_count(input_file)

with open(input_file, "r") as infile:
    with open(output_file, "w") as outfile:
        writer = csv.writer(outfile)

        row_buffer = ""
        line = infile.readline().strip()
        i = 1
        while line != "" and i <= count:
            if line.endswith("\\"):
                row_buffer += line[:-1]
            else:
                row_buffer += line

                row = row_buffer.split(delimiter)
                writer.writerow(row)
                row_buffer = ""

            line = ""
            while line == "" and i <= count:
                line = infile.readline().strip()
                i += 1

        if row_buffer:
            writer.writerow(row_buffer.split(delimiter))

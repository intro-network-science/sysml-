import csv
import sys

if len(sys.argv) < 3:
    print("Usage: python convert.py input_file output_file")
    sys.exit()

input_file = sys.argv[1]
output_file = sys.argv[2]
delimiter = "|"

with open(input_file, "r") as infile:
    with open(output_file, "w") as outfile:
        writer = csv.writer(outfile)

        row_buffer = ""
        line = infile.readline().strip()
        while line or row_buffer:
            if line and line.endswith("\\"):
                row_buffer += line[:-1]
            elif line or row_buffer:
                row_buffer += line

                row = row_buffer.split(delimiter)
                writer.writerow(row)
                row_buffer = ""

            line = infile.readline().strip()

        if row_buffer:
            writer.writerow(row_buffer.split(delimiter))

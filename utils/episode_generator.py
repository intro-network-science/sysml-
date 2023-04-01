"""
This script takes in multiple input CSV files, an output file path, and a bucket length as command line arguments.

:arg input_files
:arg output_file
:arg bucket_length

example: python episode_generator.py input1.csv input2.csv output.json 3

It reads each input file, and for each author in the file, creates a list of indices of rows in the CSV file where that author appears.
These lists are then split into "buckets" of the specified length, with the default value of each bucket set to -1.

The results are written out to a JSON file with the specified output file path.

If the command line arguments are not provided correctly, the script will print an error message and exit with a status code of 1.
Finally, it prints a message indicating where the output was written.
"""

import csv
import json
import os
import sys

if len(sys.argv) < 4:
    print("Error: Input files name, output file name, or bucket length not provided.")
    sys.exit(1)

input_files = [sys.argv[i] for i in range(1, len(sys.argv) - 2)]
output_file = sys.argv[-2]
bucket_length = int(sys.argv[-1])

results = {}
for input_file in input_files:
    with open(input_file, 'r') as infile:
        reader = csv.DictReader(infile)

        author_indices = {}

        for i, row in enumerate(reader):
            author = row['author']

            if author in author_indices:
                author_indices[author].append(i)
            else:
                author_indices[author] = [i]

        for author in author_indices:
            indices = author_indices[author]
            num_buckets = (len(indices) + bucket_length - 1) // bucket_length
            author_buckets = [[-1] * bucket_length for _ in range(num_buckets)]
            for i, idx in enumerate(indices):
                bucket_idx = i // bucket_length
                inner_idx = i % bucket_length
                author_buckets[bucket_idx][inner_idx] = idx
            author_indices[author] = author_buckets

        results[os.path.splitext(os.path.basename(input_file))[0]] = author_indices

with open(output_file, 'w') as outfile:
    json.dump(results, outfile)

print(f"Output written to {output_file}")

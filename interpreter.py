#!/usr/bin/env python3
import csv
import ast  #for reading the printed list into a list object
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("file", help="a file output from cleaner.py")
args = parser.parse_args()

def csvreader(file):
    wdict = {}
    with open(file, "r", newline="") as filehandle:
        reader = csv.reader(filehandle, delimiter='\t')
        for row in reader:
            key = row[0]
            if key == 'None':
                continue
            value = ast.literal_eval(row[1])
            wdict[key] = value

    return wdict

csvreader(args.file)

#!/usr/bin/env python3
#cleans file from palm analyzer and makes a single entry for each gene ID
#with its related GO terms
#need to ensure that ATH_GO_GOSLIM file in present
import argparse
import os
import csv
from datetime import date
parser = argparse.ArgumentParser()
parser.add_argument("-i", help="file from palm analyzer")
parser.add_argument("-n", help="name for saved file")
args = parser.parse_args()


pos_ids = set()
try:
    with open(args.i, "r") as handle:
        lines = handle.readlines()
        for line in lines:
            sep = line.split('\t')
            if sep[0] == 'ID':
                continue
            idcolumn = sep[0]
            splitcolumn = idcolumn.split('|')
            geneid = splitcolumn[0][:9]
            pos_ids.add(geneid)
except IOError as err:
    print(err)
print("IDs collected from css palm output file")
idwithterms = {}
for key in pos_ids:
    idwithterms.setdefault(key, [])

try:
    with open("ATH_GO_GOSLIM.txt", 'r') as file:
        athlines = file.readlines()
        for line in athlines:
            if line.startswith('!'):
                continue
            else:
                for key in pos_ids:
                    if line.startswith(key):
                        l = line.split('\t')
                        q = l[5]
                        idwithterms[key].append(q)
except IOError:
    print("error getting go terms")
print("GO terms for ids collected")

idlistformat = []
for key in idwithterms:
    entry = []
    entry.append(key)
    entry.append(idwithterms[key])
    idlistformat.append(entry)

filename = "{}_cleaned{}.csv".format(args.n, date.today())
try:
    with open(filename, 'w', newline='') as handle:
        filewriter = csv.writer(handle, delimiter='\t', quotechar='|')
        for entry in idlistformat:
            filewriter.writerow(entry)
except IOError as err:
    print('error writing to savefile')

print("file saved")

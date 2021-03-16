#!/usr/bin/env python


import argparse
import Bio.SeqIO

parser = argparse.ArgumentParser(description="get fasta sequences")
parser.add_argument("--file", "-f", help="file list of genes ids")
parser.add_argument("--output", "-o", help="name of output file")
args = parser.parse_args()

names = []  #list of gene names to get sequences for
dict = {}   #key = ID, value = the record object
records = []    #collection of the wanted fasta records to be sent to writer
try:
    with open(args.file) as file:
        lines = file.readlines()
        for name in lines:
            names.append(name.rstrip('\n'))
except IOError:
    print("error reading file")
for record in Bio.SeqIO.parse("Araport11_genes.201606.pep.fasta", "fasta"):
    dict.setdefault(record.id, record)  #insert seqrecord objects into dictionary for quick sorting
for protein in names:
    records.append(dict[protein])   #add seqrecord object to records list
fastaname = "{}.fasta".format(args.output)
Bio.SeqIO.write(records, fastaname, "fasta")

#!/usr/bin/env python
import sys
from Bio import GenBank
import os
import re


def get_gbfiles_via_naming_conv(directory):
    fn_pat = re.compile(r"^records-(\d)+.gb$")
    fn_list = []
    sortable = []
    for fn in os.listdir(directory):
        if not os.path.isfile(fn):
            continue
        m = fn_pat.match(fn)
        if m:
            sortable.append((int(m.group(1)), fn))
    sortable.sort()
    fn_list = [i[1] for i in sortable]
    return fn_list

def scan_metadata_in_file(filepath):
    with open(filepath) as handle:
        for record in GenBank.parse(handle):
            print(record.source)
            for feat in record.features:
                if feat.key == "source":

                    print(feat.__dict__)
            sys.exit("early\n")

def main(fn_list):
    if fn_list is None:
        msg ="No input file name supplied, assuming records-#.gb naming convention in cwd.\n"
        sys.stderr.write(msg)
        fn_list = get_gbfiles_via_naming_conv(os.curdir)
        if not fn_list:
            sys.exit("No input files found.\n")
    for fn in fn_list:
        if not os.path.isfile(fn):
            sys.exit(f'"{fn}" does not exist or is not a file.\n')
        scan_metadata_in_file(fn)



if __name__ == "__main__":
    if len(sys.argv) == 1:
        main(None)
    else:
        main(sys.argv[1:])

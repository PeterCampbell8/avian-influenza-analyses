#!/usr/bin/env python3
import sys
from Bio import GenBank
import os
import re
import argparse

KNOWN_KEY_LIST = """/collection_date=
/bio_material=
/lab_host=
/db_xref=
/organism=
/PCR_primers=
/country=
/note=
/isolation_source=
/tissue_type=
/mol_type=
/collected_by=
/clone=
/lat_lon=
/strain=
/segment=
/identified_by=
/isolate=
/map=
/culture_collection=
/host=
/serotype=
/chromosome="""
KNOWN_KEYS = set(KNOWN_KEY_LIST.split("\n"))
KNOWN_CLEANED_KEYS = set([i[1:-1] for i in KNOWN_KEYS])


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


ORG_SRC_CROSSCHECK = False
no_org = 0
COUNTRY_SRC_CROSSCHECK = False
STRAIN_CROSSCHECK = False


def cleaned_val(key, qual_dict):
    rval = qual_dict.get(key)
    if rval is None:
        return None
    assert rval.startswith('"') and rval.endswith('"')
    return rval[1:-1]


def scan_metadata_in_file(filepath, key_list_vals=None):
    global no_org
    if key_list_vals is not None:
        dec_key = f"/{key_list_vals}="

    with open(filepath) as handle:
        for record in GenBank.parse(handle):
            # print(record.source)
            for feat in record.features:
                if feat.key == "source":
                    # qualifier keys seem uniq in the source FEATURE
                    qdict = {q.key: q.value for q in feat.qualifiers}
                    keyset = set(qdict.keys())
                    if not keyset.issubset(KNOWN_KEYS):
                        for k in keyset:
                            if k not in KNOWN_KEYS:
                                sys.stderr(f'Unknown key "{k}"\n')
                            raise RuntimeError(f"Unknown keys in {record.accession}")
                    if key_list_vals is not None and dec_key in qdict:
                        print(qdict[dec_key])
                    if ORG_SRC_CROSSCHECK:
                        oval = cleaned_val("/organism=", qdict)
                        if oval is not None:
                            if oval != record.source:
                                sys.stderr.write(
                                    f"mismatch {repr(oval)} != {repr(record.source)} for {record.accession}\n"
                                )
                        else:
                            no_org += 1
                    if COUNTRY_SRC_CROSSCHECK:
                        cval = cleaned_val("/country=", qdict)
                        if cval is not None:
                            if cval not in record.source:
                                sys.stderr.write(
                                    f"mismatch {repr(cval)} != {repr(record.source)} for {record.accession}\n"
                                )
                    if STRAIN_CROSSCHECK:
                        sval = cleaned_val("/strain=", qdict)
                        if sval is not None:
                            if sval not in record.source:
                                sys.stderr.write(
                                    f"mismatch {repr(sval)} != {repr(record.source)} for {record.accession}\n"
                                )

            # sys.exit("early\n")


def main_parsed(fn_list, key_list_vals=None):
    if fn_list is None:
        msg = "No input file name supplied, assuming records-#.gb naming convention in cwd.\n"
        sys.stderr.write(msg)
        fn_list = get_gbfiles_via_naming_conv(os.curdir)
        if not fn_list:
            sys.exit("No input files found.\n")
    for fn in fn_list:
        if not os.path.isfile(fn):
            sys.exit(f'"{fn}" does not exist or is not a file.\n')
        scan_metadata_in_file(fn, key_list_vals=key_list_vals)
    if ORG_SRC_CROSSCHECK:
        sys.stderr.write(f"{no_org} records with no organism qualifiers")


def main():

    parser = argparse.ArgumentParser(
        prog="genbank_metadata_scanner",
        description="Reads genbank records and examines fields that might be of interest for understanding the source of samples",
    )
    parser.add_argument(
        "filenames",
        nargs="*",
        help="filenames or none to use default naming convention",
    )
    parser.add_argument(
        "--key-list-vals",
        dest="key_list_vals",
        type=str,
        choices=KNOWN_CLEANED_KEYS,
        default=None,
    )
    args = parser.parse_args()
    fn_list = args.filenames
    if not fn_list:
        fn_list = None
    main_parsed(fn_list, key_list_vals=args.key_list_vals)


if __name__ == "__main__":
    main()

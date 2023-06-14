#!/usr/bin/env python3
"""
Based on code from
  https://www.biostars.org/p/66921/#188448 by Eli Korvigo
"""
import sys
from Bio import Entrez
import os
import time

entrez_email = os.environ.get("ENTREZ_EMAIL")
if entrez_email:
    Entrez.email = entrez_email

RETMAX = 10 ** 9


def batch_query(accessions_batch, db="nucleotide", retmax=RETMAX, batchsize=500):
    # get GI for query accessions
    query = " ".join(accessions_batch)
    query_handle = Entrez.esearch(db=db, term=query, retmax=retmax)
    gi_list = Entrez.read(query_handle)["IdList"]
    query_handle.close()
    # get GB files
    search_handle = Entrez.epost(db=db, id=",".join(gi_list))
    try:
        search_results = Entrez.read(search_handle)
    except:
        sys.stderr.write(f"query={query}\ngi_list={gi_list}\n\nsearch_handle={search_handle}\n")
        raise
    webenv, query_key = search_results["WebEnv"], search_results["QueryKey"]
    records_handle = Entrez.efetch(
        db=db, rettype="gb", retmax=batchsize, webenv=webenv, query_key=query_key
    )
    return records_handle


def batch(accessions, size=500):
    l = len(accessions)
    for start in range(0, l, size):
        yield accessions[start : min(start + size, l)]


def main(acc_fp):
    batchsize = 500
    err = sys.stderr
    verbose = True

    acc_list = []
    with open(acc_fp, "r") as inp:
        tmp = [i.strip() for i in inp]
        acc_list = [i for i in tmp if i]  # skip empty lines
    if not acc_list:
        raise RuntimeError("No accessions found")
    rec_ind = 1
    first = True
    for abatch in batch(acc_list, size=batchsize):
        ofn = f"records-{rec_ind}.gb"
        if os.path.exists(ofn):
            err.write(f"Skipping redownload of {ofn} ...\n")
            rec_ind += len(abatch)
            continue
        if not first:
            err.write(f"Sleeping...\n")
            time.sleep(20)
        first = False
        if verbose:
            err.write(f"Fetching records {rec_ind} to {len(abatch) + rec_ind}\n")
        rec_ind += len(abatch)
        records = batch_query(abatch, batchsize=batchsize)
        tfn = f".tmp-{ofn}"
        try:
            with open(tfn, "w") as out:
                for line in records:
                    out.write(line)
            records.close()
        except:
            os.remove(tfn)
            raise
        else:
            os.rename(tfn, ofn)



if __name__ == "__main__":
    try:
        acc_fp = sys.argv[1]
    except:
        sys.exit("Expected 1 argument: a filepath to a list of accession numbers\n")
    main(acc_fp)

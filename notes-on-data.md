## Feature source qualifiers
From a directory with data for a gene, run a command like:

    ../../bin/genbank_metadata_scanner.py --key-list-vals=bio_material

to see all of the values for a qualifier of the `source` in `FEATURES`

  * `bio_material` followed by an sample code such as `"CEIRS#..."`  (`SCV:` and `SMMU` also seen). See https://www.niaidceirs.org/ceirs-surveillance-data/ 

  * `collection_date` sometimes just a year, sometimes `%d-%b-%Y`

  * `lab_host`: sometimes an organism common name. Some cell line IDs. sometimes # of passages. For PB2 about 15,171 of 87,095 records have something other than "NA" in this field (as of 14-Jun-2023)

  * `lat_lon` as expected "[float] {N,S} [float] {E,W}"
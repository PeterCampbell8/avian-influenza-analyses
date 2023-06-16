## Feature source qualifiers
From a directory with data for a gene, run a command like:

    ../../bin/genbank_metadata_scanner.py --key-list-vals=bio_material

to see all of the values for a qualifier of the `source` in `FEATURES`

  * `bio_material` followed by an sample code such as `"CEIRS#..."`  (`SCV:` and `SMMU` also seen). See https://www.niaidceirs.org/ceirs-surveillance-data/ 

  * `collection_date` sometimes just a year, sometimes `%d-%b-%Y`

  * `lat_lon` as expected "[float] {N,S} [float] {E,W}"
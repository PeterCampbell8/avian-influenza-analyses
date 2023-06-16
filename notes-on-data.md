## Feature source qualifiers
From a directory with data for a gene, run a command like:

    ../../bin/genbank_metadata_scanner.py --key-list-vals=bio_material

to see all of the values for a qualifier of the `source` in `FEATURES`

Frequencies below are based on 87,095 records of PB2 (all from a query of influenza A on 14-Jun-2023)

  * `bio_material` **IGNORE (for now):** followed by an sample code such as `"CEIRS#..."`  (`SCV:` and `SMMU` also seen). See https://www.niaidceirs.org/ceirs-surveillance-data/ 

  * `collection_date` sometimes just a year, sometimes `%d-%b-%Y`

  * `db_xref` in about half the entries. format `taxon:#` where the number is the NCBI taxon ID for the flu variant, e.g. https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=931543

  * `lab_host`: sometimes an organism common name. Some cell line IDs. sometimes # of passages. About 1/6 of the records have something other than "NA" in this field.

  * `lat_lon` as expected "[float] {N,S} [float] {E,W}"

  * `organism` **IGNORE:** Always present and almost always the same as top-level `SOURCE` field. In a tiny # of cases a space appears in the biopython read of a record which causes the 2 to differ.
  
  * `PCR_primers` **IGNORE**

  * `country` It's complicated. Often duplicate of the geographic info in the `SOURCE` field, sometimes more or less precise.

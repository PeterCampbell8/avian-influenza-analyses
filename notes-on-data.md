## Feature source qualifiers
From a directory with data for a gene, run a command like:

    ../../bin/genbank_metadata_scanner.py --key-list-vals=bio_material

to see all of the values for a qualifier of the `source` in `FEATURES`

Frequencies below are based on 87,095 records of PB2 (all from a query of influenza A on 14-Jun-2023)

  * `bio_material` **IGNORE (for now):** followed by an sample code such as `"CEIRS#..."`  (`SCV:` and `SMMU` also seen). See https://www.niaidceirs.org/ceirs-surveillance-data/ 

  * `clone` **IGNORE, I think** might want to check for duplicates. rarely used. 

  * `collected_by` **IGNORE**

  * `collection_date` sometimes just a year, sometimes `%d-%b-%Y`

  * `country` It's complicated. Often duplicate of the geographic info in the `SOURCE` field, sometimes more or less precise.

  * `db_xref` in about half the entries. format `taxon:#` where the number is the NCBI taxon ID for the flu variant, e.g. https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=931543

  * `isolation_source`: **IGNORE** Occassionally some host species info, but usually the anotomical location or type of substance from which the sample was extracted.

  * `lab_host`: **MAYBE IGNORE/DELETE** sometimes an organism common name. Some cell line IDs. sometimes # of passages. About 1/6 of the records have something other than "NA" in this field. We should avoid sequences from long-term passages. Perhaps worth deleting all records with something in this field.

  * `lat_lon` as expected "[float] {N,S} [float] {E,W}"

  * `mol_type` **IGNORE** "genomic DNA", "genomic RNA", "mRNA", "other RNA", "unassigned DNA" "unassigned RNA", or "viral cRNA"

  * `organism` **IGNORE:** Always present and almost always the same as top-level `SOURCE` field. In a tiny # of cases a space appears in the biopython read of a record which causes the 2 to differ.
  
  * `note` **IGNORE** potentially interesting info sometimes, but free-form text will be too hard to deal with.

  * `PCR_primers` **IGNORE**

  * `strain` Often duplicate of the strain info in `SOURCE`, but sometimes `SOURCE` lacks the strain info and it is only found here. Other times there are trivial differences. Other times, one is more precise than the other.

  * `serotype` sometimes this info is in the `SOURCE` too, but it seems more reliable here. **TODO** need to check if it is ever only in `SOURCE` or whether it is safe to just use this field.

  * `tissue_type` **IGNORE** very rarely used. Anatomical source of sample.

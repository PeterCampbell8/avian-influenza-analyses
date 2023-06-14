# avian-influenza-analyses

Large datafiles will be stored in full_data and not synced through git.


# MTH notes
## env setup 
I'm using virtualenv:

    python3 -mvenv env
    source env/bin/activate
    pip install biopython

Note that you'll have to run 

	source env/bin/activate

## Fetching data

   1. Configure and add a search query on https://www.ncbi.nlm.nih.gov/genomes/FLU/Database/nph-select.cgi
   2. Select "Nucletide accesion list" from the drop-down next to the "Download results"
   3. store the downloaded file as `full_data/{genename}/accessions.fa`
   4. https://www.ncbi.nlm.nih.gov/sites/batchentrez

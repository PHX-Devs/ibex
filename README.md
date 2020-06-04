# IBEX
Project Ibex: RNA sequence matching to save the world

## to get started...
* make sure you have a GB or two to spare on your drive
* get your hands on a file called all_sequences.txt and place it in data/source_data/human/
  * use this: curl -O https://rna-sequences.s3-us-west-1.amazonaws.com/all_sequences.txt
* run buid_sequence_db.py (will create a db in /data/db/). this will take a while, but it's reasonable
* run analyze.py (careful, this can end up taking your whole week). tip: edit the for loop parameters
* run get_result_set.py, passing an integer as an arg - maybe start with 3 or 4

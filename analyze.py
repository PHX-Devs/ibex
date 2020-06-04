import pprint
from scraper.rna_scraper import getRNASequence
from substring.substring_toolkit import allMatchingSubstrings, getRemainingSubstrings
from sequence_parser.parser import parse
from sequence_db.sequence_db import SequenceDB
from paths import db_path, cached_covid_path

if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)

    sars2 = getRNASequence("https://www.ncbi.nlm.nih.gov/nuccore/MN988668.1?report=fasta", cached_covid_path)
    db = SequenceDB(db_path)

    total_len = 0
    keys = db.fetch_sequence_ids()
    count = 0
    cursor = 0
    exit_after = 10000
    for key in keys:
        count += 1

        if (count < cursor):
            # this is a hack to pick up where we left off
            # update the cursor if you run this script for "a while" and then want to pick up where you left off
            continue

        sequence = db.fetch_sequence(key)
        substring_set = allMatchingSubstrings(sars2, sequence, 3)

        db.insert_matches(key, substring_set)

        print("iteration %s complete" % count)
        if (count >= exit_after):
            break

    print("end")

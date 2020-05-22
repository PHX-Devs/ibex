import sys
import pprint
from scraper.rna_scraper import getRNASequence
from substring.substring_toolkit import allMatchingSubstrings, getRemainingSubstrings
from sequence_parser.parser import parse
from sequence_db.sequence_db import SequenceDB
from paths import db_path, cached_covid_path

if __name__ == "__main__":
    sars2 = getRNASequence("https://www.ncbi.nlm.nih.gov/nuccore/MN988668.1?report=fasta", cached_covid_path)
    db = SequenceDB(db_path)
    substrings_from_db = db.fetch_all_matches(sys.argv[1])
    result_set = getRemainingSubstrings(sars2, substrings_from_db)

    print (result_set)
    print("end")

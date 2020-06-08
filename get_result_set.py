import sys
import pprint
from scraper.rna_scraper import getRNASequence
from substring.substring_toolkit import allMatchingSubstrings, getRemainingSubstrings
from sequence_parser.parser import parse
# from sequence_db.sequence_db import SequenceDB
from sequence_db.sequence_db_postgres import SequenceDB
from paths import db_path, cached_covid_path

from result_set import get_result_set, get_result_set_size, get_min_match_size, get_next_result_set

if __name__ == "__main__":
    min_match = sys.argv[1]
    result_set = get_result_set(min_match)
    print (result_set)
    # print ("matches in db starting at length=%s" % get_min_match_size())
    # print ("next result set: %s" % get_next_result_set())
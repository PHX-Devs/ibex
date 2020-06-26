from scraper.rna_scraper import getRNASequence
from substring.substring_toolkit import allMatchingSubstrings, getRemainingSubstrings
from sequence_parser.parser import parse
# from sequence_db.sequence_db import SequenceDB
from sequence_db.sequence_db_postgres import SequenceDB
from paths import db_path, cached_covid_path

def get_result_set_size(min_match):
    return len(get_result_set(min_match))

def get_min_match_size():
    db = SequenceDB(db_path)
    return db.get_min_match_size()

def get_result_set(min_match):
    min_in_db = get_min_match_size()
    if (min_in_db > int(min_match)):
        return []
    sars2 = getRNASequence("https://www.ncbi.nlm.nih.gov/nuccore/MN988668.1?report=fasta", cached_covid_path)
    db = SequenceDB(db_path)
    substrings_from_db = db.fetch_all_matches(min_match)
    result_set = getRemainingSubstrings(sars2, substrings_from_db, int(min_match))
    return result_set

def prune_matches(size):
    db = SequenceDB(db_path)
    db.prune_matches(size)

def get_next_result_set(min_match=1):
    # special case for length of the whole genome
    if (min_match >= 29882):
        return min_match

    # get the size of the result set for the given match size
    size = get_result_set_size(min_match)

    # if the size is > zero, we've found our result_set
    if (size > 0):
        return min_match

    # else, recurse
    else:
        return get_next_result_set(min_match+1)


import time
from scraper.rna_scraper import getRNASequence
from substring.substring_toolkit import allMatchingSubstrings, getRemainingSubstrings
from sequence_parser.parser import parse
from sequence_db.sequence_db import SequenceDB
from paths import db_path, cached_covid_path
from result_set import get_result_set, get_result_set_size, prune_matches, get_next_result_set

if __name__ == "__main__":

    sars2 = getRNASequence("https://www.ncbi.nlm.nih.gov/nuccore/MN988668.1?report=fasta", cached_covid_path)
    db = SequenceDB(db_path)

    keys = db.fetch_sequence_ids()
    count = 0
    exit_after = 10000

    count_seq_processed = int(db.get_count_sequences_processed())

    candidate_string_size = 3
    result_set_size = 999
    if (count_seq_processed > 0):
        candidate_string_size = get_next_result_set()
        result_set_size = get_result_set_size(candidate_string_size)

    for key in keys:
        count += 1
        start = time.time()

        sequence = db.fetch_sequence(key)

        substring_set = allMatchingSubstrings(sars2, sequence, candidate_string_size)

        db.insert_matches_optimized(key, substring_set)

        db.set_sequence_analyzed(key)

        print("iteration %s complete" % count)

        end = time.time()
        duration = end - start
        print("iteration duration: %s" % duration)

        if (count % 100 == 0):
            print("fetching new result set size.")
            result_set_size = get_result_set_size(candidate_string_size)
            if (result_set_size == 0):
                candidate_string_size = get_next_result_set()
                prune_matches(candidate_string_size)
                print("result set incremented to %s" % candidate_string_size)

        print("result set size: %s " % result_set_size)
        print("candidate string size: %s" % candidate_string_size)
        print("--------------------------------------")

        if (count >= exit_after):
            break

    print("end")

import sys
from tqdm import tqdm
from sequence_db.sequence_db import SequenceDB
from paths import db_path
from result_set import get_result_set

def is_sequence_viable_option(candidate_substring, sequence_keys):
    count = 0
    for key in tqdm(sequence_keys):
        count += 1
        sequence = db.fetch_sequence(key)
        if (candidate_substring in sequence):
            return False

    return True


if __name__ == "__main__":
    min_match = sys.argv[1]
    try:
        result_set = get_result_set(int(min_match))
    except:
        result_set = [sys.argv[1]]

    db = SequenceDB(db_path)
    sequence_keys = db.fetch_all_sequence_ids()

    for substring in result_set:
        print ("analyzing %s" % substring)
        print ("(%s nucleotides long)" % len(substring))
        is_viable = is_sequence_viable_option(substring, sequence_keys)
        if (is_viable):
            print ("POSITIVE (may be a viable attack surface)")
        else:
            print ("NEGATIVE")
        print("---------------------------------------------------")
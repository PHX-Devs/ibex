import sys
sys.path.append('..')
#from sequence_db.sequence_db import SequenceDB
from sequence_db.sequence_db_postgres import SequenceDB

def parse(path, db_path):
    count = 0
    db = SequenceDB(db_path)
    # sequences = {}
    temp_seq = ""
    nucleotides = ["T", "A", "G", "C"]
    with open(path, "r") as f:
        lines =  f.readlines()
        current_sequence_key = ""
        for line in lines:
            if (line.startswith(">")):
                current_sequence_key = line.split(" ")[0].split("|")[1]
                #sequences[current_sequence_key] = ""
                if current_sequence_key != "":
                    db.insert_sequence(current_sequence_key, temp_seq)
                temp_seq = ""
                count += 1
                # print("parsing sequence %i: %s" % (count, current_sequence_key))
            if (line[0] in nucleotides):
                #sequences[current_sequence_key] += line.rstrip()
                temp_seq += line.rstrip()

        if current_sequence_key != "":
            db.insert_sequence(current_sequence_key, temp_seq)

    #return sequences


def print_debug(sequences):
    print("size: %s" % len(sequences))
    print("keys: %s" % sequences.keys())
    for key, seq in sequences.items():
        print(key)
        print(seq[0:75])
        print(len(seq))
        print(" ")
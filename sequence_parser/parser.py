import sys


def parse(path):
    count = 0
    sequences = {}
    nucleotides = ["T", "A", "G", "C"]
    with open(path, "r") as f:
        lines =  f.readlines()
        current_sequence_key = ""
        for line in lines:
            if (line.startswith(">")):
                current_sequence_key = line.split(" ")[0].split("|")[1]
                sequences[current_sequence_key] = ""
                count += 1
                # print("parsing sequence %i: %s" % (count, current_sequence_key))
            if (line[0] in nucleotides):
                sequences[current_sequence_key] += line.rstrip()
    return sequences

def print_debug(sequences):
    print("size: %s" % len(sequences))
    print("keys: %s" % sequences.keys())
    for key, seq in sequences.items():
        print(key)
        print(seq[0:75])
        print(len(seq))
        print(" ")

if __name__ == "__main__":
    filename_to_parse = sys.argv[1]
    print("parsing %s" % filename_to_parse)
    sequences = parse(filename_to_parse)
    print_debug(sequences)
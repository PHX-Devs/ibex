import pprint
from scraper.rna_scraper import getRNASequence
from substring.substring_toolkit import allMatchingSubstrings, getRemainingSubstrings
from sequence_parser.parser import parse

def get_rna_sequences(urls):
    sequences = []
    for url in urls:
        sequence = getRNASequence(url)
        sequences.append(sequence)
    return sequences

if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)

    sars2 = getRNASequence("https://www.ncbi.nlm.nih.gov/nuccore/MN988668.1?report=fasta")

    human_data = parse("./input_data/format_example.txt")

    substrings = []
    total_len = 0
    for key, sequence in human_data.items():
        substrings += allMatchingSubstrings(sars2, sequence, 8)

    result_set = getRemainingSubstrings(sars2, substrings)

    print (result_set)
    print("end")

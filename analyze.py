import pprint
from scraper.rna_scraper import getRNASequence
from substring.substring_toolkit import allMatchingSubstrings, getRemainingSubstrings

def get_rna_sequences(urls):
    sequences = []
    for url in urls:
        sequence = getRNASequence(url)
        sequences.append(sequence)
    return sequences

if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)

    sars2 = getRNASequence("https://www.ncbi.nlm.nih.gov/nuccore/MN988668.1?report=fasta")

    human_urls = [
        "https://www.ncbi.nlm.nih.gov/nuccore/NM_001330348.2?report=fasta",
        "https://www.ncbi.nlm.nih.gov/nuccore/NM_001382287.1?report=fasta",
        "https://www.ncbi.nlm.nih.gov/nuccore/NM_004731.5?report=fasta",
        "https://www.ncbi.nlm.nih.gov/nuccore/NM_001318204.2?report=fasta",
        "https://www.ncbi.nlm.nih.gov/nuccore/NM_001329452.2?report=fasta",
        "https://www.ncbi.nlm.nih.gov/nuccore/NM_001040662.2?report=fasta",
        "https://www.ncbi.nlm.nih.gov/nuccore/NM_001375460.1?report=fasta",
        "https://www.ncbi.nlm.nih.gov/nuccore/NM_001375458.1?report=fasta",
        "https://www.ncbi.nlm.nih.gov/nuccore/NM_001144770.2?report=fasta",
        "https://www.ncbi.nlm.nih.gov/nuccore/NM_001374729.1?report=fasta",
        "https://www.ncbi.nlm.nih.gov/nuccore/NM_005154.5?report=fasta",
        "https://www.ncbi.nlm.nih.gov/nuccore/NM_001376.5?report=fasta"
    ]

    human_sequences = get_rna_sequences(human_urls)

    substrings = []
    for sequence in human_sequences:
        substrings += allMatchingSubstrings(sars2, sequence, 6)

    result_set = getRemainingSubstrings(sars2, substrings)

    print (result_set)
    print("end")




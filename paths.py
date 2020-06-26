# some relative filepaths in the project
#db_path = "./data/db/sequence.db"
db_path = "postgresql://ibex:ibex@localhost/ibex"

cached_covid_path = "./data/source_data/sars_cov2"

human_sequences = {
    'complete': './data/source_data/human/all_sequences.txt',
    'small_example': './data/source_data/human/format_example.txt',
    'largest_sequences': './data/source_data/human/big_ones.txt'
}
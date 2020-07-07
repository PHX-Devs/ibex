from sequence_parser.parser import parse
from paths import db_path, human_sequences

if __name__ == "__main__":
    parse(human_sequences['complete'], db_path)
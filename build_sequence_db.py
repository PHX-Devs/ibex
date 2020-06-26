from sequence_db.init_db import init_db
from sequence_parser.parser import parse
from paths import db_path, human_sequences

if __name__ == "__main__":
    #init_db(db_path)
    parse(human_sequences['complete'], db_path)
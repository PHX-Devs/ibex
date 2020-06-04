import sqlite3

def init_db(path):
    conn = sqlite3.connect(path)
    c = conn.cursor()

    # Create tables
    try:
        c.execute('''CREATE TABLE sequence (
                            id text primary key unique, 
                            sequence text,
                            length int)''')

        c.execute('''CREATE TABLE match (
                            seq_id text,
                            starting_index int,
                            length int,
                            FOREIGN KEY(seq_id) REFERENCES sequence(id),
                            UNIQUE(seq_id, starting_index, length))''')

        c.execute('''CREATE INDEX seq_length_idx ON sequence(length)''')
        c.execute('''CREATE INDEX match_length_idx ON match(length)''')

    except sqlite3.OperationalError:
        print("tables already exist")
    else:
        print("created tables")

    # Save (commit) the changes
    conn.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()
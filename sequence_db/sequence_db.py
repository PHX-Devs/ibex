import sqlite3

class SequenceDB (object):
    def __init__(self, path):
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()

    def insert_sequence(self, key, sequence):
        args = (key,sequence,len(sequence))
        query = '''
                    INSERT INTO sequence(id, sequence, length) VALUES (?,?,?)
                        ON CONFLICT(id) DO UPDATE SET sequence=excluded.sequence;
        '''
        self.cursor.execute(query, args)
        self.connection.commit()

    def insert_match(self, seq_id, start_index, length):
        args = (seq_id, start_index, length)
        query = '''INSERT OR REPLACE INTO match(seq_id, starting_index, length) VALUES (?,?,?)'''
        self.cursor.execute(query, args)
        self.connection.commit()

    def fetch_sequences(self):
        rows = self.cursor.execute('SELECT * FROM sequence')
        for row in rows:
            print(row)

    def fetch_sequence_ids(self):
        rows = self.cursor.execute('SELECT id FROM sequence ORDER BY length')
        keys = []
        for row in rows:
            keys.append(row[0])
        return keys

    def fetch_sequence(self, key):
        args = (key, )
        rows = self.cursor.execute('SELECT sequence FROM sequence WHERE id=?', args)
        row = rows.fetchone()
        return row[0]

    def fetch_matches(self, key, length):
        args = (key, length)
        rows = self.cursor.execute('SELECT starting_index, length FROM match WHERE seq_id = ? and length > ?', args)
        row = rows.fetchone()
        return row[0]

    def fetch_all_matches(self, length):
        args = (length, )
        rows = self.cursor.execute('SELECT starting_index, length FROM match WHERE length >= ?', args)
        results = []
        for row in rows:
            results.append([row[0], row[1]])
        return results

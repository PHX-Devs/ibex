import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.exc import IntegrityError

class SequenceDB (object):
    def __init__(self, db_string):
        self.engine = create_engine(db_string)

    def insert_sequence(self, key, sequence):
        query = 'INSERT INTO ibex.sequence(id, sequence, length) VALUES (:key, :seq, :len) ON CONFLICT (id) DO UPDATE SET sequence = EXCLUDED.sequence, length = EXCLUDED.length'
        args = {'key': key, 'seq': sequence, 'len': len(sequence)}
        try:
            statement = text(query)
            with self.engine.connect() as connection:
                result = connection.execute(statement, args)
            return "done"
        except IntegrityError:
            print("Integrity Error, unique constraint or otherwise encountered.")
            return "error"

    def insert_match(self, seq_id, start_index, length):
        query = 'INSERT INTO ibex.match(seq_id, starting_index, length) VALUES (:seq_id :index, :len) ON CONFLICT DO NOTHING'
        args = {'seq_id': seq_id, 'index': start_index, 'len': length}
        try:
            statement = text(query)
            with self.engine.connect() as connection:
                result = connection.execute(statement, args)
            return "done"
        except IntegrityError:
            print("Integrity Error, unique constraint or otherwise encountered.")
            return "error"

    def insert_matches(self, key, matches):
        args = ()
        for match in matches:
            args = args + ({'seq_id': key, 'index': match[0], 'len': match[1]},)
        query = 'INSERT INTO ibex.match(seq_id, starting_index, length) VALUES (:seq_id, :index, :len) ON CONFLICT DO NOTHING'

        try:
            statement = text(query)
            with self.engine.connect() as connection:
                result = connection.execute(statement, args)
            return "done"
        except IntegrityError:
            print("Integrity Error, unique constraint or otherwise encountered.")
            return "error"

    def insert_matches_optimized(self, key, matches):
        if (len(matches) == 0):
            return "nothing to do"
        strings = []
        for match in matches:
            strings.append("('%s',%s,%s)" % (key, match[0], match[1]))
        values = ",".join(strings)
        query = "INSERT INTO ibex.match (seq_id, starting_index, length) VALUES %s" % values
        try:
            statement = text(query)
            with self.engine.connect() as connection:
                result = connection.execute(statement, {})
            return "done"
        except IntegrityError:
            print("Integrity Error, unique constraint or otherwise encountered.")
            return "error"

    def set_sequence_analyzed(self, id, analyzed=True):
        args = {'seq_id': id, 'analyzed': analyzed}
        query = 'UPDATE ibex.sequence SET analyzed = :analyzed WHERE id = :seq_id'
        try:
            statement = text(query)
            with self.engine.connect() as connection:
                result = connection.execute(statement, args)
            return "done"
        except IntegrityError:
            print("Integrity Error, unique constraint or otherwise encountered.")
            return "error"

    def fetch_sequence_ids(self):
        rows = self.simple_query("SELECT id FROM sequence WHERE analyzed = 'f' ORDER BY length desc", {})
        keys = []
        for row in rows:
            keys.append(row['id'])
        return keys

    def fetch_all_sequence_ids(self):
        rows = self.simple_query("SELECT id FROM sequence ORDER BY length desc", {})
        keys = []
        for row in rows:
            keys.append(row['id'])
        return keys

    def get_count_sequences_processed(self):
        rows = self.simple_query("SELECT count(*) FROM sequence WHERE analyzed = 't'", {})
        count = rows[0]['count']
        return count

    def fetch_sequence(self, key):
        query = "SELECT sequence FROM ibex.sequence WHERE id = :id"
        args = {'id': key}
        rows = self.simple_query(query, args)
        return rows[0]['sequence']

    def fetch_all_matches(self, length):
        args = {'len': length}
        query = 'SELECT starting_index, length FROM match WHERE length >= :len'
        rows = self.simple_query(query, args)
        results = []
        for row in rows:
            results.append([row['starting_index'], row['length']])
        return results

    def get_count_of_matches(self):
        rows = self.simple_query('SELECT count(*) FROM ibex.match', {})
        return rows[0]['count']

    def get_min_match_size(self):
        query = "SELECT min(length) FROM ibex.match"
        rows = self.simple_query(query, {})
        try:
            return int(rows[0]['min'])
        except TypeError:
            return 0

    def prune_matches(self, size):
        query = "delete from ibex.match where length < :size"
        args = {'size': size}
        try:
            statement = text(query)
            with self.engine.connect() as connection:
                result = connection.execute(statement, args)
            return "done"
        except IntegrityError:
            print("Integrity Error, unique constraint or otherwise encountered.")
            return "error"

    def simple_query(self, query_string, args={}):
        statement = text(query_string)
        with self.engine.connect() as connection:
            result = connection.execute(statement, args)

        results_list = []
        for row in result:
            results_list.append(dict(row.items()))
        return results_list


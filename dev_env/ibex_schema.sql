CREATE SCHEMA ibex;
GRANT ALL ON SCHEMA ibex TO ibex;

CREATE TABLE ibex.sequence (
    id TEXT PRIMARY KEY,
    sequence TEXT,
    length INT
);
GRANT ALL ON TABLE ibex.sequence TO ibex;

CREATE TABLE ibex.match (
    seq_id TEXT REFERENCES ibex.sequence(id),
    starting_index INT,
    length INT,
    PRIMARY KEY (seq_id, starting_index, length)
);
GRANT ALL ON TABLE ibex.match TO match;

CREATE INDEX seq_length_idx ON ibex.sequence (length);
CREATE INDEX match_length_idx ON ibex.match (length);

GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA ibex TO ibex;

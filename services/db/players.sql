CREATE TABLE players (
	id FLOAT NOT NULL, 
	full_name VARCHAR NOT NULL, 
	first_name VARCHAR, 
	last_name VARCHAR NOT NULL, 
	is_active BOOLEAN NOT NULL
);

CREATE INDEX ON players ("id");


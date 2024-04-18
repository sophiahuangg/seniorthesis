CREATE TABLE teams (
	id FLOAT NOT NULL, 
	full_name VARCHAR NOT NULL, 
	abbreviation VARCHAR NOT NULL, 
	nickname VARCHAR NOT NULL, 
	city VARCHAR NOT NULL, 
	state VARCHAR NOT NULL, 
	year_founded FLOAT NOT NULL
);

CREATE INDEX ON teams ("id");


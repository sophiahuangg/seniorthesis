CREATE TABLE games (
	"SEASON_ID" FLOAT NOT NULL, 
	"TEAM_ID" FLOAT NOT NULL, 
	"TEAM_ABBREVIATION" VARCHAR NOT NULL, 
	"TEAM_NAME" VARCHAR NOT NULL, 
	"GAME_ID" FLOAT NOT NULL, 
	"GAME_DATE" DATE NOT NULL, 
	"MATCHUP" VARCHAR NOT NULL, 
	"WL" VARCHAR, 
	"MIN" FLOAT NOT NULL, 
	"PTS" FLOAT NOT NULL, 
	"FGM" FLOAT NOT NULL, 
	"FGA" FLOAT NOT NULL, 
	"FG_PCT" FLOAT, 
	"FG3M" FLOAT NOT NULL, 
	"FG3A" FLOAT NOT NULL, 
	"FG3_PCT" FLOAT, 
	"FTM" FLOAT NOT NULL, 
	"FTA" FLOAT NOT NULL, 
	"FT_PCT" FLOAT, 
	"OREB" FLOAT NOT NULL, 
	"DREB" FLOAT NOT NULL, 
	"REB" FLOAT NOT NULL, 
	"AST" FLOAT NOT NULL, 
	"STL" FLOAT NOT NULL, 
	"BLK" FLOAT NOT NULL, 
	"TOV" FLOAT NOT NULL, 
	"PF" FLOAT NOT NULL, 
	"PLUS_MINUS" FLOAT NOT NULL
);

CREATE INDEX ON games ("TEAM_ID");
CREATE INDEX ON games ("TEAM_ABBREVIATION");
CREATE INDEX ON games ("GAME_DATE");
CREATE INDEX ON games ("TEAM_NAME");
CREATE INDEX ON games ("WL")


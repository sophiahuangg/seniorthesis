CREATE TABLE regseasonpbp (
	"gameId" FLOAT NOT NULL, 
	"actionNumber" FLOAT NOT NULL, 
	clock VARCHAR NOT NULL, 
	period FLOAT NOT NULL, 
	"teamId" FLOAT NOT NULL, 
	"teamTricode" VARCHAR, 
	"personId" FLOAT NOT NULL, 
	"playerName" VARCHAR, 
	"playerNameI" VARCHAR, 
	"xLegacy" FLOAT NOT NULL, 
	"yLegacy" FLOAT NOT NULL, 
	"shotDistance" FLOAT NOT NULL, 
	"shotResult" VARCHAR, 
	"isFieldGoal" BOOLEAN NOT NULL, 
	"scoreHome" FLOAT, 
	"scoreAway" FLOAT, 
	"pointsTotal" FLOAT NOT NULL, 
	location VARCHAR, 
	description VARCHAR, 
	"actionType" VARCHAR, 
	"subType" VARCHAR, 
	"videoAvailable" BOOLEAN NOT NULL, 
	"actionId" FLOAT NOT NULL
);

CREATE INDEX ON regseasonpbp ("gameId");
CREATE INDEX ON regseasonpbp ("teamId");
CREATE INDEX ON regseasonpbp ("personId");


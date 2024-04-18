CREATE TABLE regseasonboxscores (
	"gameId" FLOAT NOT NULL, 
	"teamId" FLOAT NOT NULL, 
	"teamCity" VARCHAR NOT NULL, 
	"teamName" VARCHAR NOT NULL, 
	"teamTricode" VARCHAR NOT NULL, 
	"teamSlug" VARCHAR NOT NULL, 
	"personId" FLOAT NOT NULL, 
	"firstName" VARCHAR NOT NULL, 
	"familyName" VARCHAR NOT NULL, 
	"nameI" VARCHAR NOT NULL, 
	"playerSlug" VARCHAR NOT NULL, 
	position VARCHAR, 
	comment VARCHAR, 
	"jerseyNum" BOOLEAN, 
	minutes VARCHAR(8), 
	"fieldGoalsMade" FLOAT NOT NULL, 
	"fieldGoalsAttempted" FLOAT NOT NULL, 
	"fieldGoalsPercentage" FLOAT NOT NULL, 
	"threePointersMade" FLOAT NOT NULL, 
	"threePointersAttempted" FLOAT NOT NULL, 
	"threePointersPercentage" FLOAT NOT NULL, 
	"freeThrowsMade" FLOAT NOT NULL, 
	"freeThrowsAttempted" FLOAT NOT NULL, 
	"freeThrowsPercentage" FLOAT NOT NULL, 
	"reboundsOffensive" FLOAT NOT NULL, 
	"reboundsDefensive" FLOAT NOT NULL, 
	"reboundsTotal" FLOAT NOT NULL, 
	assists FLOAT NOT NULL, 
	steals FLOAT NOT NULL, 
	blocks FLOAT NOT NULL, 
	turnovers FLOAT NOT NULL, 
	"foulsPersonal" FLOAT NOT NULL, 
	points FLOAT NOT NULL, 
	"plusMinusPoints" FLOAT NOT NULL
);

ALTER TABLE regseasonboxscores ALTER COLUMN "firstName" DROP NOT NULL;
CREATE INDEX ON regseasonboxscores ("gameId");
CREATE INDEX ON regseasonboxscores ("teamId");
CREATE INDEX ON regseasonboxscores ("personId");



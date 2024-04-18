#!/bin/bash

docker-compose exec pg psql -U user -d postgres -c "\COPY players FROM 'datasets/players.csv' WITH CSV HEADER;"
docker-compose exec pg psql -U user -d postgres -c "\COPY teams FROM 'datasets/teams.csv' WITH CSV HEADER;"
docker-compose exec pg psql -U user -d postgres -c "\COPY playercareerstats FROM 'datasets/playercareerstats.csv' WITH CSV HEADER;"
docker-compose exec pg psql -U user -d postgres -c "\COPY games FROM 'datasets/games.csv' WITH CSV HEADER;"
docker-compose exec pg psql -U user -d postgres -c "\COPY playerinfo FROM 'datasets/playerinfo.csv' WITH CSV HEADER;"
docker-compose exec pg psql -U user -d postgres -c "\COPY regseasonboxscores FROM 'datasets/regseasonboxscores.csv' WITH CSV HEADER;"
docker-compose exec pg psql -U user -d postgres -c "\COPY playoffboxscores FROM 'datasets/playoffboxscores.csv' WITH CSV HEADER;"
docker-compose exec pg psql -U user -d postgres -c "\COPY playoffspbp FROM 'datasets/playoffspbp.csv' WITH CSV HEADER;"
docker-compose exec pg psql -U user -d postgres -c "\COPY regseasonpbp FROM 'datasets/regseasonpbp.csv' WITH CSV HEADER;"


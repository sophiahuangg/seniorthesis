#!/bin/bash

# Loading All Data Except for Play By Play

for data in datasets/*.csv; do
    table="$(basename "$data" .csv)"
    docker-compose exec pg psql -U user -d postgres -c "\COPY $table FROM '$data' WITH CSV HEADER;"
done


# Loading Regular Season Play by Play

for z in datasets/*regpbp.zip; do
    unzip -oj "$z" -d datasets/
done

for csv in datasets/*regSSN*.csv; do
    docker-compose exec pg psql -U user -d postgres -c "\COPY regseasonpbp FROM '$csv' WITH CSV HEADER;"
    rm "$csv"
done

# Loading Playpffs Play by Play

unzip -oj datasets/playoffspbp.zip -d datasets/

for csv in datasets/*playoffspbp.csv; do
    docker-compose exec pg psql -U user -d postgres -c "\COPY playoffspbp FROM '$csv' WITH CSV HEADER;"
    rm "$csv"
done
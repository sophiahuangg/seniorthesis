#!/bin/bash
#python3 scrape.py

for file in datasets/*.csv; do
	ECHO $(basename "${file%.csv}")
	mkdir -p "../services/db"
	csvsql -i sqlite "$file" > "../services/db/$(basename "${file%.csv}").sql"
done

ECHO "SCHEMAS CREATED"



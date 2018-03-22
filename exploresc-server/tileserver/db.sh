#!/bin/bash

service postgresql start
createuser osm

createdb -E UTF8 -O osm -T template0 gis

psql -c "CREATE EXTENSION hstore;" -d gis

psql -c "CREATE EXTENSION postgis;" -d gis


psql -c "CREATE ROLE root superuser;" 
psql -c "ALTER ROLE root WITH LOGIN;"



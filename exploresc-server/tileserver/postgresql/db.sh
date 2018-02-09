#!/bin/bash
service postgresql start
echo 'createuser renderaccount'
createuser renderaccount
echo 'createdb -E UTF8 -O renderaccount -T template0 gis'
createdb -E UTF8 -O renderaccount -T template0 gis
cat initdb.sql
cat initdb.sql | psql

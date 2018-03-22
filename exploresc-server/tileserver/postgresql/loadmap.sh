#!/bin/bash
service postgresql start
osm2pgsql -d gis --create --slim  -G --hstore --tag-transform-script /home/renderaccount/src/openstreetmap-carto/openstreetmap-carto.lua -C 2500 --number-processes 2 -S /home/renderaccount/src/openstreetmap-carto/openstreetmap-carto.style /home/renderaccount/data/south-carolina-latest.osm.pbf

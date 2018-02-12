#!/bin/bash
service postgresql start
su - postgres
cd /home/osm
wget https://github.com/gravitystorm/openstreetmap-carto/archive/v2.41.0.tar.gz
tar xvf v2.41.0.tar.gz
osm2pgsql --slim -d gis -C 2500 --hstore --number-processes 2 -S openstreetmap-carto-2.41.0/openstreetmap-carto.style sc-latest.pbf



#!/bin/bash

cd /home/osm/openstreetmap-carto-2.41.0/

./get-shapefiles.sh

carto project.mml > style.xml



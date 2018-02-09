#!/bin/bash
mkdir /home/renderaccount/src
cd /home/renderaccount/src
git clone git://github.com/openstreetmap/mod_tile.git
cd mod_tile
./autogen.sh
./configure
make
make install
make install-mod_tile
ldconfig


echo 'DONE BUILDING mod_tile'

cd /home/renderaccount/src
git clone git://github.com/gravitystorm/openstreetmap-carto.git
cd openstreetmap-carto

npm install -g carto

carto -v

carto project.mml > mapnik.xml




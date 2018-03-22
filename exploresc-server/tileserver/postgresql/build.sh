#!/bin/bash



mkdir /home/renderaccount/src
cd /home/renderaccount/src

git clone git://github.com/openstreetmap/osm2pgsql.git
cd osm2pgsql

mkdir build && cd build
cmake ..
make
make install



cd /home/renderaccount/src

git clone -b switch2osm git://github.com/SomeoneElseOSM/mod_tile.git
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




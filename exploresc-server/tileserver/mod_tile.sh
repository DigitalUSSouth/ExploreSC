#!/bin/bash

cd /home/osm

git clone https://github.com/openstreetmap/mod_tile.git

cd mod_tile/

./autogen.sh
./configure
make
make install
make install-mod_tile

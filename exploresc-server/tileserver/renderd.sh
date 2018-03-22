#!/bin/bash

mkdir -p /var/lib/mod_tile
chmod -R 777 /var/lib/mod_tile
chown -R osm:osm /var/lib/mod_tile

mkdir /var/run/renderd
chmod -R 777 /var/run/renderd
chown -R osm:osm /var/run/renderd


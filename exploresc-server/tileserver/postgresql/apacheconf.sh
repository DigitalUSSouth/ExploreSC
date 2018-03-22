#!/bin/bash
mkdir /var/lib/mod_tile
chown renderaccount /var/lib/mod_tile

mkdir /var/run/renderd
chown renderaccount /var/run/renderd

a2enconf mod_tile

service apache2 reload
service apache2 restart 

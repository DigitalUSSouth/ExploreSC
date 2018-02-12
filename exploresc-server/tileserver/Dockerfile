FROM ubuntu:16.04

RUN apt-get update -y && apt-get install -y \
 	postgresql postgresql-contrib postgis postgresql-9.5-postgis-2.2 osm2pgsql wget tar
USER postgres
COPY db.sh /db.sh
RUN /db.sh
USER root
RUN useradd -ms /bin/bash osm
COPY sc-latest.pbf /home/osm/sc-latest.pbf
COPY mapdata.sh /mapdata.sh
#USER osm
RUN /mapdata.sh
#USER root
RUN apt install -y git autoconf libtool libmapnik-dev apache2-dev
COPY mod_tile.sh /mod_tile.sh
RUN /mod_tile.sh

#mapnik stylesheet
RUN apt install -y curl unzip gdal-bin mapnik-utils node-carto
COPY mapnik.sh /mapnik.sh
RUN /mapnik.sh

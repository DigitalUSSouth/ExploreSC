FROM ubuntu:16.04

RUN apt-get update && apt-get install -y \
    postgresql \ 
    postgresql-contrib \
    postgis \
    postgresql \
    postgresql-9.5-postgis-2.2 
RUN apt install -y libboost-all-dev git-core tar unzip wget bzip2 build-essential autoconf libtool libxml2-dev libgeos-dev libgeos++-dev libpq-dev libbz2-dev libproj-dev munin-node munin libprotobuf-c0-dev protobuf-c-compiler libfreetype6-dev libpng12-dev libtiff5-dev libicu-dev libgdal-dev libcairo-dev libcairomm-1.0-dev apache2 apache2-dev libagg-dev liblua5.2-dev ttf-unifont lua5.1 liblua5.1-dev libgeotiff-epsg autoconf apache2-dev libtool libxml2-dev libbz2-dev libgeos-dev libgeos++-dev libproj-dev gdal-bin libgdal1-dev libmapnik-dev mapnik-utils python-mapnik sudo vim osm2pgsql python-mapnik npm nodejs-legacy make cmake g++ libboost-dev libboost-system-dev libboost-filesystem-dev libexpat1-dev zlib1g-dev libbz2-dev libpq-dev libgeos-dev libgeos++-dev libproj-dev lua5.2 liblua5.2-dev
#RUN apt install -y libboost-all-dev git-core tar unzip wget bzip2 build-essential autoconf libtool libxml2-dev libgeos-dev libgeos++-dev libpq-dev libbz2-dev libproj-dev munin-node munin libprotobuf-c0-dev protobuf-c-compiler libfreetype6-dev libpng12-dev libtiff5-dev libicu-dev libgdal-dev libcairo-dev libcairomm-1.0-dev apache2 apache2-dev libagg-dev liblua5.2-dev ttf-unifont lua5.1 liblua5.1-dev libgeotiff-epsg
COPY setupdb.sh /setupdb.sh
COPY db.sh /db.sh
COPY loadmap.sh /loadmap.sh
COPY initdb.sql /initdb.sql
COPY south-carolina-latest.osm.pbf /home/renderaccount/data/south-carolina-latest.osm.pbf
RUN useradd -ms /bin/bash renderaccount
COPY build.sh /home/renderaccount/build.sh
USER postgres
RUN /db.sh    
USER root 
WORKDIR /home/renderaccount
RUN /home/renderaccount/build.sh
USER postgres
RUN /loadmap.sh
USER root
COPY getshapefiles.sh /getshapefiles.sh
RUN /getshapefiles.sh
RUN apt install -y fonts-noto-cjk fonts-noto-hinted fonts-noto-unhinted ttf-unifont
COPY renderd.conf /usr/local/etc/renderd.conf
COPY mod_tile.conf /etc/apache2/conf-available/mod_tile.conf
COPY apacheconf.sh /apacheconf.sh
#WORKDIR /home/renderaccount/src/openstreetmap-carto/
RUN /apacheconf.sh
#RUN a2enmod rewrite
COPY apache-conf.conf /etc/apache2/sites-available/000-default.conf
#COPY apache-config.conf /etc/apache2/sites-available/000-default.conf
#RUN service apache2 start
EXPOSE 80
#ENTRYPOINT bash &&

FROM ubuntu:16.04

RUN apt-get update && apt-get install -y \
    postgresql \ 
    postgresql-contrib \
    postgis \
    postgresql \
    postgresql-9.5-postgis-2.2 
#RUN apt install -y libboost-all-dev git-core tar unzip wget bzip2 build-essential autoconf libtool libxml2-dev libgeos-dev libgeos++-dev libpq-dev libbz2-dev libproj-dev munin-node munin libprotobuf-c0-dev protobuf-c-compiler libfreetype6-dev libpng12-dev libtiff5-dev libicu-dev libgdal-dev libcairo-dev libcairomm-1.0-dev apache2 apache2-dev libagg-dev liblua5.2-dev ttf-unifont lua5.1 liblua5.1-dev libgeotiff-epsg
RUN apt install -y libboost-all-dev git-core tar unzip wget bzip2 build-essential autoconf libtool libxml2-dev libgeos-dev libgeos++-dev libpq-dev libbz2-dev libproj-dev munin-node munin libprotobuf-c0-dev protobuf-c-compiler libfreetype6-dev libpng12-dev libtiff5-dev libicu-dev libgdal-dev libcairo-dev libcairomm-1.0-dev apache2 apache2-dev libagg-dev liblua5.2-dev ttf-unifont lua5.1 liblua5.1-dev libgeotiff-epsg
RUN apt-get install -y  autoconf apache2-dev libtool libxml2-dev libbz2-dev libgeos-dev libgeos++-dev libproj-dev gdal-bin libgdal1-dev libmapnik-dev mapnik-utils python-mapnik
RUN apt-get install -y sudo vim osm2pgsql python-mapnik
RUN apt install -y npm nodejs-legacy
COPY setupdb.sh /setupdb.sh
COPY db.sh /db.sh
COPY loadmap.sh /loadmap.sh
COPY initdb.sql /initdb.sql
COPY south-carolina-latest.osm.pdf /home/renderaccount/data/south-carolina-latest.osm.pbf
RUN useradd -ms /bin/bash renderaccount
COPY build.sh /home/renderaccount/build.sh
USER postgres
RUN /db.sh    
USER root 
WORKDIR /home/renderaccount
RUN /home/renderaccount/build.sh
USER postgres
RUN /loadmap.sh
#RUN a2enmod rewrite
#COPY apache-config.conf /etc/apache2/sites-available/000-default.conf
#RUN service apache2 start
EXPOSE 5432
#ENTRYPOINT bash &&

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

#configure renderd
COPY renderd.conf /usr/local/etc/renderd.conf
COPY renderd.sh /renderd.sh
RUN /renderd.sh

#install apache
RUN apt install -y apache2
COPY mod_tile.conf /etc/apache2/mods-available/mod_tile.load
RUN ln -s /etc/apache2/mods-available/mod_tile.load /etc/apache2/mods-enabled/
COPY apache.sh /apache.sh
RUN /apache.sh
COPY apache-conf.conf /etc/apache2/sites-enabled/000-default.conf

#setup supervisor
RUN apt install -y python-setuptools && easy_install supervisor
COPY startdb.sh /startdb.sh
COPY supervisord.conf /etc/supervisor/supervisord.conf
COPY supervisorprograms.ini /etc/supervisor/conf.d/programs.ini

EXPOSE 80

ENTRYPOINT supervisord -c /etc/supervisor/supervisord.conf -n

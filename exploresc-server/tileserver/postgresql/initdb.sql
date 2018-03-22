\c gis

CREATE EXTENSION postgis;

CREATE EXTENSION hstore;

ALTER TABLE geometry_columns OWNER TO renderaccount;

ALTER TABLE spatial_ref_sys OWNER TO renderaccount;

CREATE ROLE root superuser;

ALTER ROLE root WITH LOGIN;

\q


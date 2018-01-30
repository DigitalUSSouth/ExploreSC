#this file configures the database:
#enter correct credentials and rename to db-config.py
import pymysql as sql

connection = mariadb.connect('host','user','password','database')
cursor = connection.cursor()
import mysql.connector
import json 

with open("config.json","r") as config:
    dbPassword = (json.load(config)["dbPass"])

db = mysql.connector.connect(
   host = "localhost",
   user = "root",
   passwd = dbPassword,
   database = "phone_directory"
)

dbCursorObject = db.cursor()
createTable = """CREATE TABLE phone_numbers (name varchar(100) NOT NULL, number INT NOT NULL)"""
dbCursorObject.execute(createTable)

db.close()
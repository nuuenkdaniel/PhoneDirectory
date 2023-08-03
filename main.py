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

print(db)
import mysql.connector
import json 
from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

with open("config.json","r") as config:
    dbPassword = (json.load(config)["dbPass"])

db = mysql.connector.connect(
   host = "localhost",
   user = "root",
   passwd = dbPassword,
   database = "phone_directory"
)

def add_person(name,phone_number,street_address,city,state,zip,email):
    cursor_object = db.cursor()
    sql = "INSERT INTO address (name,street_address,city,state,zip)\
        VALUES (%s,%s,%s,%s,%s)"
    values = (name,street_address,city,state,zip)
    cursor_object.execute(sql,values)
    db.commit()
    sql = "INSERT INTO phone_numbers (name,number)\
        VALUES (%s,%s)"
    values = (name,phone_number)
    cursor_object.execute(sql,values)
    db.commit()
    sql = "INSERT INTO emails (name,email)\
        VALUES (%s,%s)"
    values = (name,email)
    cursor_object.execute(sql,values)
    db.commit()
    print("added values to tables")

def request_data():
    cursor_object = db.cursor()
    sql = "SELECT phone_numbers.name,phone_numbers.number,emails.email,address.street_address,address.city,address.state,address.zip\
        FROM phone_numbers\
        INNER JOIN emails ON phone_numbers.name = emails.name\
        INNER JOIN address ON phone_numbers.name = address.name"
    cursor_object.execute(sql)
    return cursor_object.fetchall()

def request_data_filtered(column,filter):
    cursor_object = db.cursor()
    sql = "SELECT phone_numbers.name,phone_numbers.number,emails.email,address.street_address,address.city,address.state,address.zip\
        FROM phone_numbers\
        INNER JOIN emails ON phone_numbers.name = emails.name\
        INNER JOIN address ON phone_numbers.name = address.name WHERE address.%s = '%s'" % (column,filter)
    cursor_object.execute(sql)
    return cursor_object.fetchall()

# add_person("Jane Doe",119,"2 Doe Dr","East Brunswick","NJ",54321,"JDoe@example.com")
# print(request_data()[0][0])
print(request_data_filtered("state","NY")[0][0])
db.close()

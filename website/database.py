import mariadb
import sys
import json 

with open("config.json","r") as config:
    dbPassword = (json.load(config)["dbPass"])

try: 
    db = mariadb.connect(
        user = "Danuu",
        passwd = dbPassword,
        host = "localhost"
    )
    print("Connection to database successful!")
except mariadb.Error as err:
    print(f"Could not make connection: {err}")
    sys.exit(1)

def create_database():
    cursor_object = db.cursor()
    try:
        cursor_object.execute("CREATE DATABASE phone_directory DEFAULT CHARACTER SET 'utf8'")
        cursor_object.execute("USE phone_directory")
    except mariadb.Error as err:
        print(f"Database could not be created: {err}")
        sys.exit(1)

def create_tables():
    cursor_object = db.cursor()
    tables = {}
    tables['contact_info'] = (
        "CREATE TABLE `contact_info` ("
        "   `id` int(10) NOT NULL AUTO_INCREMENT,"
        "   `phone_number` varchar(20),"
        "   `email` varchar(255),"
        "   PRIMARY KEY(id)"
        ")"
    )
    tables['address'] = (
        "CREATE TABLE `address` ("
        "   `id` int(10) NOT NULL AUTO_INCREMENT,"
        "   `street_address` varchar(255),"
        "   `state` varchar(255),"
        "   `city` varchar(255),"
        "   `zipcode` varchar(255),"
        "   PRIMARY KEY(id)"
        ")"
    )
    tables['info'] = (
        "CREATE TABLE `info` ("
        "   `id` int(10) NOT NULL AUTO_INCREMENT,"
        "   `first_name` varchar(255),"
        "   `last_name` varchar(255),"
        "   `notes` varchar(255),"
        "   PRIMARY KEY(id)"
        ")"
    )
    for table_name in tables:
        table_description = tables[table_name]
        try:
            print(f"Creating table {table_name}: ", end='')
            cursor_object.execute(table_description)
            print("OK")
        except mariadb.Error as err:
            if err.errno == 1050:
                print("already exists")
            else:
                print(err)
                sys.exit(1)

try:
    cursor_object = db.cursor()
    cursor_object.execute("USE phone_directory")
except mariadb.Error as err:
    if err.errno == 1049:
        create_database()
        create_tables()
        print("database and tables created")
    else:
        print(f"Error: {err}")
        sys.exit(1)


def add_person(first_name,last_name,phone_number,street_address,city,state,zip,email):
    try:
        cursor_object = db.cursor()
        sql = "INSERT INTO contact_info (phone_number,email)\
            VALUES (%s,%s)"
        values = (phone_number,email)
        cursor_object.execute(sql,values)
        db.commit()
    except maridb.Error as err:
        print(err)
        print("1")
    try:
        sql = "INSERT INTO address (street_address,state,city,zipcode)\
            VALUES (%s,%s,%s,%s)"
        values = (street_address,state,city,zip)
        cursor_object.execute(sql,values)
        db.commit()
    except mariadb.Error as err:
        print(err)
        print("2")
    try:
        sql = "INSERT INTO info (first_name,last_name)\
            VALUES (%s,%s)"
        values = (first_name,last_name)
        cursor_object.execute(sql,values)
        db.commit()
    except mariadb.Error as err:
        print(err)
        print("3")
    print("added values to tables")

def request_data():
    cursor_object = db.cursor()
    sql = "SELECT info.id,info.first_name,info.last_name,contact_info.email,contact_info.phone_number,address.street_address,address.city,address.state,address.zipcode\
        FROM info\
        INNER JOIN contact_info ON info.id = contact_info.id\
        INNER JOIN address ON contact_info.id = address.id"
    cursor_object.execute(sql)
    db.commit()
    return cursor_object.fetchall()

def search(table,columns,filters):
    cursor_object = db.cursor()
    sql = "SELECT info.id,info.first_name,info.last_name,contact_info.email,contact_info.phone_number,address.street_address,address.city,address.state,address.zipcode\
        FROM info\
        INNER JOIN contact_info ON info.id = contact_info.id\
        INNER JOIN address ON contact_info.id = address.id WHERE "
    for i in range(len(columns)):
        if i == 0:
            sql += "%s.%s = '%s'" % (table[i],columns[i],filters[i])
        else:
            sql += " AND %s.%s = '%s'" % (table[i],columns[i],filters[i])
    cursor_object.execute(sql)
    db.commit()
    return cursor_object.fetchall()

def delete_data(id):
    cursor_object = db.cursor()
    try:
        sql = f"DELETE FROM info WHERE info.id = {id}"
        cursor_object.execute(sql)
        sql = f"DELETE FROM address WHERE address.id = {id}"
        cursor_object.execute(sql)
        sql = f"DELETE FROM contact_info WHERE contact_info.id = {id}"
        cursor_object.execute(sql)
        db.commit()
        return True
    except mariadb.Error as err:
        print(f"Error deleting {id}: {err}")
        return False
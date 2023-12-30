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
except mariadb.Error as err:
    print("Could not make connection: {}".format(err))
    sys.exit(1)

def create_database():
    cursor_object = db.cursor()
    try:
        cursor_object.execute("CREATE DATABASE phone_directory DEFAULT CHARACTER SET 'utf8'")
    except mariadb.Error as err:
        print("Database could not be created: {}".format(err))
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
            print("Creating table {}: ".format(table_name), end='')
            cursor_object.execute(table_description)
        except mariadb.Error as err:
            if err:#.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists")
            else:
                print(err.msg)
        else:
            print("OK")

try:
    cursor_object = db.cursor()
    cursor_object.execute("USE phone_directory")
except mariadb.Error as err:
    if err:#.errno == errorcode.ER_BAD_DB_ERROR:
        create_database()
        create_tables()
        print("database and tables created")
    else:
        print(err)
        exit(1)


def add_person(first_name,last_name,phone_number,street_address,city,state,zip,email):
    try:
        cursor_object = db.cursor()
        sql = "INSERT INTO contact_info (phone_number,email)\
            VALUES (%s,%s)"
        values = (phone_number,email)
        cursor_object.execute(sql,values)
        db.commit()
    except err:
        print(err)
        print("1")
    try:
        sql = "INSERT INTO address (street_address,state,city,zipcode)\
            VALUES (%s,%s,%s,%s)"
        values = (street_address,state,city,zip)
        cursor_object.execute(sql,values)
        db.commit()
    except err:
        print(err)
        print("2")
    try:
        sql = "INSERT INTO info (first_name,last_name)\
            VALUES (%s,%s)"
        values = (first_name,last_name)
        cursor_object.execute(sql,values)
        db.commit()
    except err:
        print(err)
        print("3")
    print("added values to tables")

def request_data():
    cursor_object = db.cursor()
    sql = "SELECT phone_numbers.name,phone_numbers.number,emails.email,address.street_address,address.city,address.state,address.zip\
        FROM phone_numbers\
        INNER JOIN emails ON phone_numbers.name = emails.name\
        INNER JOIN address ON phone_numbers.name = address.name"
    cursor_object.execute(sql)
    return cursor_object.fetchall()

def search(table,columns,filters):
    cursor_object = db.cursor()
    sql = "SELECT info.first_name,info.last_name,contact_info.email,contact_info.phone_number,address.street_address,address.city,address.state,address.zipcode\
        FROM info\
        INNER JOIN contact_info ON info.id = contact_info.id\
        INNER JOIN address ON contact_info.id = address.id WHERE "
    for i in range(len(columns)):
        if i == 0:
            sql += "%s.%s = '%s'" % (table[i],columns[i],filters[i])
        else:
            sql += " AND %s.%s = '%s'" % (table[i],columns[i],filters[i])
    cursor_object.execute(sql)
    return cursor_object.fetchall()

import mysql.connector

database = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'password'
)

cursor_object = database.cursor()

cursor_object.execute("CREATE DATABASE crmdb")

print("Database created")
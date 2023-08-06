import os
import sqlite3

print(os.getcwd())

if(os.path.isfile("before.sqlite")):
    os.remove("before.sqlite")
if(os.path.isfile("after.sqlite")):
    os.remove("after.sqlite")

beforeDB = sqlite3.connect("before.sqlite")
afterDB = sqlite3.connect("after.sqlite")

cursor = beforeDB.cursor()
cursor.execute("CREATE TABLE fish (name TEXT, species TEXT, tank_number INTEGER)")
cursor.execute("CREATE TABLE dog (name TEXT, species TEXT, house_number INTEGER)")
cursor.execute("CREATE TABLE people (name TEXT, species TEXT, house_number INTEGER)")

cursor.execute("INSERT INTO fish VALUES ('Sammy', 'shark', 1)")
cursor.execute("INSERT INTO fish VALUES ('Jamie', 'cuttlefish', 7)")

cursor.execute("INSERT INTO dog VALUES ('Bill', 'shepard', 1)")
cursor.execute("INSERT INTO dog VALUES ('Tom', 'little', 7)")

beforeDB.commit()

cursor_ = afterDB.cursor()
cursor_.execute("CREATE TABLE fish (name TEXT, species TEXT, tank_number INTEGER)")
cursor_.execute("INSERT INTO fish VALUES ('Sammy', 'shark', 1)")
cursor_.execute("CREATE TABLE snowman (name TEXT, species TEXT, tank_number INTEGER)")


afterDB.commit()
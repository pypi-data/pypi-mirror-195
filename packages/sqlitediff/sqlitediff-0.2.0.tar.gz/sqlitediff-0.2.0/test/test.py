import os
import sqlite3

'''
Actions:

- Table created
    - snowman

- Table deleted
    - dog

- Entry created
    - leo, ole
    - olaf

- Entry deleted
    - samy

- Entry updated


'''

print(os.getcwd())

if(os.path.isfile("before.sqlite")):
    os.remove("before.sqlite")
if(os.path.isfile("after.sqlite")):
    os.remove("after.sqlite")

beforeDB = sqlite3.connect("before.sqlite")
afterDB = sqlite3.connect("after.sqlite")

cursor = beforeDB.cursor()
cursor.execute("CREATE TABLE fish (id INTEGER primary key autoincrement, name TEXT, species TEXT, tank INTEGER)")
cursor.execute("CREATE TABLE dog (id INTEGER primary key autoincrement, name TEXT, species TEXT, garden INTEGER)")

cursor.execute("INSERT INTO fish (name, species, tank) VALUES ('Sammy', 'shark', 1)")
cursor.execute("INSERT INTO fish (name, species, tank) VALUES ('Jamie', 'cuttlefish', 7)")
cursor.execute("INSERT INTO dog (name, species, garden) VALUES ('Bill', 'shepard', 1)")
cursor.execute("INSERT INTO dog (name, species, garden) VALUES ('Tom', 'little', 7)")

beforeDB.commit()

cursor_ = afterDB.cursor()
cursor_.execute("CREATE TABLE fish (id INTEGER primary key, name TEXT, species TEXT, tank INTEGER)")
cursor_.execute("INSERT INTO fish (id, name, species, tank) VALUES (2, 'Jamie', 'cuttlefish', 2)")
cursor_.execute("INSERT INTO fish (id, name, species, tank) VALUES (3, 'Leo', 'whale', 3)")
cursor_.execute("INSERT INTO fish (id, name, species, tank) VALUES (4, 'Ole', 'delfin', 4)")

cursor_.execute("UPDATE fish SET tank = '77' WHERE id = 2")

cursor_.execute("CREATE TABLE snowman (id INTEGER primary key, name TEXT, species TEXT, fridge INTEGER)")
cursor_.execute("INSERT INTO snowman (name, species, fridge) VALUES ('olaf', 'snow', 1)")


afterDB.commit()

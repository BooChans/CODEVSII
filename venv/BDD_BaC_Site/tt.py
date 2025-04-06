import os
import sqlite3

db_path = os.path.abspath('db/BDD_Velos.db')  # Get full absolute path
print("Trying to connect to:", db_path)

connection = sqlite3.connect(db_path)
print("Database connected successfully!")
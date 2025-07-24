# app/database.py
from databases import Database

DATABASE_URL = "mysql+aiomysql://root:123456@localhost/sies_tes"

database = Database(DATABASE_URL)
# app/models.py
from sqlalchemy import Table, Column, Integer, String, MetaData

metadata = MetaData()

students = Table(
    "students",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100)),
    Column("roll_number", String(20), unique=True),
    Column("password", String(100))
)
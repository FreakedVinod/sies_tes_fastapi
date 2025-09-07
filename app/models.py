from sqlalchemy import Table, Column, Integer, String, ForeignKey, MetaData

metadata = MetaData()

students = Table(
    "students",  # This matches your actual table name
    metadata,
    Column("student_id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(100)),
    Column("roll_no", String(10), unique=True),
    Column("password", String(255)),
    Column("class_id", Integer, ForeignKey("classes.class_id")),
    Column("admission_year", Integer),
)
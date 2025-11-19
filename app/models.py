from sqlalchemy import Table, Column, Integer, String, ForeignKey, MetaData

metadata = MetaData()

students = Table(
    "students",
    metadata,
    Column("student_id", Integer, primary_key=True, autoincrement=True),

    Column("name", String(100), nullable=False),
    Column("email", String(100), nullable=False),
    Column("roll_no", String(10), unique=True, nullable=False),
    Column("password", String(255), nullable=False),

    # Foreign keys (nullable because ON DELETE SET NULL)
    Column("stream_id", Integer, ForeignKey("streams.id"), nullable=True),
    Column("course_id", Integer, ForeignKey("courses.course_id"), nullable=True),
    Column("class_id", Integer, ForeignKey("classes.class_id"), nullable=True),

    Column("admission_year", Integer, nullable=False),

    # Correct column name from SQL: "is_eligible"
    Column("is_eligible", Integer, default=0)
)

classes = Table(
    "classes",
    metadata,
    Column("class_id", Integer, primary_key=True, autoincrement=True),
    Column("class_name", String(50), ForeignKey("courses.course_id")),
    Column("course_id", Integer)
)
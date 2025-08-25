from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from app.database import database

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# -------------------------------
# Show Students Page (with classes + eligibility)
# -------------------------------
@router.get("/admin/students", response_class=HTMLResponse)
async def admin_students_page(request: Request):
    students_query = """
        SELECT s.student_id, s.name, s.roll_no, s.class_id, s.admission_year,
               COALESCE(e.is_eligible, 0) AS is_eligible
        FROM students s
        LEFT JOIN eligibility e ON s.student_id = e.student_id
        ORDER BY s.class_id
    """
    students = await database.fetch_all(students_query)

    classes_query = "SELECT class_id, class_name FROM classes ORDER BY class_id"
    classes = await database.fetch_all(classes_query)

    return templates.TemplateResponse("adminStudents.html", {
        "request": request,
        "students": students,
        "classes": classes
    })


# -------------------------------
# Toggle Eligibility
# -------------------------------
@router.post("/admin/update-eligibility")
async def update_eligibility(student_id: str = Form(...), is_eligible: bool = Form(...)):
    # First update eligibility table
    check_query = "SELECT 1 FROM eligibility WHERE student_id = :student_id"
    existing = await database.fetch_one(check_query, {"student_id": student_id})

    if existing:
        update_query = """
            UPDATE eligibility 
            SET is_eligible = :is_eligible
            WHERE student_id = :student_id
        """
        await database.execute(update_query, {"student_id": student_id, "is_eligible": is_eligible})
    else:
        insert_query = """
            INSERT INTO eligibility (student_id, is_eligible)
            VALUES (:student_id, :is_eligible)
        """
        await database.execute(insert_query, {"student_id": student_id, "is_eligible": is_eligible})

    # Also update in students table
    update_student_query = """
        UPDATE students 
        SET is_eligible = :is_eligible
        WHERE student_id = :student_id
    """
    await database.execute(update_student_query, {"student_id": student_id, "is_eligible": is_eligible})

    return JSONResponse(content={"message": "Eligibility updated in both tables"})


# -------------------------------
# Add Student
# -------------------------------
@router.post("/admin/add-student")
async def add_student(
    name: str = Form(...),
    roll_no: str = Form(...),
    password: str = Form(...),
    class_id: int = Form(...),
    admission_year: int = Form(...)
):
    insert_query = """
        INSERT INTO students (name, roll_no, password, class_id, admission_year)
        VALUES (:name, :roll_no, :password, :class_id, :admission_year)
    """
    await database.execute(insert_query, {
        "name": name,
        "roll_no": roll_no,
        "password": password,
        "class_id": class_id,
        "admission_year": admission_year
    })
    return JSONResponse(content={"message": "Student added"})


# -------------------------------
# Update Student
# -------------------------------
@router.post("/admin/update-student")
async def update_student(
    student_id: str = Form(...),
    name: str = Form(...),
    roll_no: str = Form(...),
    password: str = Form(None),
    class_id: int = Form(...),
    admission_year: int = Form(...)
):
    update_query = """
        UPDATE students
        SET name = :name, roll_no = :roll_no,
            class_id = :class_id, admission_year = :admission_year
        WHERE student_id = :student_id
    """
    await database.execute(update_query, {
        "student_id": student_id,
        "name": name,
        "roll_no": roll_no,
        "class_id": class_id,
        "admission_year": admission_year
    })

    # Update password only if provided
    if password:
        pw_query = "UPDATE students SET password = :password WHERE student_id = :student_id"
        await database.execute(pw_query, {"password": password, "student_id": student_id})

    return JSONResponse(content={"message": "Student updated"})


# -------------------------------
# Delete Student
# -------------------------------
@router.delete("/admin/delete-student/{student_id}")
async def delete_student(student_id: str):
    await database.execute("DELETE FROM eligibility WHERE student_id = :student_id", {"student_id": student_id})
    await database.execute("DELETE FROM students WHERE student_id = :student_id", {"student_id": student_id})
    return JSONResponse(content={"message": "Student deleted"})
from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from app.database import database

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# -------------------------------
# Show the Student Eligibility Page
# -------------------------------
@router.get("/admin/student-eligibility", response_class=HTMLResponse)
async def student_eligibility_page(request: Request):
    return templates.TemplateResponse("studentEligibility.html", {"request": request})


# -------------------------------
# Fetch students with their eligibility
# -------------------------------
@router.get("/admin/students")
async def get_students(request: Request):
    query = """
        SELECT s.student_id, s.name, s.roll_no, s.class_id,
               COALESCE(e.is_eligible, 0) AS is_eligible
        FROM students s
        LEFT JOIN eligibility e ON s.student_id = e.student_id
        ORDER BY s.class_id
    """
    rows = await database.fetch_all(query)
    students = [dict(row._mapping) for row in rows]
    return templates.TemplateResponse(
        "adminStudents.html",
        {"request": request, "students": students}
    )

# -------------------------------
# Update student's eligibility
# -------------------------------
@router.post("/admin/update-eligibility")
async def update_eligibility(student_id: int = Form(...), is_eligible: bool = Form(...)):
    # Update eligibility table
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
    update_student = """
        UPDATE students
        SET is_eligible = :is_eligible
        WHERE student_id = :student_id
    """
    await database.execute(update_student, {"student_id": student_id, "is_eligible": is_eligible})

    return JSONResponse(content={"message": "Eligibility updated in both tables."})

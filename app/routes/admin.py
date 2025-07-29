from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from app.database import database
from sqlalchemy import text

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

#Show the main Admin Eligibility Page
@router.get("/admin-eligibility", response_class=HTMLResponse)
async def admin_eligibility_page(request: Request):
    return templates.TemplateResponse("adminEligibility.html",{"request": request})

#Fetch students with their eligibility
@router.get("/admin/students")
async def get_students():
    query = text("""
        SELECT s.student_id, s.name, s.roll_no, s.class_id,
                 COALESCE(e.is_eligible, 0) AS is_eligible
        FROM students s
        LEFT JOIN eligibility e ON s.student_id = e.student_id
    """)
    rows= await database.fetch_all(query)
    students = [dict(row._mapping) for row in rows]
    return {"students": students}

#Update student's eligibility
@router.post("/admin/update-eligibility")
async def update_eligibility(student_id: int = Form(...), is_eligible: bool = Form(...)):
    # Check if record exists
    check_query = text("SELECT * FROM eligibility WHERE student_id = :student_id")
    existing = await database.fetch_one(check_query, {"student_id": student_id})

    if existing:
        # Update existing record
        update_query = text("""
            UPDATE eligibility
            SET is_eligible = :is_eligible
            WHERE student_id = :student_id
        """)
        await database.execute(update_query, {"student_id": student_id, "is_eligible": is_eligible})
    else:
        # Insert new record
        insert_query = text("""
            INSERT INTO eligibility (student_id, is_eligible)
            VALUES (:student_id, :is_eligible)
        """)
        await database.execute(insert_query, {"student_id": student_id, "is_eligible": is_eligible})

    return JSONResponse(content={"message": "Eligibility updated."})

@router.get("/admin/students")
async def list_student():
    query="""
    SELECT student_id, name, roll_no, is_eligible, class_id
    FROM students
    ORDER BY class_id
    """
    results = await database.fetch_all(query)
    return {"students": results}
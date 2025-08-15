from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from myapp.database import database
from sqlalchemy import text

router = APIRouter()
templates = Jinja2Templates(directory="myapp/templates")


#Show the main Admin Eligibility Page
@router.get("/admin-eligibility", response_class=HTMLResponse)
async def admin_eligibility_page(request: Request):
    query = """
    SELECT s.student_id, s.name, s.roll_no, s.class_id,
           COALESCE(e.is_eligible, 0) AS is_eligible
    FROM students s
    LEFT JOIN eligibility e ON s.student_id = e.student_id
    """
    rows = await database.fetch_all(query)
    students = [dict(row._mapping) for row in rows]
    
    return templates.TemplateResponse(
        "adminEligibility.html",
        {"request": request, "students": students}
    )




# #Fetch students with their eligibility
# @router.get("/admin/students")
# async def get_students():
#     query = text("""
#         SELECT s.student_id, s.name, s.roll_no, s.class_id,
#                  COALESCE(e.is_eligible, 0) AS is_eligible
#         FROM students s
#         LEFT JOIN eligibility e ON s.student_id = e.student_id
#     """)
#     rows= await database.fetch_all(query)
#     students = [dict(row._mapping) for row in rows]
#     return {"students": students}




# #Update student's eligibility
# @router.post("/admin/update-eligibility")
# async def update_eligibility(data: dict):
#     student_id = data.get("student_id")
#     is_eligible = data.get("is_eligible", 0)

#     check_query = "SELECT 1 FROM eligibility WHERE student_id = :student_id"
#     existing = await database.fetch_one(check_query, {"student_id": student_id})

#     if existing:
#         await database.execute(
#             "UPDATE eligibility SET is_eligible = :is_eligible WHERE student_id = :student_id",
#             {"student_id": student_id, "is_eligible": is_eligible}
#         )
#     else:
#         await database.execute(
#             "INSERT INTO eligibility (student_id, is_eligible) VALUES (:student_id, :is_eligible)",
#             {"student_id": student_id, "is_eligible": is_eligible}
#         )

#     return {"message": "Eligibility updated"}


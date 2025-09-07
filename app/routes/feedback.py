from fastapi import APIRouter
from app.database import database  # import the database object
from fastapi.requests import Request

router = APIRouter()

@router.get("/get-my-average-rating/{teacher_subject_id}")
async def get_my_average_rating(teacher_subject_id: int, request: Request):
    # get student roll number from cookie
    roll_number = request.cookies.get("student_roll_number")
    if not roll_number:
        return {"avg_rating": 0}  # not logged in, return empty rating

    # fetch student_id
    student = await database.fetch_one(
        "SELECT student_id FROM students WHERE roll_no = :roll_no",
        {"roll_no": roll_number}
    )
    if not student:
        return {"avg_rating": 0}

    student_id = student["student_id"]

    # calculate average rating for this student and teacher_subject
    query = """
    SELECT AVG(rating) AS avg_rating
    FROM feedback
    WHERE teacher_subject_id = :teacher_subject_id
      AND student_id = :student_id
    """
    result = await database.fetch_one(query=query, values={
        "teacher_subject_id": teacher_subject_id,
        "student_id": student_id
    })
    avg_rating = float(result["avg_rating"]) if result["avg_rating"] is not None else 0
    return {"avg_rating": round(avg_rating, 2)}
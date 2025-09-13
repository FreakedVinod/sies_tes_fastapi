from fastapi import APIRouter, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates
from app.database import database
from app.models import students
import bcrypt

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# -------------------------
# Student Registration
# -------------------------
@router.post("studentRegister")
async def register_student(
    name: str = Form(...),
    roll_number: str = Form(...),
    password: str = Form(...),
    admission_year: int = Form(...),
    class_id: int = Form(...),
    course_id: int = Form(...)
):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    query = """
        INSERT INTO students (name, roll_no, password, admission_year, class_id, course_id)
        VALUES (:name, :roll_no, :password, :admission_year, :class_id, :course_id)
    """
    await database.execute(query=query, values={
        "name": name,
        "roll_no": roll_number,
        "password": hashed_password,
        "admission_year": admission_year,
        "class_id": class_id,
        "course_id": course_id
    })

    return RedirectResponse(url="/student/login-form", status_code=302)


# -------------------------
# Student Login
# -------------------------
@router.post("/studentLogin")
async def login_student(request: Request, roll_number: str = Form(...), password: str = Form(...)):
    query = students.select().where(students.c.roll_no == roll_number)
    student = await database.fetch_one(query)
    
    if student and bcrypt.checkpw(password.encode('utf-8'), student["password"].encode('utf-8')):
        request.session["student_id"] = student["student_id"]
        return RedirectResponse(url="/studentDashboard", status_code=302)
    
    return templates.TemplateResponse("studentLogin.html", {
        "request": request,
        "error": "Incorrect roll number or password"
    })


# -------------------------
# Student Dashboard (Class-based subjects)
# -------------------------
@router.get("/studentDashboard", response_class=HTMLResponse)
async def show_dashboard(request: Request):
    student_id = request.session.get("student_id")
    if not student_id:
        return RedirectResponse(url="/login", status_code=302)

    # Fetch student info including class_id
    student_query = "SELECT * FROM students WHERE student_id = :student_id"
    student = await database.fetch_one(student_query, values={"student_id": student_id})
    class_id = student["class_id"]

    # Fetch all subjects for student's class along with feedback status
    modules_query = """
        SELECT ts.id AS teacher_subject_id, s.subject_name, t.name AS teacher_name,
               EXISTS(
                   SELECT 1 
                   FROM feedback f
                   WHERE f.student_id = :student_id
                     AND f.teacher_subject_id = ts.id
               ) AS feedback_given
        FROM teacher_subjects ts
        INNER JOIN subjects s ON ts.subject_id = s.subject_id
        INNER JOIN teachers t ON ts.teacher_id = t.teacher_id
        INNER JOIN class_subjects cs ON cs.subject_id = ts.subject_id
        WHERE cs.class_id = :class_id
        ORDER BY s.subject_name
    """
    modules = await database.fetch_all(modules_query, values={
        "student_id": student_id,
        "class_id": class_id
    })

    return templates.TemplateResponse("studentDashboard.html", {
        "request": request,
        "student": student,
        "subjects": modules
    })


# -------------------------
# Module Rating Page (Class-based subjects)
# -------------------------
@router.get("/module-rating", response_class=HTMLResponse)
async def module_rating(request: Request):
    student_id = request.session.get("student_id")
    if not student_id:
        return RedirectResponse(url="/login", status_code=302)

    # Fetch student info including class_id
    student_query = "SELECT * FROM students WHERE student_id = :student_id"
    student = await database.fetch_one(student_query, values={"student_id": student_id})
    class_id = student["class_id"]

    # Fetch all modules for the student's class
    modules_query = """
        SELECT ts.id AS teacher_subject_id, s.subject_name, t.name AS teacher_name
        FROM teacher_subjects ts
        INNER JOIN subjects s ON ts.subject_id = s.subject_id
        INNER JOIN teachers t ON ts.teacher_id = t.teacher_id
        INNER JOIN class_subjects cs ON cs.subject_id = ts.subject_id
        WHERE cs.class_id = :class_id
        ORDER BY s.subject_name
    """
    modules = await database.fetch_all(modules_query, values={"class_id": class_id})

    # Calculate per-student average rating
    updated_modules = []
    for module in modules:
        module_dict = dict(module)

        feedback_query = """
            SELECT AVG(rating) AS student_avg
            FROM feedback
            WHERE teacher_subject_id = :teacher_subject_id
              AND student_id = :student_id
        """
        result = await database.fetch_one(feedback_query, values={
            "teacher_subject_id": module_dict["teacher_subject_id"],
            "student_id": student_id
        })
        module_dict["student_avg_rating"] = round(result["student_avg"] if result and result["student_avg"] else 0, 1)
        updated_modules.append(module_dict)

    return templates.TemplateResponse("moduleRating.html", {
        "request": request,
        "student": student,
        "modules": updated_modules
    })

# -------------------------
# Rate Subject Page
# -------------------------
@router.get("/rate/{teacher_subject_id}", response_class=HTMLResponse)
async def rate_subject(request: Request, teacher_subject_id: int):
    student_id = request.session.get("student_id")
    if not student_id:
        return RedirectResponse(url="/login", status_code=302)

    # Fetch student info
    student = await database.fetch_one(
        "SELECT * FROM students WHERE student_id = :student_id",
        {"student_id": student_id}
    )
    class_id = student["class_id"]

    # Check if the teacher_subject_id belongs to the student's class
    check_query = """
        SELECT ts.id
        FROM teacher_subjects ts
        INNER JOIN class_subjects cs ON cs.subject_id = ts.subject_id
        WHERE ts.id = :teacher_subject_id
          AND cs.class_id = :class_id
    """
    valid = await database.fetch_one(check_query, {"teacher_subject_id": teacher_subject_id, "class_id": class_id})
    if not valid:
        raise HTTPException(status_code=403, detail="You cannot rate this subject")

    # Fetch questions
    questions = await database.fetch_all("SELECT * FROM questions ORDER BY question_id ASC")

    # Fetch teacher-subject info
    sub_query = """
        SELECT ts.id AS teacher_subject_id, s.subject_name, t.name AS teacher_name
        FROM teacher_subjects ts
        JOIN subjects s ON ts.subject_id = s.subject_id
        JOIN teachers t ON ts.teacher_id = t.teacher_id
        WHERE ts.id = :teacher_subject_id
    """
    subject = await database.fetch_one(sub_query, {"teacher_subject_id": teacher_subject_id})

    return templates.TemplateResponse("rate.html", {
        "request": request,
        "questions": questions,
        "subject": subject
    })


# -------------------------
# Submit Feedback
# -------------------------
@router.post("/submit-feedback")
async def submit_feedback(request: Request, teacher_subject_id: int = Form(...)):
    student_id = request.session.get("student_id")
    if not student_id:
        raise HTTPException(status_code=401, detail="Student not logged in")

    form = await request.form()
    responses = {}
    for key, value in form.items():
        if key.startswith("responses[") and value:
            qid = int(key.replace("responses[", "").replace("]", ""))
            responses[qid] = int(value)

    # Delete previous ratings by this student for this teacher_subject
    delete_query = """
        DELETE FROM feedback
        WHERE student_id = :student_id
          AND teacher_subject_id = :teacher_subject_id
    """
    await database.execute(delete_query, values={
        "student_id": student_id,
        "teacher_subject_id": teacher_subject_id
    })

    # Insert new ratings
    insert_query = """
        INSERT INTO feedback (student_id, teacher_subject_id, question_id, rating)
        VALUES (:student_id, :teacher_subject_id, :question_id, :rating)
    """
    for qid, rating in responses.items():
        await database.execute(insert_query, values={
            "student_id": student_id,
            "teacher_subject_id": teacher_subject_id,
            "question_id": qid,
            "rating": rating
        })

    return RedirectResponse(url="/module-rating", status_code=303)

# -------------------------
# Student Logout
# -------------------------
@router.get("/logout")
async def logout(request: Request):
    request.session.pop("student_id", None)
    return RedirectResponse(url="student/login-form", status_code=302)

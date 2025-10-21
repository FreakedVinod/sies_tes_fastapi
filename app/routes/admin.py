from fastapi import APIRouter, Form, Request, UploadFile
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import bcrypt
from app.database import database

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# -------------------------
# Admin Registration
# -------------------------
@router.post("/adminRegister")
async def register_admin(
    admin_name: str = Form(...),
    admin_email: str = Form(...),
    admin_password: str = Form(...)
):
    # Hash password
    hashed_password = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Insert into DB
    query = """
        INSERT INTO admins (admin_name, admin_password, admin_email)
        VALUES (:admin_name, :admin_password, :admin_email)
    """
    await database.execute(query=query, values={
        "admin_name": admin_name,
        "admin_password": hashed_password,
        "admin_email": admin_email
    })

    # Redirect to admin login
    return RedirectResponse(url="/admin/login-form", status_code=302)


# -------------------------
# Admin Login
# -------------------------
@router.post("/adminLogin")
async def login_admin(request: Request, admin_name: str = Form(...), admin_password: str = Form(...)):
    # Fetch admin by name (raw SQL)
    query = "SELECT * FROM admins WHERE admin_name = :admin_name"
    admin = await database.fetch_one(query, values={"admin_name": admin_name})

    # Verify credentials
    if admin and bcrypt.checkpw(admin_password.encode('utf-8'), admin["admin_password"].encode('utf-8')):
        request.session["admin_id"] = admin["admin_id"]
        return RedirectResponse(url="/adminDashboard", status_code=302)

    # On error, reload login template with message
    return templates.TemplateResponse("adminLogin.html", {
        "request": request,
        "error": "Incorrect name or password"
    })

# -------------------------
# Admin Dashboard
# -------------------------
@router.get("/adminDashboard")
async def admin_dashboard(request: Request):
    # Suppose you stored admin data in session after login
    admin = request.session.get("admin")
    return templates.TemplateResponse(
        "adminDashboard.html", 
        {"request": request, "admin": admin}
    )

# -------------------------
# Admin Students
# -------------------------
@router.get("/manage-students")
async def admin_students(request: Request):
    return templates.TemplateResponse("adminStudents.html", {"request": request})

# 1. Streams
@router.get("/admin/streams")
async def get_streams(request: Request):
    query = "SELECT stream_id, stream_name FROM streams"
    rows = await request.database.fetch_all(query)
    return [dict(r) for r in rows]

# 2. Courses by Stream
@router.get("/admin/courses/{stream_id}")
async def get_courses(stream_id: int, request: Request):
    query = "SELECT course_id, course_name FROM courses WHERE stream_id = :sid"
    rows = await request.database.fetch_all(query, {"sid": stream_id})
    return [dict(r) for r in rows]

# 3. Classes by Course
@router.get("/admin/classes/{course_id}")
async def get_classes(course_id: int, request: Request):
    query = "SELECT class_id, class_name FROM classes WHERE course_id = :cid"
    rows = await request.database.fetch_all(query, {"cid": course_id})
    return [dict(r) for r in rows]

# 4. Students by Class
@router.get("/admin/students/{class_id}")
async def get_students(class_id: int, request: Request):
    query = """
        SELECT student_id, name, roll_no, class_id, admission_year, is_eligible
        FROM students WHERE class_id = :cid
    """
    rows = await request.database.fetch_all(query, {"cid": class_id})
    return [dict(r) for r in rows]

# 5. Add Student
@router.post("/admin/add-student")
async def add_student(
    request: Request,
    name: str = Form(...),
    roll_no: str = Form(...),
    password: str = Form(...),
    class_id: int = Form(...),
    admission_year: int = Form(...)
):
    query = """
        INSERT INTO students (student_id, name, roll_no, class_id, password, admission_year, is_eligible)
        VALUES (:student_id, :name, :roll_no, :class_id, :password, :admission_year, 1)
    """
    # student_id can be generated as roll_no or UUID
    student_id = roll_no  
    values = {
        "student_id": student_id,
        "name": name,
        "roll_no": roll_no,
        "class_id": class_id,
        "password": password,
        "admission_year": admission_year
    }
    await request.database.execute(query, values)
    return {"message": "Student added successfully"}

# 6. Update Student
@router.post("/admin/update-student")
async def update_student(
    request: Request,
    student_id: str = Form(...),
    name: str = Form(...),
    roll_no: str = Form(...),
    password: str = Form(None),
    class_id: int = Form(...),
    admission_year: int = Form(...)
):
    if password:  # update with password
        query = """
            UPDATE students SET name=:name, roll_no=:roll_no, class_id=:class_id,
            password=:password, admission_year=:admission_year WHERE student_id=:sid
        """
        values = {
            "sid": student_id,
            "name": name,
            "roll_no": roll_no,
            "class_id": class_id,
            "password": password,
            "admission_year": admission_year
        }
    else:  # update without changing password
        query = """
            UPDATE students SET name=:name, roll_no=:roll_no, class_id=:class_id,
            admission_year=:admission_year WHERE student_id=:sid
        """
        values = {
            "sid": student_id,
            "name": name,
            "roll_no": roll_no,
            "class_id": class_id,
            "admission_year": admission_year
        }
    await request.database.execute(query, values)
    return {"message": "Student updated successfully"}

# 7. Delete Student
@router.delete("/admin/delete-student/{student_id}")
async def delete_student(student_id: str, request: Request):
    query = "DELETE FROM students WHERE student_id = :sid"
    await request.database.execute(query, {"sid": student_id})
    return {"message": "Student deleted successfully"}

# 8. Student Ratings (new tab view)
@router.get("/admin/student-ratings/{student_id}", response_class=HTMLResponse)
async def student_ratings(student_id: str, request: Request):
    # Example: fetch feedback for student
    query = """
        SELECT q.question_text, r.rating
        FROM feedback_responses r
        JOIN feedback_questions q ON r.question_id = q.question_id
        WHERE r.student_id = :sid
    """
    rows = await request.database.fetch_all(query, {"sid": student_id})
    html = "<h2>Student Ratings</h2><table border='1'><tr><th>Question</th><th>Rating</th></tr>"
    for r in rows:
        html += f"<tr><td>{r['question_text']}</td><td>{r['rating']}</td></tr>"
    html += "</table>"
    return HTMLResponse(content=html)

@router.get("/admin/student-ratings/{student_id}", response_class=HTMLResponse)
async def student_ratings(request: Request, student_id: str):
    query = """
        SELECT q.question_text, r.rating
        FROM feedback_responses r
        JOIN feedback_questions q ON r.question_id = q.question_id
        WHERE r.student_id = :sid
    """
    rows = await request.app.state.db.fetch_all(query, {"sid": student_id})
    return templates.TemplateResponse("studentRatings.html", {
        "request": request,
        "ratings": rows,
        "student_id": student_id
    })

@router.get("/student/{student_id}/ratings", response_class=HTMLResponse)
async def student_ratings(request: Request, student_id: str):
    query = """
        SELECT q.question_text, r.rating
        FROM feedback_responses r
        JOIN questions q ON r.question_id = q.id
        WHERE r.student_id = :student_id
    """
    rows = await database.fetch_all(query, values={"student_id": student_id})

    ratings = [{"question_text": row["question_text"], "rating": row["rating"]} for row in rows]

    return templates.TemplateResponse(
        "studentRatings.html",
        {"request": request, "ratings": ratings}
    )


# -------------------------
# Admin Logout
# -------------------------
@router.get("/adminLogout")
async def logout(request: Request):
    request.session.pop("student_id", None)
    return RedirectResponse(url="admin/login-form", status_code=302)
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from app.database import database
from math import ceil
from typing import Optional
import bcrypt

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

print("🟢 Loaded: app/routes/admin.py (ACTIVE ROUTER)")

# 🧩 Step 1: Form Page — shows all courses dynamically
# ---------------------------
# Admin Registration Form Page (with Courses)
# ---------------------------
@router.get("/admin/register-form", response_class=HTMLResponse)
async def admin_register_form(request: Request):
    # ✅ Fetch all available courses (so admin can select department)
    query = "SELECT course_id, course_name FROM courses"
    courses = await database.fetch_all(query=query)
    print(f"Fetched {len(courses)} courses for admin registration.")

    return templates.TemplateResponse(
        "adminRegistration.html",
        {
            "request": request,
            "courses": courses
        }
    )

# 🧩 Step 2: POST Route — register admin
@router.post("/adminRegister")
async def admin_register(
    admin_name: str = Form(...),
    admin_email: str = Form(...),
    admin_password: str = Form(...),
    course_id: int = Form(...)
):
    import bcrypt
    hashed_pw = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt()).decode()

    insert_query = """
        INSERT INTO admins (admin_name, admin_email, admin_password, course_id)
        VALUES (:admin_name, :admin_email, :admin_password, :course_id)
    """

    await database.execute(insert_query, {
        "admin_name": admin_name,
        "admin_email": admin_email,
        "admin_password": hashed_pw,
        "course_id": course_id
    })

    print(f"✅ Admin registered: {admin_name} for course {course_id}")

    return RedirectResponse(url="/admin/login-form", status_code=302)



# ---------------------------
# Admin Login Form Page
# ---------------------------
@router.get("/admin/login-form", response_class=HTMLResponse)
async def admin_login_form(request: Request):
    return templates.TemplateResponse("adminLogin.html", {"request": request})


# ---------------------------
# Admin Login POST
# ---------------------------
@router.post("/adminLogin")
async def admin_login(
    request: Request,
    admin_name: str = Form(...),
    admin_password: str = Form(...)
):
    # Fetch admin by name
    query = "SELECT * FROM admins WHERE admin_name = :name"
    admin = await database.fetch_one(query=query, values={"name": admin_name})

    # Verify password
    if not admin or not bcrypt.checkpw(admin_password.encode('utf-8'), admin["admin_password"].encode('utf-8')):
        return templates.TemplateResponse(
            "adminLogin.html",
            {"request": request, "error": "Invalid name or password."},
            status_code=401
        )

    # Save admin_id to session
    request.session["admin_id"] = admin["admin_id"]

    return RedirectResponse(url="/admin/dashboard", status_code=302)


# ---------------------------
# Helper function to get logged-in admin
# ---------------------------
async def get_logged_in_admin(request: Request):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        return None
    query = "SELECT * FROM admins WHERE admin_id = :admin_id"
    return await database.fetch_one(query=query, values={"admin_id": admin_id})


# ---------------------------
# Admin Dashboard (Department-based Dynamic Insights)
# ---------------------------
@router.get("/admin/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request, class_id: int | None = None):
    admin = await get_logged_in_admin(request)
    if not admin:
        return RedirectResponse(url="/admin/login-form", status_code=302)

    # Fetch all classes under this admin's department
    classes_query = """
        SELECT class_id, class_name 
        FROM classes 
        WHERE course_id = :course_id 
        ORDER BY class_name
    """
    classes = await database.fetch_all(classes_query, {"course_id": admin["course_id"]})

    if not classes:
        return templates.TemplateResponse("adminDashboard.html", {
            "request": request,
            "admin": admin,
            "error": "No classes found for your department."
        })

    # Default: use first class if not selected
    selected_class_id = class_id or classes[0]["class_id"]

    # Teacher-wise average ratings
    teacher_ratings_query = """
        SELECT 
            t.name AS teacher_name,
            AVG(f.rating) AS avg_rating
        FROM feedback f
        INNER JOIN teacher_subjects ts ON f.teacher_subject_id = ts.id
        INNER JOIN teachers t ON ts.teacher_id = t.teacher_id
        INNER JOIN students s ON f.student_id = s.student_id
        WHERE s.class_id = :class_id
        GROUP BY t.teacher_id
        ORDER BY avg_rating DESC
    """
    teacher_ratings = await database.fetch_all(teacher_ratings_query, {"class_id": selected_class_id})

    # Convert Decimal to float
    teacher_ratings = [
        {
            "teacher_name": r["teacher_name"],
            "avg_rating": float(r["avg_rating"]) if r["avg_rating"] else 0.0
        }
        for r in teacher_ratings
    ]

    top_teachers = teacher_ratings[:3]

    # Summary stats (fully qualified columns)
    summary_query = """
        SELECT 
            (
                SELECT COUNT(DISTINCT t.teacher_id)
                FROM teacher_subjects ts
                JOIN class_subjects cs ON ts.subject_id = cs.subject_id
                JOIN teachers t ON ts.teacher_id = t.teacher_id
                WHERE cs.class_id = :class_id
            ) AS total_teachers,

            (
                SELECT COUNT(*) 
                FROM students s 
                WHERE s.class_id = :class_id
            ) AS total_students,

            (
                SELECT COUNT(DISTINCT f.student_id) 
                FROM feedback f
                JOIN students s ON f.student_id = s.student_id
                WHERE s.class_id = :class_id
            ) AS total_feedbacks
    """
    summary = await database.fetch_one(summary_query, {"class_id": selected_class_id})

    return templates.TemplateResponse("adminDashboard.html", {
        "request": request,
        "admin": admin,
        "classes": classes,
        "selected_class_id": selected_class_id,
        "teacher_ratings": teacher_ratings,
        "summary": summary,
        "top_teachers": top_teachers,
    })


# ---------------------------
# Manage Students (with Pagination + Filters + Search)
# ---------------------------
@router.get("/admin/manage-students", response_class=HTMLResponse)
async def admin_students(
    request: Request,
    class_id: Optional[int] = None,
    eligibility: Optional[str] = None,
    search: Optional[str] = None,
    page: int = 1
):  
    admin = await get_logged_in_admin(request)
    if not admin:
        return RedirectResponse(url="/admin/login-form", status_code=302)

    limit = 10  # Students per page
    offset = (page - 1) * limit

    # Fetch classes for dropdown
    classes_query = "SELECT class_id, class_name FROM classes WHERE course_id = :course_id ORDER BY class_name"
    classes = await database.fetch_all(classes_query, {"course_id": admin["course_id"]})

    # Base query
    base_query = "FROM students WHERE course_id = :course_id"
    params = {"course_id": admin["course_id"]}

    # Filters
    if class_id:
        base_query += " AND class_id = :class_id"
        params["class_id"] = class_id

    if eligibility in ["1", "0"]:
        base_query += " AND is_eligible = :eligibility"
        params["eligibility"] = int(eligibility)

    if search:
        base_query += " AND (name LIKE :search OR roll_no LIKE :search)"
        params["search"] = f"%{search}%"

    # Total count
    count_query = f"SELECT COUNT(*) AS total {base_query}"
    total_row = await database.fetch_one(count_query, params)
    total_students = total_row["total"] if total_row else 0
    total_pages = ceil(total_students / limit) if total_students > 0 else 1

    # Fetch paginated data
    students_query = f"SELECT * {base_query} ORDER BY admission_year DESC LIMIT :limit OFFSET :offset"
    params.update({"limit": limit, "offset": offset})
    students = await database.fetch_all(students_query, params)

    return templates.TemplateResponse(
        "adminStudents.html",
        {
            "request": request,
            "admin": admin,
            "students": students,
            "classes": classes,
            "selected_class": class_id,
            "selected_eligibility": eligibility,
            "search": search,
            "page": page,
            "total_pages": total_pages,
            "total_students": total_students,
            "active_page": "students"
        }
    )


# ---------------------------
# Edit Student (Form Page)
# ---------------------------
@router.get("/admin/edit-student/{student_id}", response_class=HTMLResponse)
async def admin_edit_student(request: Request, student_id: int):
    admin = await get_logged_in_admin(request)
    if not admin:
        return RedirectResponse(url="/admin/login-form", status_code=302)

    # Fetch student info
    student_query = "SELECT * FROM students WHERE student_id = :student_id"
    student = await database.fetch_one(student_query, {"student_id": student_id})

    if not student:
        return RedirectResponse(url="/admin/manage-students", status_code=302)

    # Fetch dropdown data
    streams = await database.fetch_all("SELECT * FROM streams")
    courses = await database.fetch_all("SELECT * FROM courses")
    classes = await database.fetch_all("SELECT * FROM classes")

    return templates.TemplateResponse(
        "adminEditStudent.html",
        {
            "request": request,
            "admin": admin,
            "student": student,
            "streams": streams,
            "courses": courses,
            "classes": classes
        }
    )


# ---------------------------
# Update Student (POST)
# ---------------------------
@router.post("/admin/update-student")
async def admin_update_student(
    student_id: int = Form(...),
    name: str = Form(...),
    roll_number: str = Form(...),
    email: str = Form(...),
    stream_id: int = Form(...),
    course_id: int = Form(...),
    class_id: int = Form(...),
    admission_year: int = Form(...),
    is_eligible: int = Form(...)
):
    query = """
        UPDATE students
        SET name = :name,
            roll_no = :roll_number,
            email = :email,
            stream_id = :stream_id,
            course_id = :course_id,
            class_id = :class_id,
            admission_year = :admission_year,
            is_eligible = :is_eligible
        WHERE student_id = :student_id
    """
    values = {
        "student_id": student_id,
        "name": name,
        "roll_number": roll_number,
        "email": email,
        "stream_id": stream_id,
        "course_id": course_id,
        "class_id": class_id,
        "admission_year": admission_year,
        "is_eligible": is_eligible
    }

    await database.execute(query=query, values=values)

    return RedirectResponse(url="/admin/manage-students", status_code=302)


# ---------------------------
# Add Student (Form Page)
# ---------------------------
@router.get("/admin/add-student-form", response_class=HTMLResponse)
async def admin_add_student_form(request: Request):
    admin = await get_logged_in_admin(request)
    if not admin:
        return RedirectResponse(url="/admin/login-form", status_code=302)

    # No need to fetch streams/courses here; we’ll load dynamically via JS
    return templates.TemplateResponse(
        "adminAddStudent.html",
        {"request": request, "admin": admin}
    )


# ---------------------------
# Add Student (POST — Save)
# ---------------------------
@router.post("/admin/add-student")
async def admin_add_student(
    name: str = Form(...),
    roll_number: str = Form(...),
    password: str = Form(...),
    email: str = Form(...),
    stream_id: int = Form(...),
    course_id: int = Form(...),
    class_id: int = Form(...),
    admission_year: int = Form(...),
):
    # Default eligibility
    is_eligible = 0

    # Hash password
    import bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()

    # Insert new student
    query = """
        INSERT INTO students (name, roll_no, password, email, stream_id, course_id, class_id, admission_year, is_eligible)
        VALUES (:name, :roll_no, :password, :email, :stream_id, :course_id, :class_id, :admission_year, :is_eligible)
    """
    values = {
        "name": name,
        "roll_no": roll_number,
        "password": hashed_password,
        "email": email,
        "stream_id": stream_id,
        "course_id": course_id,
        "class_id": class_id,
        "admission_year": admission_year,
        "is_eligible": is_eligible
    }
    await database.execute(query=query, values=values)

    return RedirectResponse(url="/admin/manage-students", status_code=302)

# ---------------------------
# Admin Trigger: Reset/Reindex Student IDs
# ---------------------------
@router.get("/admin/reindex-students")
async def reindex_students(request: Request):
    admin = await get_logged_in_admin(request)
    if not admin:
        return RedirectResponse(url="/admin/login-form", status_code=302)

    reindex_queries = [
        "SET FOREIGN_KEY_CHECKS = 0;",
        "SET @count = 0;",
        "UPDATE students SET student_id = (@count := @count + 1) ORDER BY student_id;",
        "ALTER TABLE students AUTO_INCREMENT = 1;",
        "SET FOREIGN_KEY_CHECKS = 1;"
    ]

    for q in reindex_queries:
        await database.execute(q)

    return RedirectResponse(url="/admin/manage-students", status_code=302)



# ---------------------------
# Delete Student
# ---------------------------
@router.get("/admin/delete-student/{student_id}")
async def delete_student(student_id: int):
    query = "DELETE FROM students WHERE student_id = :student_id"
    await database.execute(query, {"student_id": student_id})
    return RedirectResponse(url="/admin/manage-students", status_code=302)


# ---------------------------
# Manage Teachers Page
# ---------------------------

@router.get("/admin/manage-teachers", response_class=HTMLResponse)
async def admin_teachers(request: Request):
    admin = await get_logged_in_admin(request)
    if not admin:
        return RedirectResponse(url="/admin/login-form", status_code=302)

    query = "SELECT * FROM teachers"
    teachers = await database.fetch_all(query)

    return templates.TemplateResponse(
        "adminTeachers.html",
        {
            "request": request,
            "admin": admin,
            "teachers": teachers,
            "active_page": "teachers"
        }
    )

@router.post("/admin/add-teacher")
async def add_teacher(name: str = Form(...)):
    query = "INSERT INTO teachers (name) VALUES (:name)"
    await database.execute(query, {"name": name})
    return JSONResponse(content={"message": "Teacher added successfully"})

@router.delete("/admin/delete-teacher/{teacher_id}")
async def delete_teacher(teacher_id: int):
    query = "DELETE FROM teachers WHERE teacher_id = :teacher_id"
    await database.execute(query, {"teacher_id": teacher_id})
    return JSONResponse(content={"message": "Teacher deleted successfully"})

@router.post("/admin/update-teacher")
async def update_teacher(teacher_id: int = Form(...), name: str = Form(...)):
    query = "UPDATE teachers SET name = :name WHERE teacher_id = :teacher_id"
    await database.execute(query, {"teacher_id": teacher_id, "name": name})
    return JSONResponse(content={"message": "Teacher updated successfully"})

# ---------------------------
# Admin Logout
# ---------------------------
@router.get("/admin/logout")
async def admin_logout(request: Request):
    request.session.pop("admin_id", None)
    return RedirectResponse(url="/admin/login-form", status_code=302)

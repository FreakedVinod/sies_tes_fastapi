import secrets
import smtplib
import os


from email.mime.text import MIMEText
from datetime import datetime, timedelta
from fastapi import APIRouter, Form, Request
from fastapi import APIRouter, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates
from app.database import database
from app.models import students
from app.models import classes
from dotenv import load_dotenv
from passlib.hash import bcrypt


load_dotenv()

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# -------------------------
# Student Registration
# -------------------------

@router.get("/student/register-form")
def student_register_form(request: Request):
    return templates.TemplateResponse("studentRegistration.html", {"request": request})

@router.post("/studentRegister")
async def register_student(
    name: str = Form(...),
    roll_number: str = Form(...),
    password: str = Form(...),
    email: str = Form(...),
    admission_year: int = Form(...),
    class_id: int = Form(...),
    course_id: int = Form(...)
):
    hashed_password = bcrypt.hash(password)

    query = """
        INSERT INTO students (name, roll_no, password, email, admission_year, class_id, course_id)
        VALUES (:name, :roll_no, :password, :email, :admission_year, :class_id, :course_id)
    """
    await database.execute(query=query, values={
        "name": name,
        "roll_no": roll_number,
        "password": hashed_password,
        "email": email,
        "admission_year": admission_year,
        "class_id": class_id,
        "course_id": course_id
    })

    return RedirectResponse(url="/student/login-form", status_code=302)


# -------------------------
# Student Login
# -------------------------

@router.get("/student/login-form")
def student_login_form(request: Request):
    return templates.TemplateResponse("studentLogin.html", {"request": request})

@router.post("/studentLogin")
async def login_student(request: Request, roll_number: str = Form(...), password: str = Form(...)):
    query = students.select().where(students.c.roll_no == roll_number)
    student = await database.fetch_one(query)

    if student:
        # Check password first
        if bcrypt.verify(password, student["password"]):
            # Check eligibility
            if student["is_eligible"] == 1:
                request.session["student_id"] = student["student_id"]
                return RedirectResponse(url="/studentDashboard", status_code=302)
            else:
                # Not eligible to login
                return templates.TemplateResponse("studentLogin.html", {
                    "request": request,
                    "error": "You are not eligible for the feedback rating. Contact your administrator."
                })
    
    # Incorrect credentials
    return templates.TemplateResponse("studentLogin.html", {
        "request": request,
        "error": "Incorrect roll number or password"
    })

# -------------------------
# STEP 1: Forgot Password Page (Form)
# -------------------------
@router.get("/student/forgot-password", response_class=HTMLResponse)
async def forgot_password_page(request: Request):
    return templates.TemplateResponse(
        "studentResetPassword.html", {"request": request, "token": None}
    )


# -------------------------
# STEP 2: Handle Forgot Password (Send Email)
# -------------------------
@router.post("/student/forgot-password")
async def forgot_password_submit(request: Request, email: str = Form(...)):
    # Check if student email exists
    query = "SELECT student_id FROM students WHERE email = :email"
    student = await database.fetch_one(query, {"email": email})

    if not student:
        return templates.TemplateResponse(
            "studentResetPassword.html",
            {
                "request": request,
                "token": None,
                "error": "No account found with that email.",
            },
        )

    # Generate unique token and expiry (30 mins)
    token = secrets.token_urlsafe(32)
    expiry_time = datetime.utcnow() + timedelta(minutes=30)

    # Save token to database
    await database.execute(
        """
        INSERT INTO password_resets (student_id, token, expiry_time)
        VALUES (:student_id, :token, :expiry_time)
        """,
        {
            "student_id": student["student_id"],
            "token": token,
            "expiry_time": expiry_time,
        },
    )

    # Create reset link
    reset_link = f"http://127.0.0.1:8000/student/reset-password?token={token}"

    # Send Email
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASSWORD")

    msg = MIMEText(
        f"Click the link below to reset your password:\n\n{reset_link}\n\nThis link expires in 30 minutes."
    )
    msg["Subject"] = "Reset Your Password - SIES TES"
    msg["From"] = sender
    msg["To"] = email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender, password)
            smtp.send_message(msg)
    except Exception as e:
        print("Error sending email:", e)
        return templates.TemplateResponse(
            "studentResetPassword.html",
            {
                "request": request,
                "token": None,
                "error": "Failed to send reset email. Please try again later.",
            },
        )

    return templates.TemplateResponse(
        "studentResetPassword.html",
        {
            "request": request,
            "token": None,
            "success": "Password reset link has been sent to your email.",
        },
    )


# -------------------------
# STEP 3: Reset Password Page (via Email Link)
# -------------------------
@router.get("/student/reset-password", response_class=HTMLResponse)
async def reset_password_page(request: Request, token: str | None = None):
    return templates.TemplateResponse(
        "studentResetPassword.html", {"request": request, "token": token}
    )


# -------------------------
# STEP 4: Handle Password Update
# -------------------------
@router.post("/student/reset-password")
async def reset_password_submit(
    request: Request, token: str = Form(...), new_password: str = Form(...)
):
    # Fetch the token record from the correct table
    query = "SELECT * FROM password_resets WHERE token = :token"
    token_entry = await database.fetch_one(query, {"token": token})

    print("DEBUG - Token:", token)
    print("DEBUG - Token entry:", token_entry)

    # Validate token existence and expiry
    if not token_entry:
        raise HTTPException(status_code=400, detail="Invalid or expired token.")

    if datetime.utcnow() > token_entry["expiry_time"]:
        raise HTTPException(status_code=400, detail="Invalid or expired token.")

    # Get the student ID
    student_id = token_entry["student_id"]

    # Hash the new password
    hashed_pw = bcrypt.hash(new_password)

    # Update the student's password in the students table
    update_query = "UPDATE students SET password = :password WHERE student_id = :student_id"
    await database.execute(update_query, {"password": hashed_pw, "student_id": student_id})

    # Delete the used token (to prevent reuse)
    delete_query = "DELETE FROM password_resets WHERE token = :token"
    await database.execute(delete_query, {"token": token})

    # Redirect to login after success
    return RedirectResponse(url="/student/login-form", status_code=303)

# -------------------------
# Student Dashboard
# -------------------------

# Query 1: Calculates the average rating for each subject in the student's class (for the Left Card)
SQL_CLASS_AVERAGES = """
SELECT
    s.subject_name,
    CAST(AVG(f.rating) AS DECIMAL(10, 2)) AS average_rating,
    COUNT(DISTINCT f.student_id) AS total_students_rated
FROM
    feedback f
INNER JOIN
    students st ON f.student_id = st.student_id
INNER JOIN
    teacher_subjects ts ON f.teacher_subject_id = ts.id
INNER JOIN
    subjects s ON ts.subject_id = s.subject_id
WHERE
    st.class_id = :class_id -- Placeholder for the student's class_id
GROUP BY
    s.subject_name
ORDER BY
    average_rating DESC;
"""

# Query 2: Retrieves the 5 most recent rating submissions/updates by the student (for the Right Card)
SQL_STUDENT_ACTIVITY = """
SELECT
    s.subject_name,
    f.rating,
    f.updated_at AS feedback_time
FROM
    feedback f
INNER JOIN
    teacher_subjects ts ON f.teacher_subject_id = ts.id
INNER JOIN
    subjects s ON ts.subject_id = s.subject_id
WHERE
    f.student_id = :student_id -- Placeholder for the student's student_id
ORDER BY
    f.updated_at DESC
LIMIT 5;
"""

@router.get("/studentDashboard", response_class=HTMLResponse)
async def show_dashboard(request: Request):
    student_id = request.session.get("student_id")
    if not student_id:
        return RedirectResponse(url="/student/login-form", status_code=302)

    # 1. Fetch student info including class_id
    student_query = "SELECT * FROM students WHERE student_id = :student_id"
    student = await database.fetch_one(student_query, values={"student_id": student_id})
    class_id = student["class_id"]

    # --- 2. EXISTING QUERY: Fetch all subjects for student's class along with feedback status ---
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

    # This variable name is kept as 'modules' for compatibility with other pages, but is also passed to the template.
    modules = await database.fetch_all(
        modules_query,
        values={
            "student_id": student_id,
            "class_id": class_id
        }
    )

    # --- 3. NEW: Fetch data for Left Card (Overall Subject Averages) ---
    class_ratings = await database.fetch_all(
        SQL_CLASS_AVERAGES,
        values={"class_id": class_id}
    )

    # --- 4. NEW: Fetch data for Right Card (Recent Student Activity) ---
    student_activity = await database.fetch_all(
        SQL_STUDENT_ACTIVITY,
        values={"student_id": student_id}
    )

    # 5. Render the dashboard with ALL data
    return templates.TemplateResponse("studentDashboard.html", {
        "request": request,
        "student": student,
        "classes":classes,
        "subjects": modules,              # Original data (can be removed if not used)
        "class_ratings": class_ratings,   # Data for the Overall Averages card
        "student_activity": student_activity  # Data for the Recent Activity card
    })



# -------------------------
# Module Rating Page (Class-based subjects)
# -------------------------
@router.get("/module-rating", response_class=HTMLResponse)
async def module_rating(request: Request):
    student_id = request.session.get("student_id")
    if not student_id:
        return RedirectResponse(url="/student/login-form", status_code=302)

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

    return templates.TemplateResponse("studentModuleRating.html", {
        "request": request,
        "student": student,
        "modules": updated_modules
    })

# -------------------------
# Rate Subject Page (Fixed with Display Numbers)
# -------------------------
@router.get("/rate/{teacher_subject_id}", response_class=HTMLResponse)
async def rate_subject(request: Request, teacher_subject_id: int):
    student_id = request.session.get("student_id")
    if not student_id:
        return RedirectResponse(url="/student/login-form", status_code=302)

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

    # ✅ Fetch all questions for this class (5 per class)
    questions = await database.fetch_all(
        "SELECT question_id, question_text FROM questions WHERE class_id = :class_id ORDER BY question_id ASC",
        {"class_id": class_id}
    )

    # ✅ Add display numbers (1–5) manually
    numbered_questions = []
    for i, q in enumerate(questions, start=1):
        numbered_questions.append({
            "display_number": i,
            "question_id": q["question_id"],
            "question_text": q["question_text"]
        })

    # Fetch teacher-subject info
    sub_query = """
        SELECT ts.id AS teacher_subject_id, s.subject_name, t.name AS teacher_name
        FROM teacher_subjects ts
        JOIN subjects s ON ts.subject_id = s.subject_id
        JOIN teachers t ON ts.teacher_id = t.teacher_id
        WHERE ts.id = :teacher_subject_id
    """
    subject = await database.fetch_one(sub_query, {"teacher_subject_id": teacher_subject_id})

    # ✅ Pass `numbered_questions` instead of `questions`
    return templates.TemplateResponse("rate.html", {
        "request": request,
        "questions": numbered_questions,
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
# Student Resources (Dynamic)
# -------------------------
@router.get("/resources", response_class=HTMLResponse)
async def student_resources(request: Request):
    student_id = request.session.get("student_id")
    if not student_id:
        return RedirectResponse(url="/student/login-form", status_code=302)

    # Fetch student info
    student_query = "SELECT * FROM students WHERE student_id = :student_id"
    student = await database.fetch_one(student_query, {"student_id": student_id})

    # Fetch announcements
    announcements_query = """
        SELECT id, title, message, category, posted_by, created_at
        FROM latest_announcements
        ORDER BY created_at DESC
        LIMIT 10
    """
    announcements = await database.fetch_all(announcements_query)

    # Fetch study materials
    materials_query = """
        SELECT id, title, description, file_url, created_at
        FROM study_materials
        ORDER BY created_at DESC
        LIMIT 10
    """
    materials = await database.fetch_all(materials_query)

    return templates.TemplateResponse("studentResources.html", {
        "request": request,
        "student": student,
        "announcements": announcements,
        "materials": materials
    })



# -------------------------
# Student Logout
# -------------------------
@router.get("/logout")
async def logout(request: Request):
    request.session.pop("student_id", None)
    return RedirectResponse(url="student/login-form", status_code=302)
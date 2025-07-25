from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.database import database
from app.models import students

import aiomysql
import bcrypt

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

# Register Student

@router.post("/register")
async def register_student(
    name: str = Form(...),
    roll_number: str = Form(...),
    password: str = Form(...),
    admission_year: int = Form(...),
    class_name: str = Form(...)
):
    # Find class_id from class_name
    query = "SELECT class_id FROM classes WHERE class_name = :class_name"
    result = await database.fetch_one(query=query, values={"class_name": class_name})

    if not result:
        return {"error": "Class not found."}

    class_id = result["class_id"]

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Insert student
    insert_query = """
        INSERT INTO students (name, roll_no, password, admission_year, class_id)
        VALUES (:name, :roll_no, :password, :admission_year, :class_id)
    """
    await database.execute(query=insert_query, values={
        "name": name,
        "roll_no": roll_number,
        "password": hashed_password,
        "admission_year": admission_year,
        "class_id": class_id
    })

    return RedirectResponse(url="/login-form", status_code=302)




# Login Student (with cookie)

@router.post("/login")
async def login_student(request: Request, roll_number: str = Form(...), password: str = Form(...)):
    query = students.select().where(students.c.roll_no == roll_number)
    student = await database.fetch_one(query)

    if student and bcrypt.checkpw(password.encode('utf-8'), student["password"].encode('utf-8')):
        response = RedirectResponse(url="/dashboard", status_code=302)
        response.set_cookie(key="student_roll_number", value=roll_number)
        return response
    else:
        return templates.TemplateResponse("studentLogin.html", {
            "request": request,
            "error": "Incorrect roll number or password"
        })

# Show Login Form

@router.get("/login", response_class=HTMLResponse)
async def show_login_form(request: Request):
    return templates.TemplateResponse("studentLogin.html", {"request": request})


# Show Dashboard

@router.get("/dashboard", response_class=HTMLResponse)
async def show_dashboard(request: Request):
    student_roll_number = request.cookies.get("student_roll_number")
    if not student_roll_number:
        return RedirectResponse(url="/login", status_code=302)

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "student_roll_number": student_roll_number
    })

# Logout
@router.get("/logout")
async def logout(request: Request):
    response = RedirectResponse(url="/login-form", status_code=302)
    response.delete_cookie("student_roll_number")
    return response

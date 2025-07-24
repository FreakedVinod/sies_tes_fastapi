# app/main.py

from fastapi import FastAPI
from app.database import database
from app.routes import students
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from fastapi.responses import RedirectResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/register-form")
def register_form(request: Request):
    return templates.TemplateResponse("studentRegistration.html", {"request": request})


@app.get("/login-form")
def login_form(request: Request):
    return templates.TemplateResponse("studentLogin.html", {"request": request})


@app.get("/logout")
async def logout(request: Request):
    response = RedirectResponse(url="/login-form", status_code=302)
    response.delete_cookie("student_roll_number")
    return response

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(students.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to SIES-TES FastAPI!"}

@app.get("/hello")
def say_hello():
    return {"message": "Hello student!"}
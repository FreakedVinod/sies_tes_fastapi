# app/main.py

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from app.database import database
from app.routes import students, admin, feedback

app = FastAPI()

# Mount static folder
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Middleware for sessions
app.add_middleware(SessionMiddleware, secret_key="VinodKamrajAcharya")

# Templates setup
templates = Jinja2Templates(directory="app/templates")

print("LOADED ROUTER FILE:", __file__)

# ✅ Include Routers
app.include_router(students.router)
app.include_router(admin.router)
app.include_router(feedback.router)

# -------------------------------
# Generic Utility Endpoints
# -------------------------------
@app.get("/get-courses/{stream_id}")
async def get_courses_by_stream(stream_id: int):
    query = "SELECT course_id AS id, course_name AS name FROM courses WHERE stream_id = :stream_id"
    result = await database.fetch_all(query=query, values={"stream_id": stream_id})
    return JSONResponse(content={"courses": [dict(row) for row in result]})

@app.get("/get-classes/{course_id}")
async def get_classes(course_id: int):
    query = "SELECT class_id AS id, class_name AS name FROM classes WHERE course_id = :course_id"
    rows = await database.fetch_all(query, {"course_id": course_id})
    return JSONResponse(content={"classes": [dict(row) for row in rows]})

# -------------------------------
# Root + Startup/Shutdown
# -------------------------------
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# right after app.include_router(...) lines
print("=== ROUTES REGISTERED ===")
for route in app.routes:
    print(route.path, "->", getattr(route, "methods", None))
print("=========================")


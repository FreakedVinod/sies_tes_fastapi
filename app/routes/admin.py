from fastapi import APIRouter, Form, Request
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
# Admin Logout
# -------------------------
@router.get("/adminLogout")
async def logout(request: Request):
    request.session.pop("student_id", None)
    return RedirectResponse(url="admin/login-form", status_code=302)
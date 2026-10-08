from datetime import date

from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from starlette.middleware.sessions import SessionMiddleware

from database import engine, Base, get_db
from models import User, Task
from auth import hash_password, verify_password


# -------------------------
# CREATE DATABASE TABLES
# -------------------------

Base.metadata.create_all(bind=engine)


# -------------------------
# FASTAPI APP
# -------------------------

app = FastAPI()


# -------------------------
# SESSION
# -------------------------

app.add_middleware(
    SessionMiddleware,
    secret_key="my-super-secret-key-change-this"
)


# -------------------------
# TEMPLATES
# -------------------------

templates = Jinja2Templates(directory="templates")


# =====================================================
# SIGNUP
# =====================================================

@app.get("/signup", response_class=HTMLResponse)
def signup_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="signup.html",
        context={
            "error": None
        }
    )


@app.post("/signup")
def signup(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    # Check username already exists

    existing_user = (
        db.query(User)
        .filter(User.username == username)
        .first()
    )

    if existing_user:

        return templates.TemplateResponse(
            request=request,
            name="signup.html",
            context={
                "error": "Username already exists!"
            }
        )

    # Create new user

    new_user = User(
        username=username,
        password=hash_password(password)
    )

    db.add(new_user)
    db.commit()

    # Go to login

    return RedirectResponse(
        url="/login",
        status_code=303
    )


# =====================================================
# LOGIN
# =====================================================

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "error": None
        }
    )


@app.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    # Find user

    user = (
        db.query(User)
        .filter(User.username == username)
        .first()
    )

    # User not found

    if not user:

        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "error": "Invalid username or password!"
            }
        )

    # Check password

    if not verify_password(password, user.password):

        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "error": "Invalid username or password!"
            }
        )

    # Save user information in session

    request.session["user_id"] = user.id
    request.session["username"] = user.username

    # Go to task page

    return RedirectResponse(
        url="/tasks",
        status_code=303
    )


# =====================================================
# LOGOUT
# =====================================================

@app.get("/logout")
def logout(request: Request):

    # Remove session

    request.session.clear()

    return RedirectResponse(
        url="/login",
        status_code=303
    )


# =====================================================
# TASK PAGE
# =====================================================

@app.get("/tasks", response_class=HTMLResponse)
def task_page(
    request: Request,
    db: Session = Depends(get_db)
):

    # Check login

    user_id = request.session.get("user_id")

    if not user_id:

        return RedirectResponse(
            url="/login",
            status_code=303
        )

    # Get only logged-in user's tasks

    tasks = (
        db.query(Task)
        .filter(Task.user_id == user_id)
        .order_by(Task.due_date)
        .all()
    )

    username = request.session.get("username")

    return templates.TemplateResponse(
        request=request,
        name="tasks.html",
        context={
            "tasks": tasks,
            "username": username,
            "today": date.today().isoformat(),
            "error": None
        }
    )


# =====================================================
# ADD TASK
# =====================================================

@app.post("/tasks/add")
def add_task(
    request: Request,
    task_name: str = Form(...),
    due_date: str = Form(...),
    db: Session = Depends(get_db)
):

    # Check login

    user_id = request.session.get("user_id")

    if not user_id:

        return RedirectResponse(
            url="/login",
            status_code=303
        )

    # Convert string date to date object

    try:

        selected_date = date.fromisoformat(due_date)

    except ValueError:

        tasks = (
            db.query(Task)
            .filter(Task.user_id == user_id)
            .order_by(Task.due_date)
            .all()
        )

        return templates.TemplateResponse(
            request=request,
            name="tasks.html",
            context={
                "tasks": tasks,
                "username": request.session.get("username"),
                "today": date.today().isoformat(),
                "error": "Invalid date!"
            }
        )

    # ---------------------------------
    # PAST DATE NOT ALLOWED
    # ---------------------------------

    if selected_date < date.today():

        tasks = (
            db.query(Task)
            .filter(Task.user_id == user_id)
            .order_by(Task.due_date)
            .all()
        )

        return templates.TemplateResponse(
            request=request,
            name="tasks.html",
            context={
                "tasks": tasks,
                "username": request.session.get("username"),
                "today": date.today().isoformat(),
                "error": "Past date select kari shakay nahi!"
            }
        )

    # ---------------------------------
    # CREATE TASK
    # ---------------------------------

    new_task = Task(
        task_name=task_name,
        status="Pending",
        due_date=selected_date,
        user_id=user_id
    )

    # Save task

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    # Go back to task page

    return RedirectResponse(
        url="/tasks",
        status_code=303
    )
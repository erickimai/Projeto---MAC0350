from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

# Create tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# ─── Dependency ───────────────────────────────────────────────────────────────

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ─── Pages ────────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()
    categories = db.query(models.Category).all()
    return templates.TemplateResponse(
        "index.html", {"request": request, "tasks": tasks, "categories": categories}
    )


@app.get("/manage", response_class=HTMLResponse)
def manage(request: Request, db: Session = Depends(get_db)):
    categories = db.query(models.Category).all()
    return templates.TemplateResponse(
        "manage.html", {"request": request, "categories": categories}
    )


# ─── Tasks CRUD ───────────────────────────────────────────────────────────────

@app.get("/tasks", response_class=HTMLResponse)
def search_tasks(
    request: Request,
    search: str = "",
    category_id: str = "",
    db: Session = Depends(get_db),
):
    """hx-get: Search/filter tasks."""
    query = db.query(models.Task)
    if search:
        query = query.filter(models.Task.title.ilike(f"%{search}%"))
    if category_id:
        try:
            query = query.filter(models.Task.category_id == int(category_id))
        except ValueError:
            pass
    tasks = query.all()
    return templates.TemplateResponse(
        "partials/task_list.html", {"request": request, "tasks": tasks}
    )


@app.post("/tasks", response_class=HTMLResponse)
def create_task(
    request: Request,
    title: str = Form(...),
    category_id: int = Form(...),
    db: Session = Depends(get_db),
):
    """hx-post: Create a new task."""
    task = models.Task(title=title, category_id=category_id, done=False)
    db.add(task)
    db.commit()
    db.refresh(task)
    return templates.TemplateResponse(
        "partials/task_item.html", {"request": request, "task": task}
    )


@app.get("/tasks/{task_id}/edit", response_class=HTMLResponse)
def task_edit_form(task_id: int, request: Request, db: Session = Depends(get_db)):
    """Return inline edit form for a task."""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404)
    return templates.TemplateResponse(
        "partials/task_edit.html", {"request": request, "task": task}
    )


@app.get("/tasks/{task_id}/view", response_class=HTMLResponse)
def task_view(task_id: int, request: Request, db: Session = Depends(get_db)):
    """Return read-only view of a task (used to cancel edit)."""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404)
    return templates.TemplateResponse(
        "partials/task_item.html", {"request": request, "task": task}
    )


@app.put("/tasks/{task_id}", response_class=HTMLResponse)
def update_task(
    task_id: int,
    request: Request,
    title: str = Form(...),
    db: Session = Depends(get_db),
):
    """hx-put: Update task title."""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404)
    task.title = title
    db.commit()
    db.refresh(task)
    return templates.TemplateResponse(
        "partials/task_item.html", {"request": request, "task": task}
    )


@app.patch("/tasks/{task_id}/toggle", response_class=HTMLResponse)
def toggle_task(task_id: int, request: Request, db: Session = Depends(get_db)):
    """Toggle task done/undone."""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404)
    task.done = not task.done
    db.commit()
    db.refresh(task)
    return templates.TemplateResponse(
        "partials/task_item.html", {"request": request, "task": task}
    )


@app.delete("/tasks/{task_id}", response_class=HTMLResponse)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """hx-delete: Delete a task."""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404)
    db.delete(task)
    db.commit()
    return HTMLResponse("")


# ─── Categories CRUD ──────────────────────────────────────────────────────────

@app.post("/categories", response_class=HTMLResponse)
def create_category(
    request: Request, name: str = Form(...), db: Session = Depends(get_db)
):
    """hx-post: Create a new category."""
    category = models.Category(name=name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return templates.TemplateResponse(
        "partials/category_item.html", {"request": request, "category": category}
    )


@app.delete("/categories/{category_id}", response_class=HTMLResponse)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """hx-delete: Delete a category (also deletes its tasks via cascade)."""
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404)
    db.delete(category)
    db.commit()
    return HTMLResponse("")

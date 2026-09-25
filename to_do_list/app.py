from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import date

app = Flask(__name__)

DATABASE = "todo.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(150) NOT NULL,
            description VARCHAR(300),
            priority VARCHAR(20),
            is_completed BOOLEAN DEFAULT 0,
            due_date DATE
        )
    """)

    conn.commit()
    conn.close()


# Home Page
@app.route("/")
def index():

    conn = get_db_connection()

    pending_tasks = conn.execute(
        "SELECT * FROM tasks WHERE is_completed = 0 ORDER BY due_date"
    ).fetchall()

    completed_tasks = conn.execute(
        "SELECT * FROM tasks WHERE is_completed = 1 ORDER BY due_date"
    ).fetchall()

    conn.close()

    # Today's date
    today = date.today().isoformat()

    return render_template(
        "index.html",
        pending_tasks=pending_tasks,
        completed_tasks=completed_tasks,
        today=today
    )


# Add Task
@app.route("/add", methods=["POST"])
def add_task():

    title = request.form["title"]
    description = request.form["description"]
    priority = request.form["priority"]
    due_date = request.form["due_date"]

    # Past date validation
    today = date.today().isoformat()

    if due_date < today:
        return "Error: Due date cannot be in the past."

    conn = get_db_connection()

    conn.execute("""
        INSERT INTO tasks
        (title, description, priority, is_completed, due_date)
        VALUES (?, ?, ?, ?, ?)
    """, (
        title,
        description,
        priority,
        0,
        due_date
    ))

    conn.commit()
    conn.close()

    return redirect("/")


# Toggle Task
@app.route("/toggle/<int:id>")
def toggle_task(id):

    conn = get_db_connection()

    task = conn.execute(
        "SELECT is_completed FROM tasks WHERE id = ?",
        (id,)
    ).fetchone()

    if task:

        new_status = 0 if task["is_completed"] else 1

        conn.execute(
            "UPDATE tasks SET is_completed = ? WHERE id = ?",
            (new_status, id)
        )

        conn.commit()

    conn.close()

    return redirect("/")


# Edit Page
@app.route("/edit/<int:id>")
def edit_task(id):

    conn = get_db_connection()

    task = conn.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (id,)
    ).fetchone()

    conn.close()

    today = date.today().isoformat()

    return render_template(
        "update.html",
        task=task,
        today=today
    )


# Update Task
@app.route("/update/<int:id>", methods=["POST"])
def update_task(id):

    title = request.form["title"]
    description = request.form["description"]
    priority = request.form["priority"]
    due_date = request.form["due_date"]

    # Past date validation
    today = date.today().isoformat()

    if due_date < today:
        return "Error: Due date cannot be in the past."

    conn = get_db_connection()

    conn.execute("""
        UPDATE tasks
        SET title = ?,
            description = ?,
            priority = ?,
            due_date = ?
        WHERE id = ?
    """, (
        title,
        description,
        priority,
        due_date,
        id
    ))

    conn.commit()
    conn.close()

    return redirect("/")


# Delete Task
@app.route("/delete/<int:id>", methods=["POST"])
def delete_task(id):

    conn = get_db_connection()

    conn.execute(
        "DELETE FROM tasks WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    create_table()
    app.run(debug=True)
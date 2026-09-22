from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


# Database connection
def get_db():
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    return conn


# Create table
def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT NOT NULL,
            task_date TEXT NOT NULL,
            from_time TEXT NOT NULL,
            to_time TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Home page - Show all tasks
@app.route("/")
def index():
    conn = get_db()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()

    return render_template("index.html", tasks=tasks)


# Add task
@app.route("/add", methods=["POST"])
def add_task():

    task_name = request.form["task_name"]
    task_date = request.form["task_date"]
    from_time = request.form["from_time"]
    to_time = request.form["to_time"]
    status = request.form["status"]

    conn = get_db()

    conn.execute("""
        INSERT INTO tasks
        (task_name, task_date, from_time, to_time, status)
        VALUES (?, ?, ?, ?, ?)
    """, (task_name, task_date, from_time, to_time, status))

    conn.commit()
    conn.close()

    return redirect("/")


# Delete task
@app.route("/delete/<int:id>")
def delete_task(id):

    conn = get_db()

    conn.execute("DELETE FROM tasks WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect("/")


# Run application
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
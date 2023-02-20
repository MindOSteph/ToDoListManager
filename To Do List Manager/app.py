from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Set up the database
conn = sqlite3.connect("tasks.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT, completed INTEGER)")
conn.commit()

# Define a function to get the tasks from the database
def get_tasks():
    c.execute("SELECT * FROM tasks")
    tasks = []
    for row in c.fetchall():
        tasks.append({"id": row[0], "task": row[1], "completed": bool(row[2])})
    return tasks

# Define a function to add a task to the database
def add_task(task):
    c.execute("INSERT INTO tasks (task, completed) VALUES (?, ?)", (task, 0))
    conn.commit()

# Define a function to update a task in the database
def update_task(task_id, task):
    c.execute("UPDATE tasks SET task = ? WHERE id = ?", (task, task_id))
    conn.commit()

# Define a function to delete a task from the database
def delete_task(task_id):
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()

# Define a function to mark a task as completed in the database
def complete_task(task_id):
    c.execute("UPDATE tasks SET completed = ? WHERE id = ?", (1, task_id))
    conn.commit()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "add" in request.form:
            task = request.form["task"]
            add_task(task)
        elif "edit" in request.form:
            task_id = request.form["id"]
            task = request.form["task"]
            update_task(task_id, task)
        elif "delete" in request.form:
            task_id = request.form["id"]
            delete_task(task_id)
        elif "complete" in request.form:
            task_id = request.form["id"]
            complete_task(task_id)
        return redirect(url_for("index"))
    else:
        tasks = get_tasks()
        return render_template("index.html", tasks=tasks)

if __name__ == "__main__":
    app.run(debug=True)

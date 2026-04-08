from flask import Flask, render_template, request, redirect, session, flash
import datetime as dt
import json
import os

import tasks as t
import commands as cmds


app = Flask(__name__) # Creates an object of the Flask class, which is the WSGI application
app.secret_key = "You would never guess it..."

def load_data():
    """
    Loads the data from the JSON file and stores it in the session. Data is loaded only once, when the session is created
    """
    base_path = os.path.dirname(os.path.abspath(__file__)) # Get the directory where the script is located
    file_path = os.path.join(base_path, "tasks.json") # Join it with the path to a JSON file
    if "tasks" not in session:
        try:
            with open(file_path, "r") as f:
                session["tasks"] = json.load(f)
        except FileNotFoundError:
            # Handles the case where the file is missing
            print(f"Could not find file at {file_path}")


@app.get("/") # Handles the root URL, which is the home page of the website 
def index():
    return render_template(
        "index.html",
        title="Welcome to ToDoList webapp!",
    )

@app.route("/demand/") # Service for the URL "/demand", which is the page for choosing a command to execute
def demand_route():
    return render_template(
        "demand.html",
        title="Choose the command",
        url="/process_command/", # The endpoint that handles the POST method
        select_id="command_select",
        select_text="command",
        data=t.commands, # List of commands to choose from
    )

@app.route("/process_command/", methods=["POST"]) # The route that handles the form submission
def process_command():
    # Get the command the user selected
    selected_command = request.form.get("command_select")
    if selected_command:
        # Redirect the user to the pages which handles the selected commands
        return redirect(f"/{selected_command}/")
    # Handles the exception, if user doesn't choose the command    
    return "Error: No command selected", 400 

@app.route("/show/")
def show_route():
    load_data()
    if session["tasks"] == []:
        title = "You have no tasks"
    else:
        title = "Here's your task list"
    return render_template(
        "tasks.html",
        title=title,
        data=t.show_tasks(session["tasks"]),
    )

@app.route("/delete/", methods=["GET", "POST"]) # Service for the URL "/delete", which is the page for choosing a task to be removed
def delete_route():
    load_data()
    if session["tasks"] == []:
        title = "You have no tasks"
    else:
        title = "Choose the task"
    if request.method == "POST":
        task_index = request.form.get("task_index")
        session["tasks"].pop(int(task_index))
        session.modified = True # Tells Flask that the session have been changed
        t.save_tasks(session["tasks"])
        flash("Your task have been successfully removed!")
        return redirect("/delete/")
    return render_template(
        "select.html",
        title=title,
        button_text="Delete",
        data=session["tasks"], # List of tasks (dicts) to choose from
    )

@app.route("/mark/", methods=["GET", "POST"])
def mark_route():
    load_data()
    if session["tasks"] == []:
        title = "You have no tasks"
    else:
        title = "Choose the task"
    if request.method == "POST":
        task_index = request.form.get("task_index") # Returns string value from the HTTP form, which represents a task
        task_status = session["tasks"][int(task_index)]["status"]
        task_status, message = t.mark_task(task_status)
        flash(message)
        session["tasks"][int(task_index)]["status"] = task_status
        session.modified = True # Tells Flask that the session have been changed
        t.save_tasks(session["tasks"])
        return redirect("/mark/")
    return render_template(
        "select.html",
        title=title,
        button_text="Mark",
        data=session["tasks"], # List of tasks (dicts) to choose from
    )



@app.route("/add/", methods=["GET", "POST"])
def add_route():
    load_data()
    if request.method == "POST":
        completion_date = request.form.get("completion_date")
        if completion_date:  
            if dt.date.fromisoformat(completion_date) < dt.date.today():
                return render_template(
                    "add.html",
                    title="You've entered a wrong date! Try again"
                )
        else:
            completion_date = None
        description = request.form.get("task")
        task = t.add_task(description, completion_date)
        session["tasks"].append(task)
        session.modified = True # Tells Flask that the session have been changed
        t.save_tasks(session["tasks"])
        flash("Your task have been successfully saved!")
        return redirect("/")
    return render_template(
        "add.html",
        title="Add a new task!",
    )

@app.route("/clear/")
def clear_route():
    load_data()
    if session["tasks"] == []:
        title = "You've already cleared your task list, what do you wanna more?"
    else:
        title = "Taskless"
    session.clear() # Clears the session cookie
    t.save_tasks([]) # Overwrites the JSON file with an empty list
    return render_template(
        "clear.html",
        title=title,
    )


if __name__ == "__main__":
    app.run(debug=True)
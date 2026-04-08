import datetime as dt
import json
import os

commands = ["add", "delete", "show", "mark", "clear"]


def show_tasks(tasks):
    """
    Shows all tasks with details, such as:
    no(inner index, integer), description(title etc, string), done/undone(status, bools), 
    creation date(datetime), completion date(datetime) if were provided, 
    and until completion(difference between completion date and create date)
    """
    output = []
    for i, t in enumerate(tasks, 1):
        if t['status']:
            status = "Done"
        else:
            status = "Undone"
        if t["completion_date"] is not None:
            extra = f", Completion date: {t['completion_date']}, Until completion: {dt.date.fromisoformat(t['completion_date']) - dt.date.fromisoformat(t['creation_date'])}"
        else:
            extra = ""
        output.append(f"\t No:{i}, Description: {t['description']}, Status: {status}, Creation date: {t['creation_date']}{extra}")
    return output 

def save_tasks(tasks):
    """
    Saves the task to the JSON file. If the file doesn't exist, it creates a new one and saves the task there
    """
    base_path = os.path.dirname(os.path.abspath(__file__)) # Get the directory where the script is located
    file_path = os.path.join(base_path, "tasks.json") # Join it with the path to a JSON file
    try:
        with open(file_path, "w") as f:
            json.dump(tasks, f, indent=4, sort_keys=False) # Indent adds spaces and newlines, sort_keys = false keeps order of keys
    except FileNotFoundError:
        print(f"Could not find file at {file_path}")

def add_task(description, completion_date):
    """
    Adds a new task to the flask session and saves it to the JSON file.
    The task is represented as dictionary with keys "description", "status", "creation_date", "completion_date" with values string, boolean, date and date respectively.
    Requires the description and completion date of the task as parameters.
    """
    creation_date = dt.date.today().isoformat()
    keys = ["description", "status", "creation_date", "completion_date"]
    values = [description, False, creation_date, completion_date]
    task = dict(zip(keys, values))
    return task

def mark_task(task_status):
    """
    Changes task status to done/undone
    (where values are true and false respectively.)
    Returns boolean value and messagee that will be displayed to the user
    """
    message = "Your task have been successfully marked as"
    if task_status:
        message += " undone"
        return False, message
    message += " done"
    return True, message

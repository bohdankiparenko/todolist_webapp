import datetime as dt
import json
import os

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

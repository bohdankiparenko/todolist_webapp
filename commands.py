"""
All commands that are used in the application
"""
import datetime as dt
import json


def load_task(filename="tasks.json"):
    """
    Tries to load tasks from a JSON file
    If tasks.json doesn't exists, means that no tasks are saved
    """
    try:
        with open(filename, "r") as jf:
            return json.load(jf)
    except:
        return []

def task_list(tasks):
    """
    Shows all tasks with details, such as:
    no(inner index, integer), description(title etc, string), done/undone(status, bools), 
    creation date(datetime), completion date(datetime) if were provided, 
    and until completion(difference between completion date and create date)
    """
    output = []
    for i, t in enumerate(tasks, 1):
        if t["completion_date"] is not None:
            extra = f", Until completion: {dt.date.fromisoformat(t['completion_date']) - dt.date.fromisoformat(t['creation_date'])}"
        else:
            extra = ""
        output.append(f"\t No:{i}, Description: {t['description']}, Done: {t['status']}, Creation date: {t['creation_date']}, Completion date: {t['completion_date']}{extra}")
    return output     

def save_tasks(tasks, filename="tasks.json"):
    """
    Saves the list of the tasks to a JSON file
    If there's no file with name provided at parametr, than creates 
    a new JSON file and saves it with the name
    Needed to be provided with a list of tasks
    """ 
    if len(tasks) >= 0:
        with open(filename, "w") as jf:          
            json.dump(tasks, jf)
        # return print("\tYour tasks have been successfully saved to a JSON file") WILL RETURN NONE!

def add_task(tasks):
    """
    Add a task to the task list, with description,
    done/undone status, creation_date, and optional completion date
    """
    current_data = dt.date.today().isoformat()
    description = input("\nPlease enter a description for your task:\n")
    keys = ["description", "status", "creation_date", "completion_date"]
    values = [description, False, current_data, None]
    task = dict(zip(keys, values))
    while True:
        completion_date = input("""
        Would you like to type in the completion date of your task?
        If so, please provide date in the format 
        year, month (without zero before digit), day.
        For instance:
        2027, 3, 1
        as the first march of 2027
        All values in numbers.
                
        If no, please type /skip
        """)
        if completion_date == "/skip": 
            tasks.append(task)
            save_tasks(tasks)
            print("\nYour task has been successfully added on the list")
            print("Your task have been successfully saved to a JSON file")
            break
        else:
            try:
                year, month, day = map(int, completion_date.split(","))
                completion_date = dt.date(year, month, day).isoformat()
            except:
                print("\nInvalid date format")
                continue
            if current_data < completion_date:
                task["completion_date"] = completion_date
                tasks.append(task)
                print("\nCompletion date is successfully added to a task")
                save_tasks(tasks)
                print("\nYour task has been successfully added on the list")
                print("Your task have been successfully saved to a JSON file")
                break
            else:
                print("\nYour completion date is wrong. You cannot do things in the past :D. Try again")
                continue

def mark_task(task_index, tasks):
    """
    Toggle task status (done/undone) based on the number 
    Needed to be provided with a task_index (look at task_list declariton for no)
    """
    if tasks[task_index - 1]["status"]:
        tasks[task_index - 1]["status"] = False
        save_tasks(tasks)
        print(f"\nYou have successfully marked {task_index} task as undone")
    else:
        tasks[task_index - 1]["status"] = True
        save_tasks(tasks)
        print(f"\nYou have successfully marked {task_index} task as done")

def delete_task(task_index, tasks):
    """
    Delete task based on the number
    Needed to be provided with a task_index (look at task_list declariton for no)
    """
    tasks.pop(task_index - 1)
    save_tasks(tasks)
    print(f"\nYou have successfully deleted {task_index} task")

def clear_tasks(tasks):
    """
    Cleares all the tasks on the list
    Attention: THIS IS IRREVERSIBLE CHANGE!
    """
    tasks.clear()
    save_tasks(tasks)
    print("\nAll of your tasks has been successfully deleted. Don't you miss 'em?")

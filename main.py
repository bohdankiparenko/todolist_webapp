import datetime as dt
import json
import commands as cmds

print("""
    Welcome to todolist0.35! 
    To see your task list type in /list
    To add a new task /add
    To delete a task /delete [no]*
    To mark it as done/undone /mark [no]

    * no of the task you can see at /list; provde no without rectangle parentheses

    To quit the loop type in /q
""")
tasks = cmds.load_task()
current_data = dt.date.today().isoformat() # Gives today date, and converts it into the YYYY-MM-DD format
while True:
    order = input()
    parts = order.split()
    cmd = parts[0]
    if cmd == "/q":
        break
    if len(tasks) < 1:
        print("\nYour task list is empty. Add a new task")
        cmds.add_task(tasks)
        continue
    else:
        if cmd in ["/list", "/mark", "/delete", "/add", "/clear"]:
                if cmd in ["/list", "/add", "/clear"]:
                    if cmd == "/list":
                        cmds.task_list(tasks)
                        continue
                    elif cmd == "/add":
                        cmds.add_task(tasks)
                        cmds.save_tasks(tasks)
                        continue
                    else:
                        order = input("\nAre you sure that you want to clear all of your tasks? y / n\n")
                        if order.lower() != "y" and order.lower() != "n":
                            print("\nYou have typed wrong response. You had two options, y for yes and n for no")
                            continue
                        else:
                            if order == "y":
                                cmds.clear_tasks(tasks)
                                continue
                            else:
                                continue
                else:
                    if len(order.split()) < 2:
                        print("\tInvalid input. Perhaps, index is missing")
                    else:
                        parts = order.split()
                        try:
                            index = int(parts[1])
                        except:
                            print("\tInvalid index")
                            continue
                        if 1 <= index <= len(tasks):
                            if parts[0] == "/mark":
                                try:
                                    cmds.mark_task(index, tasks)
                                except:
                                    print("\tInvalid number. Please try again\n")
                                    continue
                            elif parts[0] == "/delete":
                                try:
                                    cmds.delete_task(index, tasks)
                                except:
                                    print("\tInvalid number. Please try again\n")
                                    continue
                        else:
                            print("\tInvalid index (out of range). Please try again\n")
                            continue
        else:
            print("\tYou typed in wrong command\n")
            continue

        


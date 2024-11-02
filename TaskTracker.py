import json
import argparse
from datetime import datetime
import os

task_list = "Tasks.json"

def load():
    if os.path.exists(task_list):
        with open(task_list, "r") as file:
            return json.load(file)
    return []


def save(tasks):
    with open(task_list, "w") as file:
        json.dump(tasks, file)


def add(description):
    tasks = load()
    if not tasks:
        task_point = {
            "id": 1,
            "description": description,
            "status": "todo",
            "createdAt": datetime.now().isoformat(),
            "updatedAt": datetime.now().isoformat()
        }
        tasks.append(task_point)
        save(tasks=tasks)

    else:
        id_num = len(tasks) + 1        
        ids = [task["id"] for task in tasks]
        for i in range(len(tasks)):
            if i + 1 not in ids:
                id_num = i + 1
                break

        task_point = {
            "id": id_num,
            "description": description,
            "status": "todo",
            "createdAt": datetime.now().isoformat(),
            "updatedAt": datetime.now().isoformat()
        }
        tasks.append(task_point)
        save(tasks=tasks)



def update(position, new_description):
    ListOfTasks = load()
    for i in range(len(ListOfTasks)):
        if position == ListOfTasks[i]["id"]:
            ListOfTasks[i]["description"] = new_description
            ListOfTasks[i]["updatedAt"] = datetime.now().isoformat()
            break
    save(ListOfTasks)
    
def delete(position):
    ListOfTasks = load()
    task_to_delete = [task for task in ListOfTasks if task["id"] == position]
    ListOfTasks.remove(task_to_delete[0])
    save(ListOfTasks)

def mark_progress(position):
    ListOfTasks = load()
    for i in range(len(ListOfTasks)):
        if position == ListOfTasks[i]["id"]:
            ListOfTasks[i]["status"] = "in-progress"
            break
    save(ListOfTasks)

def mark_done(position):
    ListOfTasks = load()
    for i in range(len(ListOfTasks)):
        if position == ListOfTasks[i]["id"]:
            ListOfTasks[i]["status"] = "done"
            break
    save(ListOfTasks)

def list(kind="all"):
    ListOfTasks = load()
    def show_task(task_element):
        print("Number ", task_element["id"])
        print(", Description: ", task_element["description"])
        print(", Status: ", task_element["status"])
        print(", Created at: ", task_element["createdAt"])
        print(", Updated at: ", task_element["updatedAt"])
    
    if kind == "todo":
        tasks_to_list = [task for task in ListOfTasks if task["status"] == kind]
        for i in range(len(tasks_to_list)):
            show_task(tasks_to_list[i])
    elif kind == "in-progress":
        tasks_to_list = [task for task in ListOfTasks if task["status"] == kind]
        for i in range(len(tasks_to_list)):
            show_task(tasks_to_list[i])
    elif kind == "done":
        tasks_to_list = [task for task in ListOfTasks if task["status"] == kind]
        for i in range(len(tasks_to_list)):
            show_task(tasks_to_list[i])
    else:
        for i in range(len(ListOfTasks)):
            show_task(ListOfTasks[i])

    '''
    elif kind == "done":
        for i in range(len(ListOfTasks)):
            if ListOfTasks[i]["status"] == "done":
                show_task(ListOfTasks[i])
    elif kind == "in-progress":
        for i in range(len(ListOfTasks)):
            if ListOfTasks[i]["status"] == "in-progress":
                show_task(ListOfTasks[i])
    '''
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="main_backend", description="Task Descriptor")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="Add a new task.")
    add_parser.add_argument("description", type=str, help="The description of the task.")

    update_parser = subparsers.add_parser("update", help="Update an existing task.")
    update_parser.add_argument("task_id", type=int, help="The ID od the task to update.")
    update_parser.add_argument("description", type=str, help="the new description of the task.")

    delete_parser = subparsers.add_parser("delete", help="Delete an existing task.")
    delete_parser.add_argument("task_id", type=int, help="The ID of the task to delete.")

    mark_progress_parser = subparsers.add_parser("mark-in-progress", help="Marking a Task as Progress.")
    mark_progress_parser.add_argument("task_id", type=int, help="The ID of the task to mark.")

    mark_done_parser = subparsers.add_parser("mark-done", help="Marking a Task as done.")
    mark_done_parser.add_argument("task_id", type=int, help="The ID of the Task to mark.")

    list_parser = subparsers.add_parser("listing", help="Marking a Task as done.")
    list_parser.add_argument("status", type=str, help="Status of the task at hand.")

    args = parser.parse_args()

    if args.command == "add":
        add(args.description)
    elif args.command == "update":
        update(args.task_id, args.description)
    elif args.command == "delete":
        delete(args.task_id)
    elif args.command == "mark-in-progress":
        mark_progress(args.task_id)
    elif args.command == "mark-done":
        mark_done(args.task_id)
    elif args.command == "listing":
        list(args.status)

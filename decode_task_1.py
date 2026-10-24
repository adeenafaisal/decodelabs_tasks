import json
import os

DATA_FILE = "tasks.json"

def load_tasks(filename=DATA_FILE):
    """Read tasks from disk (RAM is volatile, disk is not)."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return [] 


def save_tasks(tasks, filename=DATA_FILE):
    """Serialize the list to JSON and write it to disk."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)


def add_task(tasks, text):
    """Process step: build a dictionary 'row' and append it to the list."""
    text = text.strip()
    if not text:
        return None  
    next_id = tasks[-1]["id"] + 1 if tasks else 1
    row = {"id": next_id, "task": text}
    tasks.append(row)
    return row

def show_menu():
    print("\n===== TO-DO LIST =====")
    print("1. Add a task")
    print("2. View tasks")
    print("3. Quit")

def view_tasks(tasks):
    """Output step: loop over the list with enumerate()."""
    if not tasks:
        print("\nNo tasks yet. Add one!")
        return
    print("\nYour tasks:")
    for number, row in enumerate(tasks, start=1):
        print(f"  {number}. {row['task']}")
    print(f"Total: {len(tasks)} task(s)")

def main():
    my_tasks = load_tasks() 

    while True:
        show_menu()
        choice = input("Choose an option (1-3): ").strip() 
        if choice == "1":
            text = input("Enter a task : ")
            row = add_task(my_tasks, text)  
            if row:
                save_tasks(my_tasks)
                print(f'Added: "{row["task"]}"')
            else:
                print("A task can't be empty.")
        elif choice == "2":
            view_tasks(my_tasks) 
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
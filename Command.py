import json
import os
from datetime import datetime

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d')
        return super().default(obj)

class ToDoList:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        if os.path.exists('tasks.json'):
            with open('tasks.json', 'r') as file:
                try:
                    self.tasks = json.load(file)
                except json.decoder.JSONDecodeError:
                    print('Error: Unable to load tasks. File may be empty or corrupted.')
                    self.tasks = []

    def save_tasks(self):
        with open('tasks.json', 'w') as file:
            json.dump(self.tasks, file, cls=DateTimeEncoder)

    def add_task(self, task, priority='medium', due_date=None):
        new_task = {
            'task': task,
            'priority': priority,
            'due_date': due_date,
            'completed': False
        }
        self.tasks.append(new_task)
        self.save_tasks()
        print(f'Task "{task}" added.')

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            removed_task = self.tasks.pop(index)
            self.save_tasks()
            print(f'Task "{removed_task["task"]}" removed.')
        else:
            print('Invalid task index.')

    def mark_completed(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index]['completed'] = True
            self.save_tasks()
            print(f'Task "{self.tasks[index]["task"]}" marked as completed.')
        else:
            print('Invalid task index.')

    def display_tasks(self):
        if not self.tasks:
            print('No tasks found.')
        else:
            for i, task in enumerate(self.tasks):
                status = 'Completed' if task['completed'] else 'Pending'
                due_date = task['due_date'] if task['due_date'] else 'No due date'
                print(f'{i + 1}. {task["task"]} - Priority: {task["priority"]}, Status: {status}, Due Date: {due_date}')

def main():
    todo_list = ToDoList()

    while True:
        print('\n==== ToDo List ====')
        print('1. Add Task')
        print('2. Remove Task')
        print('3. Mark Task as Completed')
        print('4. View Tasks')
        print('0. Exit')

        choice = input('Enter your choice (0-4): ')

        if choice == '1':
            task = input('Enter task description: ')
            priority = input('Enter priority (high/medium/low): ')
            due_date_str = input('Enter due date (YYYY-MM-DD): ')
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d') if due_date_str else None
            todo_list.add_task(task, priority, due_date)

        elif choice == '2':
            index = int(input('Enter the task index to remove: '))
            todo_list.remove_task(index - 1)

        elif choice == '3':
            index = int(input('Enter the task index to mark as completed: '))
            todo_list.mark_completed(index - 1)

        elif choice == '4':
            todo_list.display_tasks()

        elif choice == '0':
            print('Exiting...')
            break

        else:
            print('Invalid choice. Please enter a number between 0 and 4.')

if __name__ == "__main__":
    main()

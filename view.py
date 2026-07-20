from typing import List

from dto import TaskDTO


class BaseView:
    @staticmethod
    def show_message(message: str, m_type: str = "warning") -> None:
        print("-" * 60)
        print(f"{m_type.capitalize()}: {message}")
        print("-" * 60)

    @staticmethod
    def get_choice(message: str) -> int:
        ch = input(message)
        try:
            ch = int(ch)
        except ValueError:
            print("Wrong input!")
            return -1
        else:
            return ch

    @staticmethod
    def get_string(message: str) -> str:
        string = input(message)
        return string


class TaskView(BaseView):
    def show_task(self):
        pass
    def edit_task(self, task):
        pass
    def delete_task(self, task):
        pass
    def create_task(self, task):
        pass
    def change_status(self, task):
        pass


class UserView(BaseView):
    @staticmethod
    def draw_menu() -> None:
        print("Choose one of below options:")
        print("1. Add task")
        print("2. Show all tasks")
        print("3. Show active tasks")
        print("4. Delete task")
        print("5. Switch task status")
        print("6. Edit task")
        print("7. Exit")

    @staticmethod
    def draw_edit_menu() -> None:
        print("Choose one of below options:")
        print("1. Edit title")
        print("2. Edit content")
        print("3. Edit deadline")
        print("4. Exit")

    @staticmethod
    def draw_single_task(task: TaskDTO) -> None:
        print("=" * 60)
        print(task)
        print("=" * 60)

    @staticmethod
    def get_task_specs() -> TaskDTO:
        task_data = {
            "title": input("Enter task title: "),
            "body": input("Enter task content: "),
            "expires_at": input("Enter deadline (YYYY-mm-dd HH:MM:SS): ")
        }
        return TaskDTO(**task_data)

    @staticmethod
    def draw_tasks(tasks_info: List[TaskDTO]) -> None:
        l = len(tasks_info)
        if not l:
            UserView.show_message("Empty tasks list!")
            return

        print("=" * 20)
        print("Tasks list:")
        print("=" * 20)

        for task_index in range(l):
            print(f"Task #{task_index+1}")
            print(tasks_info[task_index])
            if not task_index == l - 1:
                print("-" * 60)
        print("=" * 20)
        print("End of list")
        print("=" * 20)


class SystemView(BaseView):
    @staticmethod
    def greet() -> None:
        print("Welcome to TaskManager program!")

    @staticmethod
    def draw_menu() -> None:
        print("List of options:")
        print("1. Create account")
        print("2. Log in")
        print("3. Exit")

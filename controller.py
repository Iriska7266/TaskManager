import os

from view import *
from model import *


class TaskController:
    def __init__(self, model: TaskModel):
        self.view = TaskView()
        self.model = model


class UserController:
    def __init__(self, model: UserModel):
        self.view = UserView
        self.model = model
        self.fail_source = ""
        self.tip_source = ""

    def choose_task(self, active_only:bool = False) -> Optional[int]:
        os.system("cls")
        tasks_count = self.model.get_tasks_count()
        if tasks_count:

            if active_only:
                tasks_to_show = list(self.model.get_active_tasks())
            else:
                tasks_to_show = list(self.model.get_all_tasks())

            tasks_count = len(tasks_to_show)

            self.view.draw_tasks(tasks_to_show)
            task_number = self.view.get_choice(
                f"Choose task number [1-{tasks_count}]: "
            )
            if 1 <= task_number <= tasks_count:
                return task_number
            else:
                self.fail_source = "Wrong input!"
                return None
        else:
            self.fail_source = "Empty tasks list!"
            return None

    def work_menu(self) -> None:
        while True:
            if self.fail_source:
                self.view.show_message(self.fail_source)
                self.fail_source = ""
            elif self.tip_source:
                self.view.show_message(self.tip_source, m_type="tip")
                self.tip_source = ""

            self.view.draw_menu()
            option = self.view.get_choice(f"Choose an option [1-7]: ")

            match option:
                case 1:
                    os.system("cls")
                    try:
                        self.model.add_task(self.view.get_task_specs())
                    except ValueError as e:
                        self.fail_source = str(e)
                    else:
                        self.tip_source = "Task was added successfully."
                case 2:
                    os.system("cls")
                    self.view.draw_tasks(list(self.model.get_all_tasks()))
                    self.view.show_message("Click 'enter' to continue", m_type="tip")
                    input()
                case 3:
                    os.system("cls")
                    self.view.draw_tasks(list(self.model.get_active_tasks()))
                    self.view.show_message("Click 'enter' to continue", m_type="tip")
                    input()
                case 4:
                    task_number = self.choose_task()

                    if not task_number is None:
                        task = self.model.delete_task(task_number - 1)
                        self.tip_source = f"Task {task.title} removed successfully."
                case 5:
                    task_number = self.choose_task()

                    if not task_number is None:
                        task = self.model.toggle_task(task_number - 1)
                        if task.status:
                            self.tip_source = f"Task {task.title} completed successfully."
                        else:
                            self.tip_source = f"Task {task.title} is in process now."
                case 6:
                    task_number = self.choose_task()

                    if not task_number is None:
                        self.handle_edit_menu(task_number - 1)
                case 7:
                    exit()
                case _:
                    self.fail_source = "Invalid option!"
            os.system("cls")

    def handle_edit_menu(self, task_number: int) -> None:
        os.system("cls")
        task = self.model.get_task_by_number(task_number)
        self.view.draw_single_task(task)
        self.view.draw_edit_menu()

        option = self.view.get_choice(f"Choose an option [1-4]: ")
        match option:
            case 1:
                self.view.show_message(f"Title length can't be more than {TITLE_MAX_LEN} characters!",
                                       m_type="tip")
                new_title = self.view.get_string("Enter new title: ")
                status = self.model.edit_task_title(task_number, new_title)
                if status is None:
                    self.tip_source = "Task was successfully renamed."
                else:
                    self.fail_source = status
            case 2:
                self.view.show_message(f"Content length can't be more than {BODY_MAX_LEN} characters!",
                                       m_type="tip")
                new_content = self.view.get_string("Enter new content: ")
                status = self.model.edit_task_body(task_number, new_content)
                if status is None:
                    self.tip_source = "Task content was successfully changed."
                else:
                    self.fail_source = status
            case 3:
                self.view.show_message(f"Deadline should be in format: YYYY-mm-dd HH:MM:SS.",
                                       m_type="tip")
                new_deadline = self.view.get_string("Enter new deadline in correct format: ")
                status = self.model.edit_task_deadline(task_number, new_deadline)
                if status is None:
                    self.tip_source = "Task deadline was successfully changed."
                else:
                    self.fail_source = status
            case 4:
                return
            case _:
                self.fail_source = "Invalid option!"


class SystemController:
    def __init__(self):
        self.view = SystemView()
        self.model = SystemModel()

    def authorisation_menu(self) -> None:
        options = {
            1: self.model.add_user,
            2: self.model.authorise,
            3: exit
        }
        fail_source = ""

        self.view.greet()

        while True:
            if fail_source:
                self.view.show_message(fail_source)
                fail_source = ""

            self.view.draw_menu()
            option = self.view.get_choice(f"Choose an option [{list(options.keys())[0]}-{list(options.keys())[-1]}]: ")

            match option:
                case 1:
                    login = self.view.get_string("Enter login: ")
                    password = self.view.get_string("Enter password: ")

                    params = UserDTO(login, password)
                    user_model = options[option](params)

                    if user_model is None:
                        fail_source =  "Login is already busy!"
                    else:
                        work_window = UserController(user_model)
                        os.system("cls")
                        break
                case 2:
                    login = self.view.get_string("Enter login: ")
                    password = self.view.get_string("Enter password: ")

                    params = UserDTO(login, password)
                    user_model =  options[option](params)

                    if user_model is None:
                        fail_source = "Wrong login or password!"
                    else:
                        work_window = UserController(user_model)
                        os.system("cls")
                        break
                case 3:
                    options[option]()
                case _:
                    fail_source = "Invalid option!"
            os.system("cls")

        work_window.work_menu()

    def add_test_data(self) -> None:
        user_model = self.model.add_user(UserDTO("Ivan", "Ivanov"))
        user_model.add_task(TaskDTO("Learn Assembler",
                                    "1. Watch tutorial; 2. Cry",
                                    datetime.strptime(
                                        "2026-07-23 23:55:55",
                                        "%Y-%m-%d %H:%M:%S")))
        user_model.add_task(TaskDTO("Learn German",
                                    "1. Not being lazy; 2. Duolingo",
                                    datetime.strptime(
                                        "2026-08-31 23:59:59",
                                        "%Y-%m-%d %H:%M:%S")))

    def run(self):
        self.add_test_data()
        self.authorisation_menu()
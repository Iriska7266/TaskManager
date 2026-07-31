import time

from view import *
from domain_models import *

try:
    from database.repository import *
except ConnectionError as e:
    SystemView.show_message(str(e) + f"\nProgram will be closed in {EXIT_LAG} seconds.")
    time.sleep(EXIT_LAG)
    exit()


class TaskController:
    def __init__(self, model: TaskModel):
        self.view = TaskView()
        self.model = model


class UserController:
    def __init__(self, model: UserModel):
        self.view = UserView
        self.model = model
        self.repo = UserRepository()
        self.fail_source = ""
        self.tip_source = ""

    def choose_task(self, active_only:bool = False) -> Optional[int]:
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
                    # Add task
                    # DB support: YES
                    os.system("cls")
                    try:
                        task_data = self.view.get_task_specs()
                        new_task = self.model.add_task(task_data)
                    except ValueError as e:
                        self.fail_source = str(e)
                    else:
                        # Adding task to DB
                        try:
                            task_id = self.repo.add_task(self.model.get_dto(), task_data)
                        except RuntimeError as e:
                            self.fail_source = str(e)
                        else:
                            new_task.task_id = task_id
                            self.tip_source = f"Task was added successfully."
                case 2:
                    # Show all tasks
                    # DB support: not used
                    os.system("cls")
                    self.view.draw_tasks(list(self.model.get_all_tasks()))
                    self.view.show_message("Click 'enter' to continue", m_type="tip")
                    input()
                case 3:
                    # Show active tasks
                    # DB support: not used
                    os.system("cls")
                    self.view.draw_tasks(list(self.model.get_active_tasks()), "No active tasks!")
                    self.view.show_message("Click 'enter' to continue", m_type="tip")
                    input()
                case 4:
                    # Delete task
                    # DB support: YES
                    os.system("cls")
                    task_number = self.choose_task()

                    if not task_number is None:
                        task = self.model.delete_task(task_number - 1)

                        # Deleting the same task from DB
                        try:
                            self.repo.delete_task(task)
                        except ValueError as e:
                            self.fail_source = str(e)
                        else:
                            self.tip_source = f"Task {task.title} removed successfully."
                case 5:
                    # Switch task status
                    # DB support: YES
                    os.system("cls")
                    task_number = self.choose_task()

                    if not task_number is None:
                        task = self.model.toggle_task(task_number - 1)

                        try:
                            self.repo.switch_task_status(task)
                        except ValueError as e:
                            self.fail_source = str(e)
                        else:
                            if task.status:
                                self.tip_source = f"Task {task.title} completed successfully."
                            else:
                                self.tip_source = f"Task {task.title} is in process now."
                case 6:
                    # Edit task
                    # DB support: YES (full)
                    os.system("cls")
                    task_number = self.choose_task()

                    if not task_number is None:
                        os.system("cls")
                        self.handle_edit_menu(task_number - 1)
                case 7:
                    exit()
                case _:
                    self.fail_source = "Invalid option!"
            os.system("cls")

    def handle_edit_menu(self, task_number: int) -> None:
        task = self.model.get_task_by_number(task_number)
        self.view.draw_single_task(task)
        self.view.draw_edit_menu()

        option = self.view.get_choice(f"Choose an option [1-4]: ")
        match option:
            case 1:
                # Edit task title
                self.view.show_message(f"Title length can't be more than {TITLE_MAX_LEN} characters!",
                                       m_type="tip")
                new_title = self.view.get_string("Enter new title: ")
                status = self.model.edit_task_title(task_number, new_title)
                if status is None:
                    # DB
                    try:
                        self.repo.change_task_title(task, new_title)
                    except ValueError as e:
                        self.fail_source = str(e)
                    else:
                        self.tip_source = "Task was successfully renamed."
                else:
                    self.fail_source = status
            case 2:
                # Edit task content
                self.view.show_message(f"Content length can't be more than {BODY_MAX_LEN} characters!",
                                       m_type="tip")
                new_content = self.view.get_string("Enter new content: ")
                status = self.model.edit_task_body(task_number, new_content)
                if status is None:
                    # DB
                    try:
                        self.repo.change_task_content(task, new_content)
                    except ValueError as e:
                        self.fail_source = str(e)
                    else:
                        self.tip_source = "Task content was successfully changed."
                else:
                    self.fail_source = status
            case 3:
                # Edit task deadline
                new_deadline = self.view.get_deadline()
                status = self.model.edit_task_deadline(task_number, new_deadline)
                if status is None:
                    # DB
                    try:
                        self.repo.change_task_deadline(task, new_deadline)
                    except ValueError as e:
                        self.fail_source = str(e)
                    else:
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
        fail_source = ""
        repo = SystemRepository()

        self.view.greet()

        while True:
            if fail_source:
                self.view.show_message(fail_source)
                fail_source = ""

            self.view.draw_menu()
            option = self.view.get_choice(f"Choose an option [1-3]: ")

            match option:
                case 1:
                    # Registration
                    # DB support: YES
                    login = self.view.get_string("Enter login: ")
                    password = self.view.get_string("Enter password: ")

                    user_model = repo.get_user_by_login(login)

                    if user_model is None:
                        user_data = repo.add_user(login, password)
                        user_model = self.model.add_user(user_data)

                        work_window = UserController(user_model)
                        os.system("cls")
                        break
                    else:
                        fail_source = "Login is already busy!"
                case 2:
                    # Authorisation
                    # DB support: YES
                    login = self.view.get_string("Enter login: ")

                    user_data = repo.get_user_by_login(login)

                    if user_data is None:
                        fail_source = "No such login!"
                    else:
                        password = self.view.get_string("Enter password: ")

                        # Check password
                        if password == user_data.password_hash:
                            user_model =  UserModel(**vars(user_data))

                            # Writing user tasks from DB to RAM
                            user_repo = UserRepository()
                            tasks = user_repo.get_user_tasks(user_data)
                            for task in tasks:
                                user_model.add_task(task)

                            work_window = UserController(user_model)
                            os.system("cls")
                            break
                        else:
                            fail_source = "Wrong password!"
                case 3:
                    exit()
                case _:
                    fail_source = "Invalid option!"
            os.system("cls")

        work_window.work_menu()


    def run(self):
        self.authorisation_menu()
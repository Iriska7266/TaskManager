from dto import *


class TaskRepository:
    def __init__(self, login: str='postgres', password: str='postgres', host: str= "localhost",
                 port: str= '5432', db_name: str= 'tasks_system_db', dms: str= 'postgres+psycopg2'):
        self.login = login
        self.password = password
        self.host = host
        self.port = port
        self.db_name = db_name
        self.dms = dms

        self.db_url = "{}://{}:{}@{}:{}/{}".format(dms, login, password, host, port, db_name)

    def get_all_tasks(self):
        pass
    def write_all_tasks(self, tasks: list[TaskDTO]):
        pass
    def update_task(self, task_id: int):
        pass
    def delete_task(self, task_id: int):
        pass
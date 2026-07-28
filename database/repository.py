from sqlalchemy import select, func
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.orm import Session
from typing import List

from dto import *
from database.db import get_db
from database.orm import User, Task


class UserRepository:
    @staticmethod
    def get_user_tasks(user: UserDTO) -> List[TaskDTO]:
        with get_db() as db:
            db: Session
            stmt = select(Task).join(Task.users).where(User.u_id == user.uid)
            tasks = db.execute(stmt).scalars().all()
            return [TaskDTO.from_orm(task) for task in tasks]


    @staticmethod
    def add_task(user: UserDTO, task: TaskDTO) -> int:
        with get_db() as db:
            db: Session
            stmt = func.add_task(user.uid,
                                   task.title,
                                   task.body,
                                   task.created_at,
                                   task.expires_at,
                                   task.status)
            result = db.execute(stmt).scalar_one()
            if result == -1:
                db.rollback()
                raise RuntimeError("Database failure!")
            else:
                db.commit()
                return result

    @staticmethod
    def delete_task(task: TaskDTO) -> None:
        with get_db() as db:
            db: Session

            task_db = db.get(Task, task.task_id)
            if task_db is None:
                raise ValueError("Task is not found!")
            db.delete(task_db)
            db.commit()

    @staticmethod
    def switch_task_status(task: TaskDTO) -> None:
        with get_db() as db:
            db: Session

            task_db = db.get(Task, task.task_id)
            if task_db is None:
                raise ValueError("Task is not found!")
            task_db.status = not task_db.status
            db.commit()
            db.refresh(task_db)

    @staticmethod
    def change_task_title(task: TaskDTO, new_title: str) -> None:
        with get_db() as db:
            db: Session

            task_db = db.get(Task, task.task_id)
            if task_db is None:
                raise ValueError("Task is not found!")
            task_db.title = new_title
            db.commit()
            db.refresh(task_db)

    @staticmethod
    def change_task_content(task: TaskDTO, new_content: str) -> None:
        with get_db() as db:
            db: Session

            task_db = db.get(Task, task.task_id)
            if task_db is None:
                raise ValueError("Task is not found!")
            task_db.t_content = new_content
            db.commit()
            db.refresh(task_db)

    @staticmethod
    def change_task_deadline(task: TaskDTO, new_deadline) -> None:
        with get_db() as db:
            db: Session

            task_db = db.get(Task, task.task_id)
            if task_db is None:
                raise ValueError("Task is not found!")
            task_db.expires_at = new_deadline
            db.commit()
            db.refresh(task_db)


class SystemRepository:
    @staticmethod
    def get_user_by_login(login: str) -> Optional[UserDTO]:
        with get_db() as db:
            db: Session
            try:
                stmt = select(User).where(User.u_login == login)
                user = db.execute(stmt).scalars().first()

                if not user is None:
                    db.refresh(user)
                    user_dto = UserDTO(user.u_id,
                                       user.u_login,
                                       user.u_password_hash,
                                       user.created_at)
                    return user_dto
                else:
                    return None
            except NoResultFound:
                return None

    @staticmethod
    def add_user(login: str, password_hash: str) -> Optional[UserDTO]:
        with get_db() as db:
            db: Session
            try:
                new_user = User(u_login=login, u_password_hash=password_hash)
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                user_data = UserDTO(new_user.u_id,
                                    new_user.u_login,
                                    new_user.u_password_hash,
                                    new_user.created_at)
                return user_data
            except IntegrityError:
                return None

    @staticmethod
    def get_all_users():
        with get_db() as db:
            db: Session

            stmt = select(User)
            users_data = db.execute(stmt).scalars().all()
            return [UserDTO.from_orm(user_data) for user_data in users_data]
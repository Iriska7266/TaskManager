from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class TaskDTO:
    title: str
    body: str
    expires_at: datetime
    status: bool = False
    created_at: datetime = field(default_factory=datetime.now)

    def __str__(self):
        return (f"Title: {self.title}\n"
                f"Content: {self.body}\n"
                f"Created: {self.created_at.strftime("%Y-%m-%d %H:%M:%S")}\n"
                f"Expires: {self.expires_at.strftime("%Y-%m-%d %H:%M:%S")}\n"
                f"Status: {"Completed" if self.status else "In process"}")


@dataclass
class UserDTO:
    login: str
    password_hash: str
    created_at: datetime = datetime.now()
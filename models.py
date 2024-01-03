import enum
from typing import Optional


class UserRole(enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"


class UserStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    IN_ACTIVE = "IN_ACTIVE"
    BLOCKED = "BLOCKED"


class TodoType(enum.Enum):
    WORK = "WORK"
    HOME = "HOME"
    SHOPPING = "SHOPPING"
    OTHER = "OTHER"


class User:
    def __init__(self, id: int, username: str,
                 password: str,
                 status: Optional[UserStatus],
                 role: Optional[UserRole],
                 login_try_count: Optional[int]
                 ):
        self.id = id
        self.username = username
        self.password = password
        self.status = status or UserStatus.IN_ACTIVE.value
        self.role = role or UserRole.USER.value
        self.login_try_count = login_try_count or 0

    @classmethod
    def from_tuple(cls, args):
        return cls(id=args[0],
                   username=args[1],
                   password=args[2],
                   status=args[3],
                   role=args[4],
                   login_try_count=args[5]
                   )

    def __repr__(self):
        return f"{self.username}:{self.status}:{self.role}"


class Todo:
    def __init__(self, id=None, name=None, user_id=None, type=None, completed=False):
        self.id = id
        self.name = name
        self.user_id = user_id
        self.type = type
        self.completed = completed

    @classmethod
    def from_tuple(cls, args):
        return cls(
            id=args[0],
            name=args[1],
            type=args[2],
            user_id=args[3],
            completed=args[4]
        )

    def __repr__(self):
        return f"Todo(id={self.id}, name='{self.name}', type='{self.type}', user_id={self.user_id}, completed={self.completed})"

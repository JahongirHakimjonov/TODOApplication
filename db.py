import sqlite3
import time
from os.path import exists

import models
import utils

db = "db.sqlite"
while not exists(db):
    print(db, "-- > doesnot exists")
    time.sleep(1)

connection = sqlite3.connect("db.sqlite")
cursor = connection.cursor()


def commit(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        connection.commit()
        return result

    return wrapper


create_user_table_sql = """
    create table if not exists users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username varchar(40) unique not null,
        password varchar(60) not null,
        status varchar(20) not null,
        role varchar(20) not null,
        login_try_count int default 0
    );
"""
create_todo_sql = """
    create table if not exists todos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name varchar(30) not null,
        type varchar(20) not null,
        completed bool default false,
        user_id int references users(id)
);
"""


@commit
def init():
    cursor.execute(create_user_table_sql)
    cursor.execute(create_todo_sql)


inser_into_sql = """
    insert into users(username, password, status, role) values (?,?,?,?)
"""


@commit
def create_todo_init():
    insert_todo_sql = """
    insert into todos(name, type,user_id) values (?,?,?);
    """
    cursor.execute(insert_todo_sql, ('Study English', "STUDY", 1))


def increase_user_try_count(username):
    increase_try_count_sql = """update users set login_try_count=login_try_count+1 where username=? """
    cursor.execute(increase_try_count_sql, (username,))


def get_user_by_username(username: str):
    get_user_sql = "select id, username, password, status, role, login_try_count from users where username=?"
    cursor.execute(get_user_sql, (username,))
    user_data = cursor.fetchone()
    return user_data


@commit
def insert_into_user(username, password, status, role):
    insert_into_user_sql = "insert into users(username, password, status, role) values (?,?,?,?)"
    cursor.execute(insert_into_user_sql,
                   (username, password, status, role))


def reset_login_try_count(username):
    reset_login_try_count_sql = "update users set login_try_count=0 where username=?"
    cursor.execute(reset_login_try_count_sql, (username,))
    return cursor.rowcount > 0


def set_user_status(username, status):
    set_user_status_sql = """update users set status=? where username=? """
    cursor.execute(set_user_status_sql, (status, username,))
    return cursor.rowcount > 0


def get_user_role(username):
    get_user_role_sql = "select role from users where username=?"
    cursor.execute(get_user_role_sql, (username,))
    user_role = cursor.fetchone()
    return user_role[0] if user_role else None


@commit
def insert_into_todo_item(todo: models.Todo):
    insert_todo_sql = """
    insert into todos(name, type,user_id) values (?,?,?);
    """
    cursor.execute(insert_todo_sql, (todo.name, todo.type.name, todo.user_id))


def get_todo_by_id(id):
    get_todo_sql = """SELECT * FROM todos WHERE id = ?"""
    cursor.execute(get_todo_sql, (id,))
    todo_data = cursor.fetchone()
    return todo_data


@commit
def delete_todo_by_id(id):
    cursor.execute("DELETE FROM todos WHERE id = ?", (id,))
    return cursor.rowcount > 0


def get_all_todos(user_id):
    get_all_todos_sql = """select * from todos where user_id = ?"""
    cursor.execute(get_all_todos_sql, (user_id,))
    todos_data = cursor.fetchall()
    return todos_data


@commit
def complete_todo_by_id(id):
    cursor.execute("UPDATE todos SET completed = 1 WHERE id = ?", (id,))
    return cursor.rowcount > 0


@commit
def create_user_with_role(username, password, role):
    hashed_password = utils.encode_password(password)
    cursor.execute(inser_into_sql, (username, hashed_password, models.UserStatus.ACTIVE.value, role))


@commit
def unblock_user(username):
    unblock_user_sql = "update users set status = ?, login_try_count = ? where username = ?"
    cursor.execute(unblock_user_sql, (models.UserStatus.IN_ACTIVE.value, 0, username))


@commit
def unblock_admin(username):
    unblock_user_sql = "update users set status = ?, login_try_count = ? where username = ?"
    cursor.execute(unblock_user_sql, (models.UserStatus.IN_ACTIVE.value, 0, username))


@commit
def current_user(username):
    current_user_sql = "select id, username, password, status, role, login_try_count from users where username=?"
    cursor.execute(current_user_sql, (username,))
    user_data = cursor.fetchone()
    return user_data


@commit
def set_user_status_inactive(username):
    cursor.execute("UPDATE users SET status = ? WHERE username = ?", (models.UserStatus.IN_ACTIVE.value, username))

# if __name__ == '__main__':
# init()
# create_todo_init()

# create_user_with_role("new_admin", "password", models.UserRole.ADMIN.value)
# create_user_with_role("jahongir", "777", models.UserRole.SUPER_ADMIN.value)
# create_user_with_role("krinj", "777", models.UserRole.USER.value)

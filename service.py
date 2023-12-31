import db
import models
import utils
from db import commit


@commit
def login_user(username, password):
    user_data = db.get_user_by_username(username)
    if user_data is None:
        return utils.ResponseDate("User Not Found", False)
    user = models.User.from_tuple(user_data)
    if user.status == "BLOCKED":
        return utils.ResponseDate("Bad Credintials", False)
    if user.login_try_count >= 3:
        db.set_user_status(username, "BLOCKED")
        return utils.ResponseDate("Bad Credintials user tried 3 times", False)
    if not utils.match_password(password, user.password):
        db.increase_user_try_count(username)
        return utils.ResponseDate("Username or password wrong", False)
    db.reset_login_try_count(username)
    db.set_user_status(username, models.UserStatus.ACTIVE.value)
    return utils.ResponseDate({"role": user.role, "username": user.username, "status": user.status})


@commit
def register_user(username, password):
    existing_user = db.get_user_by_username(username)
    if existing_user:
        return utils.ResponseDate("Username already exists", False)

    hashed_password = utils.encode_password(password)
    db.insert_into_user(username, hashed_password, models.UserStatus.IN_ACTIVE.value, models.UserRole.USER.value)
    return utils.ResponseDate("User registered successfully")


@commit
def create_todo_service(name, type, user_id):
    todo = models.Todo(name=name, type=models.TodoType[type], user_id=user_id)
    db.insert_into_todo_item(todo)
    return utils.ResponseDate("Todo created successfully")


@commit
def complete_todo_by_id(id):
    if db.complete_todo_by_id(id):
        return utils.ResponseDate("Todo completed successfully")
    else:
        return utils.ResponseDate("Failed to complete todo", False)


def get_todo_by_id(id):
    todo_data = db.get_todo_by_id(id)
    if todo_data is None:
        raise ValueError(f"No todo found with id: {id}")
    return models.Todo.from_tuple(todo_data)


def get_user_id(username):
    user_data = db.get_user_by_username(username)
    if user_data is None:
        raise ValueError(f"No user found with username: {username}")
    user = models.User.from_tuple(user_data)
    return user.id


@commit
def get_todo_by_username():
    todo_data = db.get_todo_by_username()
    if todo_data:
        return models.Todo.from_tuple(todo_data)
    else:
        return None


@commit
def delete_todo_by_id(id):
    if db.delete_todo_by_id(id):
        return utils.ResponseDate("Todo deleted successfully")
    else:
        return utils.ResponseDate("Failed to delete todo", False)


@commit
def get_all_todos(user_id):
    todos_data = db.get_all_todos(user_id)
    todos = [models.Todo.from_tuple(todo_data) for todo_data in todos_data]
    return utils.ResponseDate(todos)


@commit
def block_user(username):
    if db.set_user_status(username, "BLOCKED"):
        return utils.ResponseDate("User blocked successfully")
    else:
        return utils.ResponseDate("Failed to block user", False)


@commit
def unblock_user(username):
    db.unblock_user(username)
    return (utils.ResponseDate("User unblocked successfully"))


@commit
def block_admin(admin_username, blocker_username):
    blocker_role = db.get_user_role(blocker_username)
    if blocker_role in ["ADMIN", "SUPER_ADMIN"]:
        if db.set_user_status(admin_username, "BLOCKED"):
            return utils.ResponseDate("Admin blocked successfully")
        else:
            return utils.ResponseDate("Failed to block admin", False)
    else:
        return utils.ResponseDate("Permission denied", False)


@commit
def unblock_admin(admin_username, unblocker_username):
    unblocker_role = db.get_user_role(unblocker_username)
    if unblocker_role in ["ADMIN", "SUPER_ADMIN"]:
        if db.set_user_status(admin_username, "IN_ACTIVE"):
            if db.reset_login_try_count(admin_username):
                return utils.ResponseDate("Admin unblocked and login try count reset successfully")
            else:
                return utils.ResponseDate("Failed to reset login try count", False)
        else:
            return utils.ResponseDate("Failed to unblock admin", False)
    else:
        return utils.ResponseDate("Permission denied", False)


@commit
def logout_user(username):
    db.set_user_status_inactive(username)
    return utils.ResponseDate("User logged out successfully")


@commit
def get_my_profile(username):
    user_data = db.current_user(username)
    user = models.User.from_tuple(user_data)
    return utils.ResponseDate({"ID": user.id, "username": user.username, "status": user.status, "role": user.role})


@commit
def delete_user(username):
    if db.delete_user(username):
        return utils.ResponseDate("User deleted successfully")
    else:
        return utils.ResponseDate("Failed to delete user", False)


@commit
def promote_to_admin(username):
    if db.promote_to_admin(username):
        return utils.ResponseDate("User promoted to admin successfully")
    else:
        return utils.ResponseDate("Failed to promote user to admin", False)


def check_user_admin_status(username):
    user_data = db.get_user_by_username(username)
    if user_data is None:
        return utils.ResponseDate("User not found", False)

    user = models.User.from_tuple(user_data)
    if user.role == models.UserRole.ADMIN.value:
        return utils.ResponseDate("User is already an admin", False)

    return utils.ResponseDate("User is not an admin")


def check_user_role_status(username):
    user_data = db.get_user_by_username(username)
    if user_data is None:
        return utils.ResponseDate("User not found", False)

    user = models.User.from_tuple(user_data)
    if user.role == models.UserRole.USER.value:
        return utils.ResponseDate("User is already an user", False)
    elif user.role == models.UserRole.SUPER_ADMIN.value:
        return utils.ResponseDate("User is a super admin", False)

    return utils.ResponseDate("User is not an user")


@commit
def demote_from_admin(username):
    if db.demote_from_admin(username):
        return utils.ResponseDate("User demoted from admin successfully")
    else:
        return utils.ResponseDate("Failed to demote user from admin", False)


@commit
def delete_todo_service(id, username):
    todo = db.get_todo_by_id(id)

    if todo is None:
        return utils.ResponseDate("Todo not found", False)

    if not todo.completed:
        return utils.ResponseDate("Todo not completed", False)

    logged_in_user_id = get_user_id(username)
    if todo.user_id != logged_in_user_id:
        return utils.ResponseDate("You can only delete your own todos", False)

    if db.delete_todo_by_id(id):
        return utils.ResponseDate("Todo deleted successfully")
    else:
        return utils.ResponseDate("Failed to delete todo", False)

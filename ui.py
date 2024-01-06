import models
import service
import utils
from utils import print_menu, print_error, print_success, print_response, print_massage

logged_in_user = None


def login():
    global logged_in_user
    username = input("username: ")
    password = input("password: ")
    response = service.login_user(username, password)
    if response.success:
        print_success("Logged in successfully")
        logged_in_user = username
        menu(response.data['role'])
    else:
        print_error(response.data)
        menu("guest")


def register():
    username = input("username: ")
    password = input("password: ")
    password2 = input("password again: ")
    if password != password2:
        print_error("Passwords do not match. Please try again.")
        return
    response = service.register_user(username, password)
    print_response(response)


def create_todo():
    global logged_in_user
    name = input("Todo name : ")
    print_menu("1.WORK")
    print_menu("2.HOME")
    print_menu("3.SHOPPING")
    print_menu("4.OTHER")
    types = {"1": models.TodoType.WORK.name, "2": models.TodoType.HOME.name, "3": models.TodoType.SHOPPING.name,
             "4": models.TodoType.OTHER.name}
    choice = input("choice: ")
    type = types[choice]
    user_id = service.get_user_id(logged_in_user)
    response = service.create_todo_service(name=name, type=type, user_id=user_id)
    utils.print_response(response)


def complete_todo():
    try:
        id = int(input("Todo id to complete: "))
    except ValueError:
        print_error("Invalid id. Please enter a valid integer.")
        return
    response = service.complete_todo_by_id(id)
    utils.print_response(response)


def delete_todo():
    global logged_in_user
    try:
        id = int(input("Enter the id of the todo to delete: "))
    except ValueError:
        print_error("Invalid id. Please enter a valid integer.")
        return

    response = service.delete_todo_service(id, logged_in_user)
    utils.print_response(response)
    if response.success:
        print(f"Todo with id {id} deleted successfully for user {logged_in_user}")


def todo_list():
    global logged_in_user
    if logged_in_user is None:
        print_error("No user is currently logged in")
        return

    user_id = service.get_user_id(logged_in_user)
    response = service.get_all_todos(user_id)

    if response.success:
        todos = response.data
        for todo in todos:
            print_massage(f"ID: {todo.id}, Name: {todo.name}, Type: {todo.type}, Completed: {todo.completed}")
    else:
        print_error(response.data)


def block_user():
    username = input("Username to block: ")
    response = service.block_user(username)
    utils.print_response(response)


def unblock_user():
    username = input("Enter the username of the user to unblock: ")
    response = service.unblock_user(username)
    print_response(response)


def block_admin():
    admin_username = input("Admin username to block: ")
    blocker_username = input("Your username: ")
    response = service.block_admin(admin_username, blocker_username)
    utils.print_response(response)


def unblock_admin():
    admin_username = input("Admin username to unblock: ")
    unblocker_username = input("Your username: ")
    response = service.unblock_admin(admin_username, unblocker_username)
    utils.print_response(response)


def logout():
    global logged_in_user
    if logged_in_user is None:
        print_error("No user is currently logged in")
        return
    response = service.logout_user(logged_in_user)
    utils.print_response(response)
    logged_in_user = None
    menu("guest")


def my_profile():
    global logged_in_user
    if logged_in_user is None:
        print_error("No user is currently logged in")
        return
    response = service.get_my_profile(logged_in_user)
    utils.print_response(response)


def delete_account():
    global logged_in_user
    if logged_in_user is None:
        print_error("No user is currently logged in")
        return

    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Verify the entered credentials
    response = service.login_user(username, password)
    if not response.success:
        print_error("Invalid credentials")
        return

    # Delete the user's account
    response = service.delete_user(username)
    if response.success:
        print_success("Account deleted successfully")
        logged_in_user = None
    else:
        print_error(response.data)


def add_admin():
    username = input("Enter the username of the user to promote to admin: ")
    response = service.check_user_admin_status(username)
    if not response.success:
        print_error(response.data)
        return

    response = service.promote_to_admin(username)
    print_response(response)


def remove_admin():
    username = input("Enter the username of the admin to demote: ")
    response = service.check_user_role_status(username)
    if not response.success:
        print_error(response.data)
        return

    response = service.demote_from_admin(username)
    print_response(response)


def create_admin():
    username = input("Enter the username for the new admin: ")
    password = input("Enter the password for the new admin: ")
    password2 = input("Re-enter the password for the new admin: ")
    if password != password2:
        print_error("Passwords do not match. Please try again.")
        return
    response = service.register_user(username, password)
    if response.success:
        promote_response = service.promote_to_admin(username)
        if promote_response.success:
            print_success("New admin created successfully")
        else:
            print_error(promote_response.data)
    else:
        print_error(response.data)


def menu(role="guest"):
    while True:
        guest_menu = ["=> login", "=> register", "=> quit"]
        user_menu = ["=> logout", "=> create_todo", "=> complete_todo", "=> delete_todo", "=> todo_list",
                     "=> my_profile", "=> delete_account",
                     "=> quit"]
        admin_menu = ["=> logout", "=> create_todo", "=> complete_todo", "=> delete_todo", "=> todo_list",
                      "=> block_user",
                      "=> unblock_user", "=> my_profile", "=> delete_account", "=> quit"]
        super_admin_menu = ["=> logout", "=> create_todo", "=> complete_todo", "=> delete_todo", "=> todo_list",
                            "=> block_user", "=> unblock_user", "=> block_admin", "=> unblock_admin", "=> my_profile",
                            "=> delete_account", "=> add_admin", "=> remove_admin", "=> create_admin", "=> quit"]

        if role == "guest":
            for item in guest_menu:
                print_menu(item)
        elif role == models.UserRole.USER.value:
            for item in user_menu:
                print_menu(item)
        elif role == models.UserRole.ADMIN.value:
            for item in admin_menu:
                print_menu(item)
        elif role == models.UserRole.SUPER_ADMIN.value:
            for item in super_admin_menu:
                print_menu(item)
        print()
        choice = input("> ?: ").lower()
        print()
        match choice:
            case "login":
                login()
                print(logged_in_user)
            case "register":
                register()
            case "logout":
                logout()
            case "create_todo":
                create_todo()
            case "complete_todo":
                complete_todo()
            case "delete_todo":
                delete_todo()
            case "todo_list":
                todo_list()
            case "block_user":
                block_user()
            case "unblock_user":
                unblock_user()
            case "block_admin":
                block_admin()
            case "unblock_admin":
                unblock_admin()
            case "my_profile":
                my_profile()
            case "delete_account":
                delete_account()
            case "add_admin":
                add_admin()
            case "remove_admin":
                remove_admin()
            case "create_admin":
                create_admin()
            case "quit":
                exit(0)
            case _:
                print_error("Wrong choice")


if __name__ == '__main__':
    menu()

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
    id = input("Todo id to complete: ")
    response = service.complete_todo_by_id(id)
    utils.print_response(response)


def delete_todo():
    global logged_in_user
    id = input("Enter the id of the todo to delete: ")

    todo = service.get_todo_by_id(id)

    if todo is None:
        print_error("Todo not found")
    elif not todo.completed:
        print_error("Todo not completed")
    elif todo.user_id != service.get_user_id(logged_in_user):
        print_error("You can only delete your own todos")
    else:
        response = service.delete_todo_by_id(id)
        utils.print_response(response)
        print(f"Todo with id {id} deleted successfully for user {logged_in_user}")


def todo_list():
    global logged_in_user
    user_id = service.get_user_id(logged_in_user)
    response = service.get_all_todos(user_id)
    if response.success:
        for todo in response.data:
            print_massage(
                f"ID: {todo.id}, Name: {todo.name}, Type: {models.TodoType[todo.type].name}, Completed: {str(todo.completed).lower()}")
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


def menu(role="guest"):
    while True:
        guest_menu = ["=> login", "=> register", "=> quit"]
        user_menu = ["=> logout", "=> create_todo", "=> complete_todo", "=> delete_todo", "=> todo_list",
                     "=> my_profile",
                     "=> quit"]
        admin_menu = ["=> logout", "=> create_todo", "=> complete_todo", "=> delete_todo", "=> todo_list",
                      "=> block_user",
                      "=> unblock_user", "=> my_profile", "=> quit"]
        super_admin_menu = ["=> logout", "=> create_todo", "=> complete_todo", "=> delete_todo", "=> todo_list",
                            "=> block_user", "=> unblock_user", "=> block_admin", "=> unblock_admin", "=> my_profile",
                            "=> quit"]

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
            case "quit":
                exit(0)
            case _:
                print_error("Wrong choice")


if __name__ == '__main__':
    menu()

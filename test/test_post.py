import requests


def test_post_users():
    url = "http://127.0.0.1:8000/users/"

    email = input("Enter email: ")
    password = input("Enter password: ")
    data = {"email": email, "password": password}

    response = requests.post(url, json=data)

    assert response.status_code == 200


def test_post_item():
    user_id = int(input("Enter user id: "))
    url = f'http://127.0.0.1:8000/users/{user_id}/items/'

    title = input("Enter title: ")
    description = input("Enter description (not required): ")
    data = {"title": title, "description": description}

    response = requests.post(url, json=data)

    assert response.status_code == 200


def test_edit_item():
    user_id = int(input("Enter user id: "))
    item_id = int(input("Enter item id: "))
    url = f'http://127.0.0.1:8000/users/{user_id}/item_edit/?item_id={item_id}'

    title = input("Enter title: ")
    description = input("Enter description (not required): ")
    data = {"title": title, "description": description}

    response = requests.post(url, json=data)

    assert response.status_code == 200


def test_post_privelige():
    user_id = int(input("Enter user id: "))
    for_user_id = int(input("Enter witch for user id: "))
    item_id = int(input("Enter item id: "))
    url = f'http://127.0.0.1:8000/users/{user_id}/item_edit/?for_user_id={for_user_id}&item_id={item_id}'

    read = input("Enter true or false: ")
    update = input("Enter true or false: ")
    data = {"read": read, "update": update}

    response = requests.post(url, json=data)

    assert response.status_code == 200
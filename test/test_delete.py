import requests


def test_delete_item():
    item_id = int(input("Enter item id: "))
    url = f"http://127.0.0.1:8000/items/{item_id}"

    response = requests.delete(url)

    assert response.status_code == 200


def test_delete_privelige():
    user_id = int(input("Enter user id: "))
    item_id = int(input("Enter item id: "))
    url = f"http://127.0.0.1:8000/users/{user_id}/delete_privelige/?item_id={item_id}"

    response = requests.delete(url)

    assert response.status_code == 200

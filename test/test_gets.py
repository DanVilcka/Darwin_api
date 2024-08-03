import requests


def make_get_request(api_path):
    base_url = "http://127.0.0.1:8000/"
    response = requests.get(f'{base_url}/{api_path}/')
    return response

def make_get_request_with_key(api_path, api_key):
    base_url = "http://127.0.0.1:8000/"
    response = requests.get(f'{base_url}/{api_path}/{api_key}/')
    return response

def test_get_users():
    api_path = "users"

    response = make_get_request(api_path=api_path)

    assert response.status_code == 200


def test_get_users_with_key():
    api_path = "users"
    api_key = input("Enter user_id: ")

    response = make_get_request_with_key(api_path=api_path, api_key=api_key)

    assert response.status_code == 200



def test_get_items():
    api_path = "items"

    response = make_get_request(api_path=api_path)

    assert response.status_code == 200


def test_get_items_with_key():
    api_path = "items"
    api_key = input("Enter item_id: ")

    response = make_get_request_with_key(api_path=api_path, api_key=api_key)

    assert response.status_code == 200
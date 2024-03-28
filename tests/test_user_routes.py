import pytest
from pydantic import ValidationError

@pytest.mark.register_normal_user_success
def test_register_normal_user_should_return_success_response(user_client, register_data):
    response = user_client.post("/api/v1/user",json=register_data,headers={"Content-Type": "application/json"},)
    assert response.status_code == 201

@pytest.mark.register_normal_user_fail
def test_register_normal_user_should_return_error_response(user_client, register_data):
    response = user_client.post("/api/v1/user",json={"username": "Manu1s",
        "email": "str2@gmail.com",
        "password": "ManuS123!",
        "location": "Nairobi",},headers={"Content-Type": "application/json"},)
    assert response.status_code == 400

@pytest.mark.login_success
def test_login_user_should_return_success_response(user_client, login_data, register_data):
    response = user_client.post("/api/v1/user",json=register_data,headers={"Content-Type": "application/json"},)
    assert response.status_code == 201
    response = user_client.post("/api/v1/login",json=login_data,headers={"Content-Type": "application/json"},)
    assert response.status_code == 200

@pytest.mark.login_fail
def test_login_user_should_return_error_response(user_client, login_data, register_data):
    response = user_client.post("/api/v1/user",json=register_data,headers={"Content-Type": "application/json"},)
    assert response.status_code == 201
    response = user_client.post("/api/v1/login",json={"username": "Manu1s", "password": "Secure12"},headers={"Content-Type": "application/json"},)
    assert response.status_code == 401


def test_login_user_with_wrong_password(user_client, register_data, login_data):
    response = user_client.post("/api/v1/user",json=register_data,headers={"Content-Type": "application/json"},)

    login_data["password"] = "WrongPassword"
    response = user_client.post(
        "/api/v1/login",
        json=login_data,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 401


def test_login_user_with_wrong_username(user_client, register_data, login_data):
    # response = user_client.post("/api/v1/user",json=register_data,headers={"Content-Type": "application/json"},)
    # with pytest.raises(ValidationError):
    login_data["username"] = "WrongEmail"
    print(login_data)
    response = user_client.post(
        "/api/v1/login",
        json=login_data,
        headers={"Content-Type": "application/json"},
    )
    print(login_data)
    print(response.json)
    assert response.status_code == 401



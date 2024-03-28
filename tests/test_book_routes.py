import pytest 
import responses


@pytest.mark.abc
@responses.activate
def test_post_book_success(book_client, login_token, authenticate_user):

    data = {
        "title": "RDBMS",
        "author": "C.J Date",
        "price": 1000,
        "quantity": 10,
    }

    response = book_client.post("/api/v1/books",
        json=data,
        headers={"Content-Type": "application/json", "Authorization": login_token},
    )
    assert response.status_code == 201

@pytest.mark.add_inventory_unauthorized
@responses.activate
def test_add_inventory_returns_unauthorized(book_client,login_token, authenticate_user):
    data = {
        "title": "RDBMS",
        "author": "C.J Date",
        "price": 1000,
        "quantity": 10,
    }

    response = book_client.post(
        "/api/v1/books",
        json=data,
        headers={"Content-Type": "application/json", "Authorization": login_token + "1"},
    )
    assert response.json == {"message": "Unable to connect to user service",'status':400}


@pytest.mark.update_inventory_succes
@responses.activate
def test_update_inventory_returns_success(book_client, login_token, authenticate_user):
    data = {
        "title": "RDBMS",
        "author": "C.J Date",
        "price": 1000,
        "quantity": 10,
    }

    response = book_client.post(
        '/api/v1/books',
        json=data,
        headers={"Content-Type": "application/json", "Authorization": login_token},
    )
    data = {
        "id": 1,
        "user_id":1,
        "price": 1000,
        "quantity": 10,
    }

    response = book_client.put(
        "/api/v1/books",
        json=data,
        headers={"Content-Type": "application/json", "Authorization": login_token},
    )
    assert response.status_code == 200


@pytest.mark.delete_inventory_success
@responses.activate
def test_delete_inventory_returns_success(book_client, login_token, authenticate_user):
    data = {
        "title": "RDBMS",
        "author": "C.J Date",
        "price": 1000,
        "quantity": 10,
    }

    response = book_client.post(
        '/api/v1/books',
        json=data,
        headers={"Content-Type": "application/json", "Authorization": login_token},
    )
    response = book_client.delete(
        '/api/v1/books?id=1',
        headers={"Content-Type": "application/json", "Authorization": login_token},
    )
    assert response.status_code == 200

@pytest.mark.get_inventory_success
def test_get_inventory_returns_success(book_client, login_token, authenticate_user):
    data = {
        "title": "RDBMS",
        "author": "C.J Date",
        "price": 1000,
        "quantity": 10,
    }

    response = book_client.post(
        '/api/v1/books',
        json=data,
        headers={"Content-Type": "application/json", "Authorization": login_token},
    )
    response = book_client.get(
        '/api/v1/books',
        headers={"Content-Type": "application/json", "Authorization": login_token},
    )
    print(response)
    assert response.status_code == 200


@pytest.mark.get_inventory_failure
def test_get_inventory_returns_failure(book_client, login_token, authenticate_user):

    response = book_client.get(
        '/api/v1/books?id=1',
        headers={"Content-Type": "application/json", "Authorization": login_token + "1"},
    )
    assert response.status_code == 400


@pytest.mark.validate_inventory_failure
def test_validate_inventory_returns_failure(book_client, login_token, authenticate_user):
    data = {
        "title": "RDBMS",
        "author": "C.J Date",
        "price": 1000,
        "quantity": 10,
    }

    response = book_client.post(
        '/api/v1/books',
        json=data,
        headers={"Content-Type": "application/json", "Authorization": login_token},
    )
    data = {
        "id": 1,
        "price": 1000,
        "quantity": 10,
    }

    response = book_client.put(
        '/api/v1/books',
        json=data,
        headers={"Content-Type": "application/json", "Authorization": login_token},
    )
    assert response.status_code == 200

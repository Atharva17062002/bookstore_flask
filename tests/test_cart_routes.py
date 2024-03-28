import pytest
import responses


@pytest.mark.add_to_cart_success
def test_add_to_cart_returns_success(
    book_client, cart_client, login_token, get_book_from_inventory, authenticate_user
):
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

    print(response.status_code)

    data1 = {"book_id": "1", "quantity": "1"}

    response = cart_client.post(
        "http://127.0.0.1:9001/api/v1/update",
        json=data1,
        headers={"Content-Type": "application/json", "Authorization": login_token},
    )
    print(response.json)
    assert response.status_code == 201


@pytest.mark.add_to_cart_unauthorized
def test_add_to_cart_returns_unauthorized(
    book_client, cart_client, login_token, get_book_from_inventory, authenticate_user
):

    data = {"book_id": "1", "quantity": "1"}

    response = cart_client.post(
        "http://127.0.0.1:9000/api/v1/update",
        json=data,
        headers={"Content-Type": "application/json", "Authorization": login_token + "1"},
    )
    assert response.status_code == 400


@pytest.mark.get_cart_success
def test_get_cart_returns_success(
    book_client, cart_client, login_token, get_book_from_inventory, authenticate_user
):
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

    data1 = {"book_id": "1", "quantity": "1"}

    response = cart_client.post(
        "http://127.0.0.1:9001/api/v1/update",
        json=data1,
        headers={"Content-Type": "application/json", "Authorization": login_token},
    )

    assert response.status_code == 201

    response = cart_client.get(
        "http://127.0.0.1:9001/api/v1/update",
        headers={"Content-Type": "application/json", "Authorization": login_token},
    )
    print(response.json)
    assert response.status_code == 200


@pytest.mark.get_cart_unauthorized
def test_get_cart_unauthorized(
    book_client, cart_client, login_token, get_book_from_inventory, authenticate_user
):
    response = cart_client.get(
        "http://127.0.0.1:9000/api/v1/update",
        headers={"Content-Type": "application/json", "Authorization": login_token + "1"},
    )
    assert response.status_code == 400

@pytest.mark.empty_cart_success
def test_empty_cart_returns_success(
    book_client, cart_client, login_token, get_book_from_inventory, authenticate_user
):
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

    print(response.status_code)

    data1 = {"book_id": "1", "quantity": "1"}

    response = cart_client.post(
        "http://127.0.0.1:9001/api/v1/update",
        json=data1,
        headers={"Content-Type": "application/json", "Authorization": login_token},
    )
    print(response.json)
    assert response.status_code == 201

    """Test to verify emptying the cart returns success."""
    response = cart_client.delete(
        'http://127.0.0.1:9000/api/v1/update?id=1',
        headers={"Content-Type": "application/json", "Authorization": login_token},
    )
    print(response.json)
    assert response.status_code == 200


@pytest.mark.empty_cart_unauthorized
def test_empty_cart_returns_unauthorized(
    book_client, cart_client, login_token, get_book_from_inventory, authenticate_user
):
    """Test to verify emptying the cart with unauthorized token returns error."""
    response = cart_client.delete(
        '/api/v1/update?id=1',
        headers={"Content-Type": "application/json", "Authorization": login_token + "1"},
    )

    assert response.status_code == 400


@pytest.mark.no_books_in_cart
def test_order_returns_no_books_in_cart(
    book_client, cart_client, login_token, get_book_from_inventory, authenticate_user
):
    """Test to verify ordering with no books in cart returns error."""
    response = cart_client.post(
        '/api/v1/order',
        headers={"Content-Type": "application/json", "Authorization": login_token},
    )
    assert response.status_code == 404


@pytest.mark.remove_from_success
def test_remove_from_success(
    book_client, cart_client, login_token, get_book_from_inventory, authenticate_user
):

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

    print(response.status_code)

    data1 = {"book_id": "1", "quantity": "1"}

    response = cart_client.post(
        "http://127.0.0.1:9001/api/v1/update",
        json=data1,
        headers={"Content-Type": "application/json", "Authorization": login_token},
    )
    print(response.json)
    assert response.status_code == 201

    """Test to verify removing from cart returns success."""
    data = {"book_id": "1", "quantity": "1", "operations": "remove"}

    response = cart_client.delete(
        '/api/v1/update?id=1',
        json=data,
        headers={"Content-Type": "application/json", "Authorization": login_token},
    )

    assert response.status_code == 200

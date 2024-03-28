import pytest
from app import create_app
from user.routes import UserAPI , LoginAPI
from user.models import db as user_db
from books.models import db as book_db
from books.routes import BooksAPI
from flask_restx import Api
from cart.routes import UpdateCart
from cart.models import db as cart_db
import responses


@pytest.fixture
def user_app():
    app = create_app("user", mode="test")
    user_db.init_app(app)

    with app.app_context():
        user_db.create_all()

    api = Api(app)
    api.add_resource(UserAPI, "/api/v1/user")
    api.add_resource(LoginAPI, "/api/v1/login")

    yield app
    with app.app_context():
        user_db.drop_all()

@pytest.fixture
def user_client(user_app):
    return user_app.test_client()

@pytest.fixture
def register_data():
    return {
            "username": "Manu1s",
            "email": "str2@gmail.com",
            "password": "Secure123",
            # "superuser": "",
            "location": "Nairobi",
    }

@pytest.fixture
def login_data():
    return {"username": "Manu1s", "password": "Secure123"}

@pytest.fixture
def book_app():
    app = create_app("book", mode="test")
    book_db.init_app(app)

    with app.app_context():
        book_db.create_all()

    api = Api(app)
    api.add_resource(BooksAPI, "/api/v1/books")

    yield app
    with app.app_context():
        book_db.drop_all()
    
@pytest.fixture()
def book_client(book_app):
    return book_app.test_client()

@pytest.fixture
def login_token(user_client):
    register_data = {
        "username": "Manu",
        "email": "17.atharva@gmail.com",
        "password": "Secure123",
        "location": "Bangalore",
        "super_key":"manuchutiya"
    }
    response = user_client.post('/api/v1/user', json=register_data,headers={'Content-Type': 'application/json'})
    new_user_data = response.get_json()['data']['id']
    login_data = {
        "username": "Manu",
        "password": "Secure123"
    }
    response = user_client.post('/api/v1/login', json=login_data,headers={'Content-Type': 'application/json'})
    token = response.get_json()['token']
    return token

@pytest.fixture()
def authenticate_user(login_token):
    with responses.RequestsMock(assert_all_requests_are_fired=False) as res:
        res = responses.add(
            method=responses.GET,
            url=f"http://127.0.0.1:5001/api/v1/authUser?token={login_token}",
            json={"message": "User authenticated successfully", "data": {
                "id": 1,
                "username": "Manu",
                "email": "17.atharva@gmail.com",
                "location": "Bangalore",
                "is_superuser": True,
            }}
        )
        return res

@pytest.fixture
def cart_app():
    app = create_app("cart", mode="test")
    cart_db.init_app(app)

    with app.app_context():
        cart_db.create_all()

    api = Api(app)
    api.add_resource(UpdateCart, "/api/v1/update")

    yield app
    with app.app_context():
        cart_db.drop_all()

@pytest.fixture
def get_book_from_inventory():
    with responses.RequestsMock(assert_all_requests_are_fired=False) as res:
        res = responses.add(
            method=responses.GET,
            url="http://127.0.0.1:7001/book/1",
            json={
                "data":{"title": "RDBMS",
                    "id": 1,
                    "author": "C.J Date",
                    "price": 1000,
                    "quantity": 10,}
            },
            status=200,
        )
        print(">>>>>>>>>>>>>>>>", res.body)

        return res


@pytest.fixture
def get_book_from_inventory_invalid():
    with responses.RequestsMock(assert_all_requests_are_fired=False) as res:
        res = responses.add(
            method=responses.GET,
            url="http://127.0.0.1:8000/api/v1/update/1",
            json={},
            status=404,
        )
        print(">>>>>>>>>>>>>>>>", res.body)

        return res

@pytest.fixture()
def cart_client(cart_app):
    return cart_app.test_client()
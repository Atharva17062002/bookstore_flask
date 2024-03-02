'''
1. Create a Book Model and migrate and upgrade it to db.
2. Book Model - id, title, author, image(optional), price, quantity, super_user_id(int, not nullable).
3. Perform CRUD on book model where only super user is allowed to perform CUD operations.
'''

from app import create_app
from passlib.hash import pbkdf2_sha256
from datetime import datetime, timedelta
from sqlalchemy.orm import Mapped
from typing import List
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from settings import settings
from app.utils import JWT

db_url = settings.book_database_uri
app = create_app(db_url)

db = SQLAlchemy()
migrate = Migrate()

db.init_app(app)
migrate.init_app(app, db)

class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False,)

class Book(BaseModel):
    __tablename__ = 'book'
    title = db.Column(db.String(100), nullable=False, unique=True)
    author = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    def __init__(self, title, author, price, quantity, user_id):
        self.title = title
        self.author = author
        self.price = price
        self.quantity = quantity
        self.user_id = user_id

    # def validate_super_key(self,super_key):
    #     if super_key == settings.super_key:
    #         self.is_superuser = True
    #     else:
    #         # self.is_superuser = False
    #         raise ValueError("Wrong super key")
    
    @property
    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "price": self.price,
            "quantity": self.quantity,
            "user_id": self.user_id
        }



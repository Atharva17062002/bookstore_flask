from app import create_app
from passlib.hash import pbkdf2_sha256
from datetime import datetime, timedelta
from sqlalchemy.orm import Mapped
from typing import List
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from settings import settings
from app.utils import JWT


db_url = settings.user_database_uri
app = create_app(db_url)

db = SQLAlchemy()
migrate = Migrate()

db.init_app(app)
migrate.init_app(app, db)

class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False,)

class User(BaseModel):
    __tablename__ = 'user'
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(100), nullable=True)
    is_verified = db.Column(db.Boolean, default=False)
    is_superuser = db.Column(db.Boolean, default=False)

    def __init__(self, username, email, password, location):
        self.username = username
        self.email = email
        self.password = pbkdf2_sha256.hash(password)
        self.location = location

    def validate_super_key(self,super_key):
        if super_key == settings.super_key:
            self.is_superuser = True
        else:
            # self.is_superuser = False
            raise ValueError("Wrong super key")

    def verify_password(self, raw_password):
        return pbkdf2_sha256.verify(raw_password, self.password)

    def generate_token(self, aud = "Default", exp = 15):
        payload = {"user_id":self.id, "aud":aud, "exp":datetime.utcnow() + timedelta(minutes=exp)}
        return JWT.to_encode(payload)

    @property
    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "location": self.location,
            "is_superuser": self.is_superuser,
    }

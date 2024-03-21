from pydantic import ValidationError
from flask import request
from flask_mail import Message
from settings import settings
import jwt
import json
from . import mail
import psycopg2
import sqlalchemy
import re
from log import set_logger

logger = set_logger()

def api_handler(body = None, query = None):
    def custom_validator(function):
        def wrapper(*args, **kwargs):
            try:
                if body:
                    body(**request.get_json())
                if query:
                    pass
                return function(*args, **kwargs)
            except sqlalchemy.exc.IntegrityError as e:
                logger.error(e)
                return {"message": "Data already exist","status": 400,"data":{}},400
            except psycopg2.errors.UniqueViolation as e:
                logger.error(e)
                return {"message": "Data already exist","status": 400,"data":{}},400
            except ValidationError as e:
                logger.error(e)
                return {"message": json.loads(e.json()),"status": 400,"data":{}},400
            except Exception as e:
                logger.error(e)
                return {"message": str(e),"status": 400,"data":{}},400
        wrapper.__name__ = function.__name__
        return wrapper
    custom_validator.__name__ = api_handler.__name__
    return custom_validator

class JWT:

    key = settings.jwt_key
    algorithm = settings.jwt_algo

    @classmethod
    def to_encode(cls,payload):
        encoded = jwt.encode(payload,cls.key,algorithm= cls.algorithm)
        return encoded
    
    @classmethod
    def to_decode(cls,encoded,aud):
        decoded = jwt.decode(encoded,cls.key,algorithms= [cls.algorithm],audience= aud)
        return decoded
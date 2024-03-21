from flask import request, g
from user.models import User
import jwt
from.utils import JWT
import requests as http
from requests.exceptions import ConnectionError, ConnectTimeout

def auth_user(func):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return {"message": "Token not found","status":404,"data":{}}, 404
        try:
            response = http.get(f"http://127.0.0.1:5001/api/v1/authUser", params={"token": token})
            if response.status_code >= 400:
                return {"message": response.json()['message'], "status":401}, 401 
            user_data = response.json()['data']
            g.user = user_data
            request.json.update({"user_id":user_data["id"]}) if request.method in ['POST', 'PUT'] else kwargs.update({"user_id":user_data["id"]})
        except ConnectionError as e:
            return {"message": "Unable to connect to user service", "status":400}, 400
        except ConnectTimeout as e:
            return {"message": "Connection timeout", "status":400}, 400
        except Exception as e:
            return {"message": str(e), "status":400, "data":{}}, 400
        return func(*args, **kwargs) 

    wrapper.__name__ = func.__name__
    return wrapper
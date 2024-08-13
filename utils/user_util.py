import bcrypt
import os
from utils.status import *
from functools import wraps
from fastapi import Depends
from fastapi_jwt_auth import AuthJWT
from jwt import ExpiredSignatureError, InvalidTokenError
import logging
import datetime

def get_hashed_password(password):
    """Hash password using bcrypt"""
    pwhash = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
    return pwhash.decode('utf8')


def check_password(plain_text_password, hashed_password):
    """Check hashed password. Password should be already hashed"""
    # encoding password with utf-8
    password_bytes = plain_text_password.encode('utf-8')
    # enoding hashed password with utf-8 as it is stored as string in the db
    hashed_password_bytes = hashed_password.encode('utf-8')
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)





# def get_jwt_token(user_email, Authorize: AuthJWT):
#     """Generate JWT token for user"""
#     expires = datetime.timedelta(days=1)
#     access_token = Authorize.create_access_token(subject=user_email, expires_time=expires)
#     return access_token
def get_jwt_token(user_email: str, Authorize: AuthJWT = Depends()):
    """Generate JWT token for user"""
    expires = datetime.timedelta(days=1)
    access_token = Authorize.create_access_token(subject=user_email, expires_time=expires)
    return access_token


def validate_token(func):
    """Validate JWT token"""

    @wraps(func)
    def wrapper(Authorize: AuthJWT = Depends(), *args, **kwargs):
        try:
            Authorize.jwt_required()
            return func(*args, **kwargs)
        except ExpiredSignatureError as e:
            return {"message": "Invalid token, Signature expired", "data": None}, HTTP_401_UNAUTHORIZED
        except InvalidTokenError as e:
            return {"message": "Invalid token", "data": None}, HTTP_401_UNAUTHORIZED
        except Exception as e:
            logging.error(e)
            return {"message": INTERNAL_SERVER_ERROR, "data": None}, HTTP_500_INTERNAL_SERVER_ERROR

    return wrapper

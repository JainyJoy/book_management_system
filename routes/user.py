from fastapi import APIRouter, Depends, Request
import datetime
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
import logging
from controller import UserController
from validator import RegistrationPayload, LoginPayload
from utils.status import *

router = APIRouter(tags=["User Management"])
__usr_controller = UserController()


@router.get("/health")
def get():
    return "OK, intelligent book management system is up", HTTP_200_OK


@router.post("/register")
async def register_users(payload: RegistrationPayload):
    try:
        msg, status_code = await __usr_controller.register_user(payload.dict())
        return JSONResponse({"message": msg, "data": None}, status_code)
    except ValueError as e:
        logging.error(e)
        return JSONResponse({"message": str(e), "data": None}, HTTP_400_BAD_REQUEST)
    except Exception as e:
        logging.error(e)
        return JSONResponse({"message": INTERNAL_SERVER_ERROR, "data": None}, HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/login")
async def user_login(payload: LoginPayload, Authorize: AuthJWT = Depends()):
    try:
        msg, status_code = await __usr_controller.login_user(payload.dict())
        if status_code == HTTP_200_OK:
            expires = datetime.timedelta(days=1)
            access_token = Authorize.create_access_token(subject=payload.email, expires_time=expires)
            return JSONResponse(status_code=status_code, content={"message": SUCCESS_MSG, "access_token": access_token})
    except ValueError as e:
        logging.error(e)
        return JSONResponse({"message": str(e), "data": None}, HTTP_400_BAD_REQUEST)
    except Exception as e:
        logging.error(e)
        return JSONResponse({"message": INTERNAL_SERVER_ERROR, "data": None}, HTTP_500_INTERNAL_SERVER_ERROR)







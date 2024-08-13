from fastapi import APIRouter, Depends, Header
from fastapi.responses import JSONResponse
import logging

from fastapi_jwt_auth import AuthJWT

from controller import BookController
from validator import BookCreationPayload, BookUpdatePayload
from utils.status import *

router = APIRouter(tags=["Register Book"])
__book_controller = BookController()


@router.get("/books/{book_id}")
@router.get("/books")
async def create_config(book_id: int = None, authorization: str = Header(None, description="Bearer <your_jwt_token>"),
                        Authorize: AuthJWT = Depends()):
    try:
        access_token = authorization.split("Bearer ")[1]
        Authorize.jwt_required(token=access_token)
        data = await __book_controller.get_all_books(book_id)
        if isinstance(data, list) and not data:
            return JSONResponse({"message": NOT_FOUND_MSG, "data": None}, HTTP_404_NOT_FOUND)
        return JSONResponse({"message": SUCCESS_MSG, "data": data}, HTTP_200_OK)
    except Exception as e:
        logging.error(e)
        return JSONResponse({"message": INTERNAL_SERVER_ERROR, "data": None}, HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/books")
async def create_book(payload: BookCreationPayload,
                      authorization: str = Header(None, description="Bearer <your_jwt_token>"),
                      Authorize: AuthJWT = Depends()):
    try:
        access_token = authorization.split("Bearer ")[1]
        Authorize.jwt_required(token=access_token)
        resp = await __book_controller.create_book(payload.dict())
        if resp is not True:
            return JSONResponse({"message": resp, "data": None}, HTTP_400_BAD_REQUEST)
        return JSONResponse({"message": CREATED_MSG, "data": None}, HTTP_201_CREATED)
    except ValueError as e:
        logging.error(e)
        return JSONResponse({"message": str(e), "data": None}, HTTP_400_BAD_REQUEST)
    except Exception as e:
        logging.error(e)
        return JSONResponse({"message": INTERNAL_SERVER_ERROR, "data": None}, HTTP_500_INTERNAL_SERVER_ERROR)


@router.put("/books/{book_id}")
async def update_book(book_id: int, payload: BookUpdatePayload,
                      authorization: str = Header(None, description="Bearer <your_jwt_token>"),
                      Authorize: AuthJWT = Depends()):
    try:
        access_token = authorization.split("Bearer ")[1]
        Authorize.jwt_required(token=access_token)
        resp = await __book_controller.update_book_by_id(book_id, payload.dict())
        if resp is True:
            return JSONResponse({"message": SUCCESS_MSG, "data": None}, HTTP_200_OK)
        if resp is False:
            return JSONResponse({"message": NOT_FOUND_MSG, "data": None}, HTTP_404_NOT_FOUND)
    except ValueError as e:
        logging.error(e)
        return JSONResponse({"message": str(e), "data": None}, HTTP_400_BAD_REQUEST)
    except Exception as e:
        logging.error(e)
        return JSONResponse({"message": INTERNAL_SERVER_ERROR, "data": None}, HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/books/{book_id}")
async def delete_book(book_id: int, authorization: str = Header(None, description="Bearer <your_jwt_token>"),
                      Authorize: AuthJWT = Depends()):
    try:
        access_token = authorization.split("Bearer ")[1]
        Authorize.jwt_required(token=access_token)
        await __book_controller.delete_book_by_id(book_id)
        return JSONResponse({"message": SUCCESS_MSG, "data": None}, HTTP_200_OK)
    except ValueError as e:
        logging.error(e)
        return JSONResponse({"message": str(e), "data": None}, HTTP_400_BAD_REQUEST)
    except Exception as e:
        logging.error(e)
        return JSONResponse({"message": INTERNAL_SERVER_ERROR, "data": None}, HTTP_500_INTERNAL_SERVER_ERROR)

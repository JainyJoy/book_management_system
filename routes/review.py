from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

import logging
from controller import BookController
from validator import ReviewCreationPayload
from utils.status import *

router = APIRouter(tags=["Book Review"])
__book_controller = BookController()


@router.get("/books/{book_id}/reviews")
async def get_book_review(book_id: int):
    try:
        data = await __book_controller.get_all_book_reviews(book_id)
        if isinstance(data, list) and data:
            return JSONResponse({"message": SUCCESS_MSG, "data": data}, HTTP_200_OK)
        if isinstance(data, list) and not data:
            return JSONResponse({"message": NOT_FOUND_MSG, "data": None}, HTTP_404_NOT_FOUND)
    except Exception as e:
        logging.error(e)
        return JSONResponse({"message": INTERNAL_SERVER_ERROR, "data": None}, HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/books/{book_id}/reviews")
async def post(book_id: int, payload: ReviewCreationPayload):
    try:
        payload = payload.dict()
        payload["book_id"] = book_id
        await __book_controller.add_book_review(payload)
        return JSONResponse({"message": CREATED_MSG, "data": None}, HTTP_201_CREATED)
    except ValueError as e:
        logging.error(e)
        return JSONResponse({"message": str(e), "data": None}, HTTP_400_BAD_REQUEST)
    except Exception as e:
        logging.error(e)
        return JSONResponse({"message": INTERNAL_SERVER_ERROR, "data": None}, HTTP_500_INTERNAL_SERVER_ERROR)

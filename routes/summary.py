from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

import logging
from controller import BookController
from utils.status import *

router = APIRouter(tags=["Book Summary"])
__book_controller = BookController()


@router.get("/books/{book_id}/summary")
async def get_book_summary(book_id: int):
    try:
        data = await __book_controller.get_summary_aggregated_book_reviews(book_id)
        if isinstance(data, list) and data:
            return JSONResponse({"message": SUCCESS_MSG, "data": data}, HTTP_200_OK)
        elif isinstance(data, list) and not data:
            return JSONResponse({"message": NOT_FOUND_MSG, "data": None}, HTTP_404_NOT_FOUND)
    except Exception as e:
        logging.error(e)
        return JSONResponse({"message": INTERNAL_SERVER_ERROR, "data": None}, HTTP_500_INTERNAL_SERVER_ERROR)



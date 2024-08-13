from repository import BookRepository
from utils.status import *

class BookController:
    def __init__(self):
        self.__book_repo = BookRepository()

    async def create_book(self, payload):
        check = await self.__book_repo.check_book_by_title(payload["title"])
        if check:
            return "Book already exists with the same title"
        return await self.__book_repo.create_book(payload)

    async def get_book_by_id(self, book_id):
        return await self.__book_repo.get_book_by_id(book_id)

    async def get_all_books(self, book_id=None):
        if book_id:
            return await self.__book_repo.get_book_by_id(book_id)
        return await self.__book_repo.get_all_books()

    async def update_book_by_id(self, book_id, payload):
        return await self.__book_repo.update_book_by_id(book_id, payload)

    async def delete_book_by_id(self, book_id):
        return await self.__book_repo.delete_book_by_id(book_id)

    async def add_book_review(self, payload):
        return await self.__book_repo.add_book_review(payload)

    async def get_all_book_reviews(self, book_id):
        return await self.__book_repo.get_reviews_by_book_id(book_id)

    async def get_summary_aggregated_book_reviews(self, book_id):
        return await self.__book_repo.get_summary_aggregated_book_reviews(book_id)

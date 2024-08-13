from database.postgres import session_obj, Book, Review
from sqlalchemy import func, text
from sqlalchemy.future import select



class BookRepository:
    def __init__(self):
        pass

    async def create_book(self, payload):
        """Create a Book"""
        async with session_obj() as session:
            async with session.begin():
                book = Book(**payload)
                session.add(book)
                session.commit()
                session.refresh(book)
        return True

    async def get_book_by_id(self, book_id):
        async with session_obj() as session:
            async with session.begin():
                stmt = select(Book).filter_by(id=book_id)
                result = await session.execute(stmt)
                book = result.scalars().first()
        if book is not None:
            return[{
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'genre': book.genre,
                'year_published': book.year_published,
                'summary': book.summary
            }]
        return []

    async def get_all_books(self):
        resp = []
        async with session_obj() as session:
            async with session.begin():
                stmt = select(Book).filter_by()
                result = await session.execute(stmt)
                books = result.scalars().all()
        for book in books:
            resp.append({
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'genre': book.genre,
                'year_published': book.year_published,
                'summary': book.summary
            })
        return resp

    async def update_book_by_id(self, book_id, payload):
        async with session_obj() as session:
            async with session.begin():
                stmt = select(Book).filter_by(id=book_id)
                result = await session.execute(stmt)
                book = result.scalars().first()
            if not book:
                return False
            book.title = payload["title"] if payload.get("title") is not None else book.title
            book.author = payload["author"] if payload.get("author") is not None else book.author
            book.genre = payload["genre"] if payload.get("genre") is not None else book.genre
            book.year_published = payload["year_published"] if payload.get("year_published") is not None else book.year_published
            book.summary = payload["summary"] if payload.get("summary") is not None else book.summary
            session.commit()
            session.refresh(book)
        return True

    async def delete_book_by_id(self, book_id):
        async with session_obj() as session:
            async with session.begin():
                stmt = select(Book).filter_by(id=book_id)
                result = await session.execute(stmt)
                book = result.scalars().first()
            if not book:
                return True
            await session.delete(book)
            await session.commit()
        return True

    async def add_book_review(self, payload):
        async with session_obj() as session:
            async with session.begin():
                review = Review(**payload)
                session.add(review)
                await session.commit()
                session.refresh(review)
        return True

    async def get_reviews_by_book_id(self, book_id):
        reviews_resp = []
        async with session_obj() as session:
            async with session.begin():
                stmt = select(Review).filter_by(book_id=book_id)
                result = await session.execute(stmt)
                reviews = result.scalars().all()
        if reviews is not None:
            for review in reviews:
                reviews_resp.append({
                    'id': review.id,
                    'book_id': review.book_id,
                    'rating': review.review_text
                })
        return reviews_resp

    async def get_summary_aggregated_book_reviews(self, book_id):
        async with session_obj() as session:
            async with session.begin():
                # stmt = (
                #     select(
                #         Book.title,
                #         Book.summary,
                #         func.avg(Review.rating).label('aggregate_rating')
                #     )
                #     .join(Review, Book.id == Review.book_id)
                #     .filter(Book.id == id)
                #     .group_by(Book.id)
                # )
                query = f"SELECT book.title,book.summary, AVG(reviw.rating) AS aggregate_rating FROM books book JOIN reviews reviw ON book.id = reviw.book_id " \
                         f"WHERE book.id = :book_id GROUP BY book.id LIMIT 1"
                result = await session.execute(text(query), {'book_id': book_id})
                resp = result.fetchone()

        if not resp:
            return []
        return [{
            'title': resp[0],
            'summary': resp[1],
            'aggregated_rating_rounded': round(resp[2])
        }]

    async def check_book_by_title(self, book_title):
        async with session_obj() as session:
            async with session.begin():
                stmt = select(Book).filter_by(title=book_title)
                result = await session.execute(stmt)
                book = result.scalars().first()
        if book is not None:
            return True
        return False

import pytest
from repository.book_repo import BookRepository

@pytest.mark.asyncio
async def test_add_book_review():
    # Create BookRepository instance
    book_repo = BookRepository()

    # Define a payload for adding a book review
    payload = {
        'book_id': 1,
        'rating': 5,
        'review_text': 'This is a great book!'
    }

    # Call the function and get the result
    result = await book_repo.add_book_review(payload)

    # Perform assertions on the result
    assert result is True  # Check if the result is True, indicating successful review addition


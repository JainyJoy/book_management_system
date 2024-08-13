import pytest
from repository.book_repo import BookRepository

@pytest.mark.asyncio
async def test_create_book():
    # Create  BookRepository instance
    book_repo = BookRepository()

    # Define a payload for creating a book
    payload = {
        'title': 'Sample Book ABC',
        'author': 'Author G',
        'genre': 'Sample Genre',
        'year_published': 2024,
        'summary': 'This is a sample book summary.'
    }

    # Call the function and get the result
    result = await book_repo.create_book(payload)

    # Perform assertions on the result
    assert result is True  # Check if the result is True, indicating successful book creation

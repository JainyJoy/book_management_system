import pytest
from repository.book_repo import BookRepository

@pytest.mark.asyncio
async def test_get_summary_aggregated_book_reviews():
    # Create a BookRepository instance
    book_repo = BookRepository()

    book_id = 1

    result = await book_repo.get_summary_aggregated_book_reviews(book_id)


    assert isinstance(result, list)  # Check if the result is a list
    assert len(result) == 1  # Check if the result contains one item
    assert 'title' in result[0]  # Check if 'title' key is present
    assert 'summary' in result[0]  # Check if 'summary' key is present
    assert 'aggregated_rating_rounded' in result[0]  # Check if 'aggregated_rating_rounded' key is present
    assert isinstance(result[0]["aggregated_rating_rounded"], int)
docker build -t book_management_service .
docker run --net=host -v $(pwd):/BOOK_MNGMT_SERVICE --name book_management_service -d book_management_service
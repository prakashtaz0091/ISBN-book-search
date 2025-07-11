import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import BookSerializer


@api_view(['GET'])
def search(request, isbn):
    """
    API endpoint to search for a book by its ISBN.

    Args:
        request: The request object.
        isbn: The ISBN of the book to search for.

    Returns:
        A JSON response with the book's title, authors, publisher, publish date, and ISBN.
        If the book is not found, returns a 404 Not Found response with an error message.
        If the request to the Open Library API fails, returns a 503 Service Unavailable response with an error message.
    """
        

    # Open Library API endpoint
    url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"

    try:
        response = requests.get(url)
        data = response.json()
        
        book_data = data.get(f"ISBN:{isbn}")
        if not book_data:
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

        # Extract required fields
        serialized_data = {
            "title": book_data.get("title", ""),
            "authors": [author.get("name") for author in book_data.get("authors", [])],
            "publisher": book_data.get("publishers", [{}])[0].get("name", ""),
            "publish_date": book_data.get("publish_date", ""),
            "isbn": isbn
        }

        serializer = BookSerializer(data=serialized_data)
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except requests.RequestException:
        return Response({"error": "Failed to fetch data from Open Library."},
                        status=status.HTTP_503_SERVICE_UNAVAILABLE)

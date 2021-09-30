"""File has book api endpoints resources"""

from api.models import Book
from api.admin.validate import validate_arg
from flask_restful import Resource
from flask import json, request, Response


class GetBooks(Resource):
    """Get books resource"""

    def get(self):
        """Function serving get all books api endpoint"""
        q = request.args.get("q")
        print(q)
        if q:
            return Response(json.dumps(Book.search(q)), status=200)
        page = request.args.get("page")
        page = int(page) if page else 1
        limit = request.args.get("limit")
        limit = int(limit) if limit else 10
        books = Book.query.paginate(page=page, per_page=limit, error_out=False)
        all_books = books.items
        if len(all_books) == 0:
            return Response(json.dumps({"Message": "No books found"}), status=404)
        total_pages = books.pages
        current_page = books.page
        return Response(json.dumps({"Books": [book.serialize for book in all_books], "totalPages": total_pages,
                                    "currentPage": current_page}), status=200)


class GetBook(Resource):
    """Getting a book resource"""

    def get(self, book_id):
        """Function serving get a book api endpoint"""
        if validate_arg(book_id):
            return validate_arg(book_id)
        book = Book.get_book_by_id(id=book_id)
        if not book:
            return Response(json.dumps({"Message": "Book does not exist"}), status=404)
        return Response(json.dumps(book.serialize), status=200)

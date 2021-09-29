"""File has admin endpoints resources"""

from api import jwt
from api.models import Book, User, ReviewBook
from api.admin.validate import validate_book, validate_arg
from flask_restful import Resource
from flask import json, request, Response
from flask_jwt_extended import get_jwt_identity, jwt_required


class AddBook(Resource):
    """Add Book API endpoint Resource"""

    @jwt_required
    def post(self):
        """Method serving add book api endpoint"""
        current_user = get_jwt_identity()
        user = User.get_user_by_username(current_user)
        if user:
            if user.is_admin:
                data = request.get_json(self)
                if validate_book(data):
                    return Response(json.dumps(validate_book(data)), status=400)
                if len(data['isbn']) not in (10, 13):
                    return Response(json.dumps({"Message": "Invalid ISBN"}), status=403)
                isbn = Book.query.filter_by(isbn=data['isbn']).first()
                if isbn:
                    return Response(json.dumps({"Message": "Book already exists"}), status=409)
                Book(data['title'], data['author'], data['isbn'],
                     data['publisher'], data['quantity']).save()
                book = Book.query.filter_by(isbn=data['isbn']).first()
                return Response(json.dumps({"Message": "Book added successfully", "Book": book.serialize}), status=201)
            return Response(json.dumps({"Message": "User not an admin"}), status=401)
        return Response(json.dumps({"Message": "User does not exist"}), status=404)


class BookOps(Resource):
    """BookOps (Edit and Delete) Resource"""

    @jwt_required
    def put(self, book_id):
        """Function serving edit book api endpoint"""
        current_user = get_jwt_identity()
        user = User.get_user_by_username(current_user)
        if validate_arg(book_id):
            return validate_arg(book_id)
        if user:
            if user.is_admin:
                book = Book.get_book_by_id(book_id)
                if book:
                    data = request.get_json(self)
                    if validate_book(data):
                        return Response(json.dumps(validate_book(data)), status=403)
                    book.title = data['title']
                    book.author = data['author']
                    book.isbn = data['isbn']
                    book.publisher = data['publisher']
                    book.quantity = data['quantity']
                    book.save()
                    book = Book.get_book_by_id(book_id)
                    return Response(json.dumps({"Message": "Book updated successfully", "Book": book.serialize}), status=200)
                return Response(json.dumps({"Message": "Book does not exist"}), status=404)
            return Response(json.dumps({"Message": "User not an admin"}), status=401)
        return Response(json.dumps({"Message": "User does not exist"}), status=404)

    @jwt_required
    def delete(self, book_id):
        """Function serving delete book api endpoint"""
        current_user = get_jwt_identity()
        user = User.get_user_by_username(current_user)
        if validate_arg(book_id):
            return validate_arg(book_id)
        if user:
            if user.is_admin:
                book = Book.get_book_by_id(book_id)
                if book:
                    borrowed = ReviewBook.query.filter_by(
                        book_id=book_id).first()
                    if borrowed:
                        return Response(json.dumps({"Message": "Book has been borrowed"}), status=403)
                    else:
                        book.delete()
                    return Response(json.dumps({"Message": "Book deleted successfully"}), status=200)
                return Response(json.dumps({"Message": "Book doesn't exist"}), status=404)
            return Response(json.dumps({"Message": "User not an admin"}), status=401)
        return Response(json.dumps({"Message": "User does not exist"}), status=404)


class PromoteUser(Resource):
    """Promote user resource"""

    @jwt_required
    def post(self):
        """Function serving promote user api endpoint"""
        current_user = get_jwt_identity()
        user = User.get_user_by_username(current_user)
        if not user:
            return Response(json.dumps({"Message": "User does not exist"}), status=404)
        if user.is_admin:
            data = request.get_json(self)
            User.promote_user(data['username'].lower())
            return Response(json.dumps({"Message": "User promoted successfully"}), status=200)
        return Response(json.dumps({"Message": "User not an admin"}), status=401)
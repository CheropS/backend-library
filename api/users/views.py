from flask_restful import Resource, reqparse
from flask import request, json, Response
from flask_jwt_extended import get_jwt_identity, jwt_required
from datetime import datetime

from api.models import User, Book, ReviewBook
from api.admin.validate import validate_arg, validate_book

parser = reqparse.RequestParser()


class GetAllUsers(Resource):
    """Get all users resource"""

    @jwt_required
    def get(self):
        """Function serving get all user api endpoint"""
        current_user = get_jwt_identity()
        user = User.get_user_by_username(current_user)
        if user:
            if user.is_admin:
                all_users = User.all_users()
                if len(all_users) == 0:
                    return Response(json.dumps({"Message": "No users found"}), status=404)
                return Response(json.dumps({"Users": [user.serialize for user in all_users]}), status=200)
            return Response(json.dumps({"Message": "User not an admin"}), status=401)
        return Response(json.dumps({"Message": "User does not exist"}), status=404)


class GetUser(Resource):
    """Get one user resource"""

    @jwt_required
    def get(self):
        """Function serving get all user api endpoint"""
        current_user = get_jwt_identity()
        user = User.get_user_by_username(current_user)
        if user:
            return Response(json.dumps({"User": user.serialize}), status=200)
        return Response(json.dumps({"Message": "User does not exist"}), status=404)


class ReviewOps(Resource):
    """Review book ops (Review) resource"""

    @jwt_required
    def post(self, book_id):
        """Function serving borrow book api endpoint"""
        current_user = get_jwt_identity()
        user = User.get_user_by_username(current_user)
        if user:
            if validate_arg(book_id):
                return Response(json.dumps(validate_book(book_id)), status=400)
            book = Book.get_book_by_id(book_id)
            if book:
                if book.quantity == 0:
                    return Response(json.dumps({"Message": "Book not available to review"}), status=404)
                borrowed = ReviewBook.query.filter_by(user_id=user.id, book_id=book.id, returned=False).first()
                if borrowed:
                    return Response(json.dumps({"Message": "Already reviewed book"}), status=403)
                ReviewBook(user=user, book=book).save()
                book.quantity -= 1
                book.save()
                return Response(json.dumps({"Message": "Book reviewed successfully", "Book": book.serialize}), status=200)
            return Response(json.dumps({"Message": "Book does not exist"}), status=404)
        return Response(json.dumps({"Message": "User does not not exist"}), status=404)

    @jwt_required
    def put(self, book_id):
        """Function serving return book api endpoint"""
        current_user = get_jwt_identity()
        user = User.get_user_by_username(current_user)
        if user:
            if validate_arg(book_id):
                return Response(json.dumps(validate_book(book_id)), status=403)
            book = Book.get_book_by_id(book_id)
            if book:
                to_return = ReviewBook.query.filter_by(user_id=user.id, book_id=book.id, returned=False).first()
                if to_return:
                    to_return.returned = True
                    to_return.date_returned = datetime.now()
                    to_return.save()
                    book.quantity += 1
                    book.save()
                    return Response(json.dumps({"Message": "Book reviewed successfully"}), status=200)
                return Response(json.dumps({"Message": "You had not reviewed this book"}), status=403)
            return Response(json.dumps({"Message": "Book does not exist"}), status=404)
        return Response(json.dumps({"Message": "User does not exist"}), status=404)

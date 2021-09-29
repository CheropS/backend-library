from flask_restful import Resource, reqparse
from flask import request, json, Response
from flask_jwt_extended import get_jwt_identity, jwt_required
from datetime import datetime

from api.models import User, Book, ReviewBook


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
                allUsers = User.all_users()
                if len(allUsers) == 0:
                    return Response(json.dumps({"Message": "No users found"}), status=404)
                return Response(json.dumps({"Users": [user.serialize for user in allUsers]}), status=200)
            return Response(json.dumps({"Message": "User not an admin"}), status=401)
        return Response(json.dumps({"Message": "User does not exist"}), status=404)

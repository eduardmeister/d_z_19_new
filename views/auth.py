from flask import request
from flask_restx import Namespace, Resource, abort

from implemented import user_service

auth_ns = Namespace("auth")


@auth_ns.route("/")
class AuthView(Resource):
    def post(self):

        req_data = request.json
        username = req_data.get("username")
        password = req_data.get("password")

        if None in [username, password]:
            abort(401, "username or password is None")
        user_data = user_service.get_by_username(username)

        if user_data is None:
            abort(401, "This user not found")

        tokens = user_service.generate_tokens(username, password)

        return tokens, 201

    def put(self):

        req_data = request.json
        token = req_data.get("refresh_token")
        tokens = user_service.approve_refresh_token(token)
        return tokens, 201


import jwt
from flask import request, abort

from config import Config

secret = Config().SECRET_HERE
algo = "HS256"


def auth_required(func):
    def wrapper(*args, **kwargs):
        if "Authorization" not in request.headers:
            abort(401)

        data = request.headers["Authorization"]
        token = data.split("Bearer ")[-1]

        try:
            jwt.decode(token, secret, algorithms=[algo])
        except Exception:
            abort(401, "jwt.decode except")

        return func(*args, **kwargs)
    return wrapper


def admin_required(func):
    def wrapper(*args, **kwargs):
        if "Authorization" not in request.headers:
            abort(401)

        data = request.headers["Authorization"]
        token = data.split("Bearer ")[-1]
        role = None

        try:
            data_user = jwt.decode(token, secret, algorithms=[algo])
            role = data_user.get("role")
        except Exception:
            abort(401)

        if role != "admin":
            abort(403)

        return func(*args, **kwargs)

    return wrapper
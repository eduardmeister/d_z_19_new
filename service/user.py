import base64
import calendar
import datetime
import hashlib
import hmac

import jwt
from flask_restx import abort

from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from dao.user import UserDAO
from config import Config


JWT_SECRET = Config().SECRET_HERE
JWT_ALGORITHM = "HS256"

class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_hash(self, password):
        return base64.b64encode(hashlib.pbkdf2_hmac(
            "sha256",
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS,
        ))

    def generate_tokens(self, username: str, password, is_refresh=False):
        user = self.get_by_username(username)

        if user is None:
            raise abort(404)

        if not is_refresh:
            if not self.compare_passwords(user.password, password):
                abort(400)

        data = {
            "username": user.username,
            "role" : user.role
        }

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=130)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)


        return {"access_token" : access_token, "refresh_token" : refresh_token}

    def approve_refresh_token(self, refresh_token):
        data = jwt.decode(jwt=refresh_token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username = data.get("username")
        return self.generate_tokens(username, password=None, is_refresh=True)

    def compare_passwords(self, user_password, input_password):
        password = self.get_hash(input_password)
        return hmac.compare_digest(user_password, password)

    def get_one(self, id):
        return self.dao.get_one(id)

    def get_by_username(self, username):
        return self.dao.get_by_username(username)


    def get_all(self):
        return self.dao.get_all()

    def create(self, data):
        user_password = data.get("password")
        hash_password = self.get_hash(user_password)
        data["password"] = hash_password
        return self.dao.create(data)

    def update(self, data):
        self.dao.update(data)
        return self.dao

    def delete(self, rid):
        self.dao.delete(rid)

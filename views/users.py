from flask import request
from flask_restx import Resource, Namespace

from dao.model.user import UserSchema
from helpers.decorations import auth_required
from implemented import user_service

user_ns = Namespace('users')


@user_ns.route('/')
class UserView(Resource):
    @auth_required
    def get(self):
        rs = user_service.get_all()
        res = UserSchema(many=True).dump(rs)
        return res, 200

    def post(self):
        req_json = request.json
        user_service.create(req_json)
        return "", 201


@user_ns.route('/<int:rid>')
class UserView(Resource):
    @auth_required
    def get(self, rid):
        r = user_service.get_one(rid)
        data = UserSchema().dump(r)
        return data, 200

    @auth_required
    def put(self, bid):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = bid
        user_service.update(req_json)
        return "", 204

    @auth_required
    def delete(self, bid):
        user_service.delete(bid)
        return "", 204
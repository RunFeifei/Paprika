from celery.utils.serialization import jsonify
from flask_restful import reqparse, Resource

from config.redis import get_online_uids
from model.users import UserModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('page', type=int, required=True)
_user_parser.add_argument('per_page', type=int, required=True)


class Accounts(Resource):
    def get(self):
        params = _user_parser.parse_args()
        page = params['page']
        per_page = params['per_page']
        print('Accounts--get----{}----{}'.format(page, per_page))
        items = UserModel.find_paginate(**params).items
        result = []
        for item in items:
            result.append(item.to_json())
        return jsonify(result), 200


class OnLineUers(Resource):
    def get(self):
        params = _user_parser.parse_args()
        page = params['page']
        per_page = params['per_page']
        print('OnLineUers--get----{}----{}'.format(page, per_page))
        sets = get_online_uids()
        if sets is None:
            return {}, 200
        result = []
        for uid in sets:
            result.append(UserModel.find_by_id(uid).to_json())
        return jsonify(result), 200

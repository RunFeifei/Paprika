from celery.utils.serialization import jsonify
from flask_restful import reqparse, Resource

from model.users import UserModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('page', type=int, required=True)
_user_parser.add_argument('per_page', type=int, required=False)


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

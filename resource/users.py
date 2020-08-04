from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_raw_jwt
from flask_restful import reqparse, Resource
from werkzeug.security import safe_str_cmp

from config.common import BLACKLIST_TOKEN
from model.users import UserModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username', type=str, required=True)
_user_parser.add_argument('password', type=str, required=True)


class UserRegister(Resource):
    def post(self):
        params = _user_parser.parse_args()
        user = UserModel.find_by_username(params['username'])
        if user:
            return {"msg": f"{user.username} already exists"}, 400
        user_model = UserModel(**params)
        try:
            user_model.save()
        except:
            return {"msg": f"{params['username']} save fails"}, 400
        return {"msg": f"{params['username']} save ok"}, 200


class UserLogin(Resource):
    def post(self):
        params = _user_parser.parse_args()
        user = UserModel.find_by_username(params['username'])
        if user and safe_str_cmp(user.password, params['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                       'access_token': access_token,
                       'refresh_token': refresh_token,
                   }, 200
        return {"msg": f"{params['username']} with password {params['password']} login fails"}, 400


class UserLogout(Resource):

    @jwt_required
    def post(self):
        token = get_raw_jwt()['jti']
        BLACKLIST_TOKEN.add(token)
        return {'msg': 'logout ok'}, 200

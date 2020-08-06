from datetime import timedelta

from flask_cors import CORS
from flask_restful import Api, Resource

from config.common import app
from resource import UserLogin, UserLogout, UserRegister, TokenRefresh
from resource.hello import HelloWorldResource

api = Api(app)

app.config['JWT_SECRET_KEY'] = "jhjhjhl3bhb3jjbjjhjhjhjhjjhgsfeifeifiefieifeifeifieifeifei"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=6000)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(seconds=6000)

CORS(app, cors_allowed_origins="*")

api.add_resource(TokenRefresh, '/token_refresh')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(UserRegister, '/register')
api.add_resource(HelloWorldResource, '/hello')


def config_app_api():
    return api

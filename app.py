from flask import Flask, request
from flask_restful import Resource, Api
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from models import db, ma, RevokedTokenModel
from flask_jwt_extended import JWTManager
import os

# app initialization
app = Flask(__name__)

## DB PART
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
db.init_app(app)
ma.init_app(app)
## END OF DB PART

# jwt
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access'] # ['access', 'refresh']
jwt = JWTManager(app)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedTokenModel.is_jti_blacklisted(jti)

# api initialization
api = Api(app, prefix="/api/v1")

import resources

api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.UserLogoutAccess, '/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
# api.add_resource(resources.TokenRefresh, '/token/refresh')
api.add_resource(resources.SecretResource, '/secret')

if __name__ == '__main__':
    app.run(debug=True)


 # with app.app_context():
 #        # Extensions like Flask-SQLAlchemy now know what the "current" app
 #        # is while within this block. Therefore, you can now run........
 #        db.create_all()

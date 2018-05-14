from flask import Flask, request
from flask_restful import Resource, Api
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from models import db, ma
import os

# app initialization
app = Flask(__name__)

## DB PART
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
db.init_app(app)
ma.init_app(app)
## END OF DB PART

# api initialization
api = Api(app, prefix="/api/v1")

import resources

api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.AllUsers, '/users')
#api.add_resource(resources.UserLogin, '/login')
#api.add_resource(resources.UserLogoutAccess, '/logout/access')
#api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
#api.add_resource(resources.TokenRefresh, '/token/refresh')
#api.add_resource(resources.SecretResource, '/secret')

if __name__ == '__main__':
    app.run(debug=True)

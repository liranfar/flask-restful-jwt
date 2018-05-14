from flask import Flask, request
from flask_restful import Resource, Api
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

## DB PART
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120), nullable = False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password # will be changed to hashed pass 

class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('username', 'email')


user_schema = UserSchema()
users_schema = UserSchema(many=True)

## END OF DB PART

#### resources
class UserRegistration(Resource):
    def post(self):
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']

        new_user = User(username, email, password)

        db.session.add(new_user)
        db.session.commit()


        return user_schema.dump(new_user)

class AllUsers(Resource):
    def get(self):
        all_users = User.query.all()
        result = users_schema.dump(all_users)
        return result

    def delete(self):
        return {'message': 'Delete all users'}
#### end of resources

api = Api(app, prefix="/api/v1")

# import resources

api.add_resource(UserRegistration, '/registration')
api.add_resource(AllUsers, '/users')
#api.add_resource(resources.UserLogin, '/login')
#api.add_resource(resources.UserLogoutAccess, '/logout/access')
#api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
#api.add_resource(resources.TokenRefresh, '/token/refresh')
#api.add_resource(resources.SecretResource, '/secret')

if __name__ == '__main__':
    app.run(debug=True)

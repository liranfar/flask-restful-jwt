from flask_restful import Resource
from flask import request
from models import db, User, user_schema, users_schema

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


class UserLogin(Resource):
    def post(self):
        current_user = User.find_by_username(request.json['username'])
        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(request.json['username'])}

        if User.verify_hash(request.json['password'], current_user.password):
            return {'message': 'Logged in as {}'.format(current_user.username)}
        else:
            return {'message': 'Wrong credentials'}


class UserLogoutAccess(Resource):
    def post(self):
        return {'message': 'User logout'}


class UserLogoutRefresh(Resource):
    def post(self):
        return {'message': 'User logout'}


class TokenRefresh(Resource):
    def post(self):
        return {'message': 'Token refresh'}



class SecretResource(Resource):
    def get(self):
        return {
            'answer': 42
        }

from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256 as sha256

db = SQLAlchemy()
ma = Marshmallow()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120), nullable = False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = User.generate_hash(password)

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)
    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()

class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('username', 'email', 'password')


user_schema = UserSchema()
users_schema = UserSchema(many=True)

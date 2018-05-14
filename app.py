from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app, prefix="/api/v1")


class PrivateResource(Resource):
    def get(self):
        return {"meaning_of_life": 42}


api.add_resource(PrivateResource, '/private')

if __name__ == '__main__':
    app.run(debug=True)

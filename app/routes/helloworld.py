# app/routes/helloworld.py

from flask_restx import Namespace, Resource

helloworld_bp = Namespace('helloworld', description='Hello World endpoints')

@helloworld_bp.route('/')
class HelloWorld(Resource):
    def get(self):
        """Returns a simple hello world message"""
        return {
            'status': 'success',
            'message': 'Hello, World!'
        }, 200

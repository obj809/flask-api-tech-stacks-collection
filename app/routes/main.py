# app/routes/main.py

from flask_restx import Namespace, Resource

main_bp = Namespace('main', description='Main API endpoints')

@main_bp.route('/')
class MainResource(Resource):
    def get(self):
        """Health check endpoint"""
        return {
            'status': 'success',
            'message': 'Todo Management API is running',
            'version': '1.0'
        }, 200

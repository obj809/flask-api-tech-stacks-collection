# app/routes/todos.py

from flask import request
from flask_restx import Namespace, Resource, fields
from app import db
from app.models import Todo

todos_bp = Namespace('todos', description='Todo management endpoints')

# Define the Todo model for Swagger documentation
todo_model = todos_bp.model('Todo', {
    'id': fields.Integer(readonly=True, description='Todo unique identifier'),
    'title': fields.String(required=True, description='Todo title')
})

todo_input_model = todos_bp.model('TodoInput', {
    'title': fields.String(required=True, description='Todo title')
})

@todos_bp.route('/')
class TodoList(Resource):
    @todos_bp.doc('list_todos')
    @todos_bp.marshal_list_with(todo_model)
    def get(self):
        """List all todos"""
        todos = Todo.query.all()
        return todos, 200

    @todos_bp.doc('create_todo')
    @todos_bp.expect(todo_input_model)
    @todos_bp.marshal_with(todo_model, code=201)
    def post(self):
        """Create a new todo"""
        data = request.get_json()

        if not data or 'title' not in data:
            todos_bp.abort(400, 'Title is required')

        new_todo = Todo(title=data['title'])
        db.session.add(new_todo)
        db.session.commit()

        return new_todo, 201

@todos_bp.route('/<int:id>')
@todos_bp.param('id', 'The todo identifier')
class TodoResource(Resource):
    @todos_bp.doc('get_todo')
    @todos_bp.marshal_with(todo_model)
    def get(self, id):
        """Get a todo by ID"""
        todo = Todo.query.get(id)
        if not todo:
            todos_bp.abort(404, f'Todo {id} not found')
        return todo, 200

    @todos_bp.doc('update_todo')
    @todos_bp.expect(todo_input_model)
    @todos_bp.marshal_with(todo_model)
    def put(self, id):
        """Update a todo"""
        todo = Todo.query.get(id)
        if not todo:
            todos_bp.abort(404, f'Todo {id} not found')

        data = request.get_json()
        if not data or 'title' not in data:
            todos_bp.abort(400, 'Title is required')

        todo.title = data['title']
        db.session.commit()

        return todo, 200

    @todos_bp.doc('delete_todo')
    @todos_bp.response(204, 'Todo deleted')
    def delete(self, id):
        """Delete a todo"""
        todo = Todo.query.get(id)
        if not todo:
            todos_bp.abort(404, f'Todo {id} not found')

        db.session.delete(todo)
        db.session.commit()

        return '', 204

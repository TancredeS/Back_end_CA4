from flask import Flask

app = Flask(__name__)

from .todo import todo

app.register_blueprint(todo.todo_bp, url_prefix='/todolist')
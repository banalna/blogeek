# -*- coding: utf-8 -*-

from app import create_app, db, cli
from app.models import User, Post, Message, Notification, Task, Room

app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Message': Message,
            'Notification': Notification, 'Task': Task, 'Room':Room}

# app.run(debug=True)

# -*- coding: utf-8 -*-
from flask import session
from flask_login import current_user
from flask_socketio import emit, join_room, leave_room

from app import socketio, db
from app.models import Message, User


@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    if message['msg']:
        room = session.get('room')
        user = User.query.filter_by(username=message['recipient']).first_or_404()

        msg = Message(author=current_user, recipient=user, body=message['msg'])
        user.add_notification('unread_message_count', user.new_messages())
        db.session.add(msg)
        db.session.commit()

        emit('message', {'msg': session.get('name') + ':' + message['msg']}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)
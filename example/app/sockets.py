from flask_socketio import emit, Namespace, leave_room, join_room
from flask import request
from flask_rest import socketio


def decoder(func):
    def wrap(self, data):
        if isinstance(data, dict):
            _data = dict()
            for k, v in data.items():
                _data[k.encode('latin-1').decode('utf-8')] = v.encode('latin-1').decode('utf-8')
            data = _data
        elif isinstance(data, str):
            data = data.encode('latin-1').decode('utf-8')
        func(self, data)
    return wrap


class TestChatSocket(Namespace):

    room = "chat"
    sids = dict()

    history_messages = []

    def __find_user_on_sid(self, sid):
        try:
            return next(filter(lambda args: args[1] == sid, self.sids.items()))[0]
        except (IndexError, StopIteration):
            return None

    def on_connect(self):
        join_room(self.room)

    @decoder
    def on_send_info(self, data):
        username = data["username"]
        self.sids[username] = request.sid
        emit("joined_new_user", dict(username=username), include_self=False, room=self.room)

    def on_disconnect(self):
        username = self.__find_user_on_sid(request.sid)
        if username:
            self.sids.pop(username)
            emit("leave_user", dict(username=username), room=self.room)
        leave_room(self.room)

    @decoder
    def on_error(self, e):
        leave_room(self.room)
        username = self.__find_user_on_sid(request.sid)
        if username:
            self.sids.pop(username)
            emit("leave_user", dict(username=username), room=self.room)

    @decoder
    def on_pers_message(self, data):
        message = data["message"]
        username = data["username"]
        for_user = data.get("for_user")

        if for_user and self.sids.get(for_user):
            emit(
                "pers_message",
                dict(message=message, username=username),
                room=self.sids[for_user],
            )
        else:
            emit(
                "send_pers_message_error",
                dict(message="User is offline"),
                room=request.sid,
            )

    @decoder
    def on_message(self, data):
        message = data["message"]
        username = data["username"]
        emit("message", dict(message=message, username=username), room=self.room)


socketio.on_namespace(TestChatSocket('/test-chat'))

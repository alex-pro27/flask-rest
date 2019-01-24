from flask_rest import socketio, project


if __name__ == '__main__':
    socketio.run(project, host='0.0.0.0', port=8080, debug=True)

import socketio
import eventlet

sio = socketio.Server()
app = socketio.WSGIApp(sio)

@sio.event
def connect(sid, environ):  ## session ID (), dictionary with details of client request 
    print(sid, " connected")
    print(environ)

@sio.event
def disconnect(sid):
    print(sid, " disconnected")


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 3050)), app)
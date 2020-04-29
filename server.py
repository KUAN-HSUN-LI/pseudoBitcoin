import eventlet
import socketio
import os
from utils import load_pkl, deserialize
import pickle

parent_path = "server"

if not os.path.exists(parent_path):
    os.mkdir(parent_path, 0o755)

wallet_path = os.path.join(parent_path, "wallet.pkl")

if not os.path.exists(wallet_path):
    wallets = {}
else:
    print(wallet_path)
    wallets = load_pkl(wallet_path)

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})


@sio.event
def connect(sid, environ):
    print('connect ', sid)


@sio.event
def my_message(sid, data):
    print('message ', data)


@sio.event
def disconnect(sid):
    print('disconnect ', sid)


@sio.event
def update_wallet(sid, address, wallet):
    wallets[address] = deserialize(wallet)
    with open(wallet_path, "wb") as f:
        pickle.dump(wallets, f)
    sio.emit("msg", "get wallet")


@sio.event
def get_wallet(sid, wallet):
    sio.emit("get_wallet", pickle.dumps(wallets))


eventlet.wsgi.server(eventlet.listen(('', 5000)), app)

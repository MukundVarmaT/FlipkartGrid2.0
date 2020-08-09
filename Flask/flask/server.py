import os
import torch
import jwt
import datetime
import secrets
import string

from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit, disconnect

from test import ready, infer

app = Flask(__name__, static_folder="../build", static_url_path="/")
socketio = SocketIO(app, cors_allowed_origins='*')
jwt_secret = 'secret'
alg = ['HS256']
N = 12

model = ready()
model.eval()

print('Model loaded')

loginCreds = {
    'Mukesh-V' : 'ComradesWon',
    'Mukund-Varma-T' : 'ComradesWin',
    'Vikas-Mahendar-K' : 'ComradesWillWin'
}

@app.route('/token', methods=['POST'])
def token():
    name = request.form['username']
    password = request.form['password']

    if name in loginCreds:
        if str(loginCreds[name]) == password:
            try:
                payload = {
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=0),
                    'iat': datetime.datetime.utcnow(),
                    'sub': name         
                }
                enc = jwt.encode(
                    payload,
                    jwt_secret,
                    algorithm=alg[0]
                )
                return enc
            except:
                return '500 : JWT couldnt be generated'
        else:
            return '405 : Password Mismatch'
    else:
        return '404 : User not found'



@app.route('/', defaults={'path': ''})
@app.route('/<path>')
def handler(path):
    return app.send_static_file('index.html')

@socketio.on('send')
def handle_input(json):

    try:
        token = json['token']
    except:
        return emit('receive', '400 : Token Absent')
    
    if token is not None:
        try:
            token = bytes(token, 'utf-8')
            payload = jwt.decode(token, jwt_secret,algorithms=alg)
            idx = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(N))

            w = open(idx +'.wav', 'wb')
            w.write(json['blob'])
            w.close()

            infer(model, idx+'.wav')

            r = open('output/'+ idx +'_clean.wav', 'rb')
            data = r.read()
            r.close()

            emit('receive', data)

            os.remove(idx+'.wav')
            os.remove('output/' + idx + '_clean.wav')
            os.remove('output/'+ idx + '_noise.wav')

        except jwt.ExpiredSignatureError:
            return emit('receive','401 : Signature expired. Please log in again.')
        except jwt.InvalidTokenError:
            emit('receive','402 : Invalid token. Please log in again.')
            disconnect()

if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'COMRADES!'
    CORS(app)
    socketio.run(app)

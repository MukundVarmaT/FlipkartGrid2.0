import os
import torch
import jwt
import datetime
import secrets
import string
import warnings
import argparse
import logging
import yaml
import mysql.connector as adapter

from flask           import Flask, request
from flask_cors      import CORS
from flask_socketio  import SocketIO, emit, disconnect

from infer import ready, infer

parser = argparse.ArgumentParser()
parser.add_argument("--prod",action='store_true',help="Production configs are applied")
args = vars(parser.parse_args())

if args['prod']:
    config_file = 'prod.yaml'
    warnings.filterwarnings('ignore')
    print('Running in Production')
else:
    config_file = 'dev.yaml'
    print('Running in Dev')

with open(config_file) as f:
    config = yaml.load(f)

if not os.path.exists('./input'):
    os.mkdir('input')
if not os.path.exists('./output'):
    os.mkdir('output')

app = Flask(__name__, static_folder="./build", static_url_path="/")
socketio = SocketIO(app, cors_allowed_origins='*', logger=True)

jwt_secret = config['jwt_secret']
N          = config['index_seed']
alg        = 'HS256'

table    = config['table']
column   = config['column']
db = adapter.connect(
    host     = config['host'],
    user     = config['username'],
    password = config['password'],
    database = config['database']
)

model_name = 'model/' + config['model']
model = ready(model_name)
model.eval()

print('Model loaded')

@app.route('/token', methods=['POST'])
def token():
    name     = request.form['username']
    password = request.form['password']

    cursor = db.cursor()
    query  = "SELECT * FROM " + table + " WHERE " + column + " = \"" + name +"\""
    cursor.execute(query)
    credential = cursor.fetchone()
    cursor.close()

    if credential:
        if str(credential[1]) == password:
            try:
                payload = {
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=0),
                    'iat': datetime.datetime.utcnow(),
                    'sub': name         
                }
                enc = jwt.encode(
                    payload,
                    jwt_secret,
                    algorithm=alg
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
            token   = bytes(token, 'utf-8')
            payload = jwt.decode(token, jwt_secret,algorithms=alg)
            idx     = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(N))

            inp       = 'input/'  + idx + '_noisy.wav'
            op_clean  = 'output/' + idx + '_clean.wav'
            op_noise  = 'output/' + idx + '_noise.wav'
            file_list = [inp, op_clean, op_noise]

            w = open(inp, 'wb')
            w.write(json['blob'])
            w.close()

            infer(model, file_list)

            r = open(op_clean, 'rb')
            data = r.read()
            r.close()

            emit('receive', data)

            if args['prod']:
                os.remove(inp)
                os.remove(op_clean)
                os.remove(op_noise)

        except jwt.ExpiredSignatureError:
            return emit('receive','401 : Signature expired. Please log in again.')
        except jwt.InvalidTokenError:
            emit('receive','402 : Invalid token. Please log in again.')
            disconnect()

if __name__ == '__main__':
    app.config['SECRET_KEY'] = config['socket_secret']
    CORS(app)
    socketio.run(app)

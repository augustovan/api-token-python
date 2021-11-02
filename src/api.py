from flask import Flask, jsonify, request, make_response
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'estaporradekey'

def token_required(f):
        @wraps(f)
        def decoreted(*args, **kwargs):
                token = request.args.get('token') # Localhost:5000/route?token

                if not token:
                        return jsonify({'message':'Essa faltando essa porra'}), 403
                
                try:
                        data = jwt.decode(token, app.config['SECRET_KEY'])
                except:
                        return jsonify({'message':'Essa poha eh invalida'}), 403

                return f(*args, **kwargs)  
        return decoreted   

@app.route('/semprotecao')
def semprotecao():
        return jsonify({'message':'Ta td aberto aqui'})

@app.route('/protegido')
@token_required
def protegido():
        return jsonify({'message':'Aqui nao é bagunca so com token'})

@app.route('/login')
def login():
        auth = request.authorization

        if auth and auth.password == 'password':
                token = jwt.encode({'user' : auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

                return jsonify({'token' :  token.decode('UTF-8')})

        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic  realm="Login Required"'})

if __name__ == '__main__':
        app.run(
                debug=True
        
        )
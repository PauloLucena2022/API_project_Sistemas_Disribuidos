from flask import Flask, request, jsonify
from keras.models import load_model
import joblib 
import jwt
import datetime 
from functools import wraps

# Configurações
SECRET_KEY = 'chave_super_segura_paulo_paula_murilo_williane'

app = Flask(__name__)
model = load_model('dataset/modelos_api/modelo_obesidade_final.h5')
scaler = joblib.load('dataset/modelos_api/scaler_obesidade.pkl')

# Decorador - verifica token JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'mensagem': 'Token ausente'}), 401
        try:
            token = token.replace("Bearer ", "")
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'mensagem': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'mensagem': 'Token inválido'}), 401
        return f(*args, **kwargs)
    return decorated

# Endpoint de login (geração do token)
@app.route('/login', methods=['POST'])
def login():
    auth = request.json 
    usuario = auth.get('usuario')
    senha = auth.get('senha')

    # Exemplo, mas vai ter que substituir depois pelo banco de dados mesmo
    if usuario == 'admin' and senha == '12345':
        token = jwt.encode({
            'usuario': usuario,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, SECRET_KEY, algorithm="HS256")
        return jsonify({'token': token})
    return jsonify({'mensagem': 'Credenciais inválidas'}), 401

# Agora sim essa rota tá filé de proteção
@app.route('/predict', methods = ['POST']) # vai receber uma lista com 16 números (hiperparâmetros)
@token_required
def predict():
    dados = request.json['entrada']
    entrada = scaler.transform([dados])
    pred = model.predict(entrada).argmax(axis = 1)[0]
    return jsonify({'label': int(pred)})

if __name__ == '__main__':
    app.run(debug = True)

'''
Para login:

Método: POST

URL: http://localhost:5000/login

Body (JSON):

* Resultado: um token jws

Para predição:

URL: http://localhost:5000/predict

Header - Authorization: Bearer <token>

{
"entrada": [0,21,1.62,64.00,1,0,2,3.00,2,0,2.00,0,0,1.00,3,3]
}

* resultado: 

{
	"label": 1
}

'''

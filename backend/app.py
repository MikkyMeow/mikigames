from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_cors import CORS
import bcrypt

app = Flask(__name__)
CORS(app)  # Разрешить CORS

# Настройки JWT
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Измените на свой ключ
jwt = JWTManager(app)

# Простое хранилище пользователей
users = {}

@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    if username in users:
        return jsonify({"msg": "User already exists"}), 400

    # Хэширование пароля
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users[username] = hashed_password

    return jsonify({"msg": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    user = users.get(username)

    if not user or not bcrypt.checkpw(password.encode('utf-8'), user):
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return jsonify(msg="This is a protected route"), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

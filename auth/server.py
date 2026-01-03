import os
import jwt
import datetime
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

server = Flask(__name__)

server.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'mysql')
server.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'auth_user')
server.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'auth123')
server.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'auth')
server.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT', 3306))

SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret')  # NEVER hardcode in prod

mysql = MySQL(server)


@server.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    if not auth:
        return jsonify({"error": "missing credentials"}), 401

    cursor = mysql.connection.cursor()
    res = cursor.execute(
        "SELECT email, password FROM users WHERE email=%s",
        (auth.username,)
    )

    if res == 0:
        return jsonify({"error": "invalid credentials"}), 401

    email, password = cursor.fetchone()

    if auth.username != email or auth.password != password:
        return jsonify({"error": "invalid credentials"}), 401

    token = create_jwt(auth.username, SECRET_KEY, True)
    return jsonify({"token": token})


@server.route('/validate', methods=['POST'])
def validate():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"error": "missing token"}), 401

    try:
        token = auth_header.split(" ")[1]
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return jsonify(decoded), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "invalid token"}), 401


def create_jwt(username, secret_key, admin):
    return jwt.encode(
        {
            "username": username,
            "admin": admin,
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
        },
        secret_key,
        algorithm="HS256",
    )

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)

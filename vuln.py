import os
import sqlite3
import pickle
import flask
from flask import request

app = flask.Flask(__name__)

# Hardcoded credentials
USERNAME = "admin"
PASSWORD = "secret123"

# Unsafe: Command injection
@app.route('/ping')
def ping():
    host = request.args.get("host")
    os.system(f"ping -c 1 {host}")
    return f"Pinging {host}..."

# Unsafe: SQL Injection
@app.route('/user')
def get_user():
    user_id = request.args.get("id")
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE id = '{user_id}'"
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return str(result)

# Unsafe: eval() usage
@app.route('/calc')
def calc():
    expr = request.args.get("expr")
    return str(eval(expr))  # dangerous

# Unsafe: Deserialization
@app.route('/load')
def load_object():
    data = request.args.get("data")
    obj = pickle.loads(bytes.fromhex(data))
    return f"Loaded object: {obj}"

# Insecure login simulation
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if username == USERNAME and password == PASSWORD:
        return "Logged in"
    return "Access Denied"

if __name__ == '__main__':
    app.run(debug=True)

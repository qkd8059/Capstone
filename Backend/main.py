from flask import Flask, request, jsonify, Response, abort, redirect

import hashlib
import base64
import secrets
import datetime
import os

from database import DB

# TODO change to domain url once we can
URL = 'http://' + os.environ['MY_IP']

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return 'This is the backend'

@app.route('/sign-up', methods=['POST'])
def sign_up():
    if not valid_request(request, ['first_name', 'last_name', 'email', 'password']):
        return abort(400)
    
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']

    salt = secrets.token_bytes(16)
    master_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

    DB.create_user(
        first_name,
        last_name,
        email,
        base64.b64encode(salt).decode('utf-8'),
        base64.b64encode(master_key).decode('utf-8')
    )

    return redirect(f'{URL}/sign-in/sign-in.html', 303)

@app.route('/sign-in', methods=['POST'])
def sign_in():
    if not valid_request(request, ['email', 'password']):
        return abort(400)

    email = request.form['email']
    password = request.form['password']
    remember = 'remember' in request.form.keys()

    user = DB.get_user(email)

    if user is not None:
        salt = base64.b64decode(user['salt'].encode('utf-8'))
        master_key = base64.b64decode(user['master_key'].encode('utf-8'))

        if master_key == hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000):
            max_age, expiration = None, None
            last_used = datetime.datetime.now()
            if remember:
                max_age = datetime.timedelta(days=365)
                expiration = last_used + max_age

            success = False
            while not success:
                session_id = secrets.token_hex(64)
                success = DB.create_session(email, session_id, expiration, last_used)

            resp = redirect(f'{URL}/dashboard/dashboard.html', 303)
            resp.set_cookie('session_id', session_id, max_age=max_age)
            return resp
    
    return redirect(f'{URL}/sign-in/sign-in-failed.html', 303)

def valid_request(req, expected_fields):
    return set(expected_fields) == set(req.form.keys())

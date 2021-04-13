#!/usr/bin/env python3
""" Module of Index views
"""


import os
from flask import jsonify
from flask.globals import request
from api.v1.views import app_views
from models.user import User

@app_views.route('/api/v1/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    email = request.form.get('email')
    if email is None or email == "":
        return jsonify({{"error": "email missing"}}), 400
    password = request.form.get('password')
    if password is None or password == "":
        return jsonify({{"error": "password missing"}}), 400
    user = User.search(attributes={"email": email})
    if user is None:
        return jsonify({ "error": "no user found for this email" }), 404
    if not user.is_valid_password(password):
        return jsonify({ "error": "wrong password" }), 401
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    res = jsonify(user.to_json())
    res.set_cookie(os.getenv('SESSION_NAME'), session_id)
    return res
    
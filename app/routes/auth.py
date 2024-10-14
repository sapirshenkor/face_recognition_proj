
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models.user import User
from app import bcrypt

bp=Blueprint('auth',__name__)



@bp.route('/register',methods=['POST'])
def register():
    username=request.json.get('username',None)
    password=request.json.get('password',None)

    if not username or not password:
        return jsonify({"msg": "Missing username or password"}),400

    if User.find_by_username(username):
        return jsonify({"msg":"Username already exists"}),400

    User.create(username,password)
    return jsonify({"msg": "User created successfully"}),201

@bp.route("/login", methods=['POST'])
def login():
    username=request.json.get('username',None)
    password=request.json.get('password',None)

    user=User.find_by_username(username)
    if user and bcrypt.check_password_hash(user['password'],password):
        access_token=create_access_token(identity=username)
        return jsonify(access_token=access_token),200

    return jsonify({"msg": "Bad username or password"}),401

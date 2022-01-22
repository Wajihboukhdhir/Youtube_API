from os import access
from flask import Blueprint,request,jsonify
from flask_jwt_extended.utils import get_jwt_identity
from werkzeug.security import check_password_hash,generate_password_hash
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT
import validators
from flask_jwt_extended import jwt_required,create_access_token,create_refresh_token
from src.database import User,db
from flasgger import Swagger,swag_from

auth = Blueprint("auth",__name__,url_prefix="/api/v1/auth")

@auth.post('/register')
@swag_from('./docs/auth/register.yml')

def register():
    username=request.json['username']
    password=request.json['password']
    email=request.json['email']

    if not validators.email(email):
        return jsonify({'error':" email is not valid"}),HTTP_400_BAD_REQUEST

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'error':" email is taken"}),HTTP_409_CONFLICT
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'error':" username is taken"}),HTTP_409_CONFLICT

    if len(username)<6:

        return jsonify({'error':" username is too short"}),HTTP_400_BAD_REQUEST
    
    if not username.isalnum() or " " in username:

        return jsonify({'error':" username should be alphanumeric and without spaces"}),HTTP_400_BAD_REQUEST

    if len(password)<6:

        return jsonify({'error':"password is too short"}),HTTP_400_BAD_REQUEST

    pwd_hash=generate_password_hash(password)

    user=User(username=username,password=pwd_hash,email=email)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message':"User created","user":{'username':username,"email":email}}),HTTP_201_CREATED


@auth.post('/login')
@swag_from('./docs/auth/login.yml')

def login():
    email = request.json.get('email','')
    password = request.json.get('password','')
    
    user=User.query.filter_by(email=email).first()

    if user:
        is_pass_correct=check_password_hash(user.password,password)
        if is_pass_correct:
            refresh=create_refresh_token(identity=user.id)
            acces = create_access_token(identity=user.id)

            return jsonify({

                'user':{
                    'refresh':refresh,
                    'access':acces,
                    'username':user.username,
                    'email': user.email

                }
            }),HTTP_200_OK
    return jsonify({'ERROR!!':"wrong credentials"}),HTTP_401_UNAUTHORIZED


@auth.get("/me")
@swag_from('./src/docs/auth/myinfo.yml')

@jwt_required()
def me():
    user_id = get_jwt_identity()

    user=User.query.filter_by(id=user_id).first()


    return jsonify({
        'username':user.username,
        'email':user.email
    })


@auth.post('/token/refresh')
@swag_from('./src/docs/auth/refreshtoken.yml')

@jwt_required(refresh=True)
def refresh_users_token():
    identity=get_jwt_identity()
    access=create_access_token(identity=identity)

    return jsonify({
        'access':access


    }),HTTP_200_OK
        

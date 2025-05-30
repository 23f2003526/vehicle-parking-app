from datetime import datetime, timedelta, timezone
import uuid
import jwt
from app import app
from flask import jsonify, make_response, redirect, render_template, request, url_for, g
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

from backend.models import Role, User, db
from backend.auth import token_required

api = Api(app)

user_fields = {
    'public_id': fields.String,
    'name': fields.String,
    'email': fields.String,
    'role_id': fields.Integer
    # 'password': fields.String,
}

signup_parser = reqparse.RequestParser()
signup_parser.add_argument("name", type=str, help='Name of the user is required', required=True, location='json')
signup_parser.add_argument("email", type=str, help='Email of the user is required', required=True, location='json')
signup_parser.add_argument("password", type=str, help='Password of the user is required', required=True, location='json')

class Signup(Resource):
    @marshal_with(user_fields)
    def post(self):
        req_args = signup_parser.parse_args()
        name = req_args['name']
        email = req_args['email']
        password = req_args['password']

        user = User.query.filter_by(email=email).first()
        if user:
            abort(403, message="User already exists. Please login.")        
        user_role = Role.query.filter_by(name='user').first()
        if not user_role:
            abort(500, message="User Role not found in database")
        else:
            new_user = User(
                public_id=str(uuid.uuid4()),
                name=name,
                email=email,
                password=generate_password_hash(password),
                role_id=user_role.id  # assign role_id here
            )
            db.session.add(new_user)
            db.session.commit()
            response = {"public_id": new_user.public_id, "name": new_user.name, "email":new_user.email, "role_id":new_user.role_id}
            return response, 200

api.add_resource(Signup, '/signup')

login_parser = reqparse.RequestParser()
login_parser.add_argument('email', type=str, help='This field cannot be empty', required=True, location='json')
login_parser.add_argument('password', type=str, help='This field cannot be empty', required=True, location='json')


class Login(Resource):
    def post(self):
        req_args = login_parser.parse_args()
        email = req_args["email"]
        password = req_args["password"]
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            abort(401, message="Invalid email or password")

        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.now(timezone.utc) + timedelta(hours=1), 'role_id':user.role_id}, app.config['SECRET_KEY'], algorithm="HS256")
        # have to set this token in cookie or smthg

        response = make_response({
            "public_id": user.public_id, 
            # "jwt_token": token, 
            "role_id": user.role_id
            })
        
        response.set_cookie(
            "jwt_token",
            token,
            httponly=True,
            samesite='Lax',
            max_age=3600
        )
        return response
    
api.add_resource(Login, '/login')


class Dashboard(Resource):
    @token_required
    def get(self):
        current_user = g.current_user
        return {
            "public_id": current_user.public_id,
            "name": current_user.name,
            "email": current_user.email,
            "role": current_user.role.name
        }, 200

api.add_resource(Dashboard, '/dashboard')


# @app.route('/')
# def home():
#     return render_template('login.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#         user = User.query.filter_by(email=email).first()

#         if not user or not check_password_hash(user.password, password):
#             return jsonify({'message': 'Invalid email or password'}), 401

#         token = jwt.encode({'public_id': user.public_id, 'exp': datetime.now(timezone.utc) + timedelta(hours=1), 'role_id':user.role_id}, app.config['SECRET_KEY'], algorithm="HS256")

#         response = make_response(redirect(url_for('dashboard')))
#         response.set_cookie('jwt_token', token)

#         return response

#     return render_template('login.html')


# @app.route('/dashboard')
# @token_required
# def dashboard(current_user):
#     return render_template('index.html')
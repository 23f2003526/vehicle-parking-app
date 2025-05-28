from datetime import datetime, timedelta, timezone
import uuid
import jwt
from app import app
from flask import jsonify, make_response, redirect, render_template, request, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from backend.models import Role, User, db
from backend.auth import token_required


@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            return jsonify({'message': 'Invalid email or password'}), 401

        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.now(timezone.utc) + timedelta(hours=1), 'role_id':user.role_id}, app.config['SECRET_KEY'], algorithm="HS256")

        response = make_response(redirect(url_for('dashboard')))
        response.set_cookie('jwt_token', token)

        return response

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'message': 'User already exists. Please login.'}), 400
        
        user_role = Role.query.filter_by(name='user').first()
        if not user_role:
            return jsonify({'message': 'User role not found in database'}), 500

        hashed_password = generate_password_hash(password)
        new_user = User(
            public_id=str(uuid.uuid4()),
            name=name,
            email=email,
            password=hashed_password,
            role_id=user_role.id  # assign role_id here
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/dashboard')
@token_required
def dashboard(current_user):
    return f"Welcome {current_user.name}! You are logged in."
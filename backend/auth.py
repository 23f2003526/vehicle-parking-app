from functools import wraps
from flask import jsonify, request, current_app, g
import jwt

from backend.models import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('jwt_token')

        if not token:
            return {'message': 'Token is missing! Please login again.'}, 401

        try:
            secret_key = current_app.config['SECRET_KEY']
            data = jwt.decode(token, secret_key, algorithms=["HS256"])

            current_user = User.query.filter_by(public_id=data['public_id'], role_id=data['role_id']).first()
            
            if not current_user:
                return {'message':'Token is invalid'}, 404
            
            g.current_user = current_user
        except Exception as e:
            print(f"Token error: {e}")
            return {'message': 'Token is invalid!'}, 401

        return f(*args, **kwargs)

    return decorated


def admin_required(f):
    @token_required
    @wraps(f)
    def decorated(*args, **kwargs):
        current_user = g.current_user

        if not current_user.role.name == 'admin':
            return {'message': 'Admin access required'}, 403
        return f(*args, **kwargs)

    return decorated

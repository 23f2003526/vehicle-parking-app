from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
# from flask_sqlalchemy import SQLAlchemy
# import jwt
# import uuid
from datetime import datetime, timezone, timedelta
from werkzeug.security import generate_password_hash

from backend.config import LocalDevelopmentConfig
from backend.models import Role, db, User

def createApp():
    app = Flask(__name__, template_folder='frontend')
    app.config.from_object(LocalDevelopmentConfig)
    CORS(app, supports_credentials=True)

    # api = Api(app)

    db.init_app(app)
    migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()

        # Check if roles already exist
        if not Role.query.filter_by(name='admin').first():
            admin_role = Role(name='admin')
            db.session.add(admin_role)
        else:
            admin_role = Role.query.filter_by(name='admin').first()

        if not Role.query.filter_by(name='user').first():
            user_role = Role(name='user')
            db.session.add(user_role)

        # Check if admin user exists
        if not User.query.filter_by(email='admin@gmail.com').first():
            admin_user = User(
                public_id='admin-public-id',
                name='Admin',
                email='admin@gmail.com',
                password=generate_password_hash('admin'),
                role=admin_role  # for many-to-one relationship
            )
            db.session.add(admin_user)

        db.session.commit()

    return app

app = createApp()

from backend.api import *

if __name__ == '__main__':
    app.run()
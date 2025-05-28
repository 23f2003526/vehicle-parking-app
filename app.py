from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import jwt
import uuid
from datetime import datetime, timezone, timedelta

from backend.config import LocalDevelopmentConfig
from backend.models import db, User

def createApp():
    app = Flask(__name__, template_folder='frontend')
    app.config.from_object(LocalDevelopmentConfig)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app

app = createApp()

# Configuration


# Database setup




# Token required decorator


from backend.routes import *

if __name__ == '__main__':
    app.run()
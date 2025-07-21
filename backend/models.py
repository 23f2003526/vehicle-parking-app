from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)  # e.g., 'admin', 'user'

    users = db.relationship('User', back_populates='role')


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(70), unique=True)
    password = db.Column(db.String(80))

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.relationship('Role', back_populates='users')

    vehicles = db.relationship('Vehicle', backref='owner', lazy=True)

class Vehicle(db.Model):
    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True)
    license_plate = db.Column(db.String(20), unique=True, nullable=False)
    vehicle_type = db.Column(db.String(20), nullable=False)  # e.g., 'car', 'bike', 'truck'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    reservations = db.relationship('Booking', backref='vehicle', lazy=True)

class ParkingLot(db.Model):
    __tablename__ = 'parking_lots'

    id = db.Column(db.Integer, primary_key=True)
    prime_location_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)  # per hour, or per day
    pin_code = db.Column(db.String(10), nullable=False)
    number_of_spots = db.Column(db.Integer, nullable=False)

    spots = db.relationship('ParkingSpot', backref='lot', lazy=True, cascade='all, delete-orphan')


class ParkingSpot(db.Model):
    __tablename__ = 'parking_spots'

    id = db.Column(db.Integer, primary_key=True)
    spot_number = db.Column(db.String(20), nullable=False)
    spot_type = db.Column(db.String(20), nullable=True)  # e.g., 'compact', 'large', 'EV'
    is_occupied = db.Column(db.Boolean, default=False)

    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lots.id'), nullable=False)

    reservations = db.relationship('Booking', back_populates='spot', lazy=True)

class Booking(db.Model):
    __tablename__ = 'booking'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=True)

    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spots.id', ondelete='SET NULL'), nullable=True)

    spot = db.relationship('ParkingSpot', back_populates='reservations')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

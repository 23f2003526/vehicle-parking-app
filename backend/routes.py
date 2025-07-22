from datetime import datetime, timedelta, timezone
from math import ceil
import uuid
import jwt
from app import app
from flask import jsonify, make_response, redirect, render_template, request, url_for, g
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

from backend.models import Booking, Role, User, Vehicle, db, ParkingSpot, ParkingLot
from backend.auth import token_required, admin_required
from backend.parsers import signup_parser, login_parser, lot_parser, spot_update_parser, vehicle_parser

# api = Api(app)

user_fields = {
    'public_id': fields.String,
    'name': fields.String,
    'email': fields.String,
    'role_id': fields.Integer
    # 'password': fields.String,
}


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

# api.add_resource(Signup, '/signup')


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
    
# api.add_resource(Login, '/login')

# class Logout(Resource):
#     def get(self):
#         return {}

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

# api.add_resource(Dashboard, '/dashboard')

class LotGetCreate(Resource):
    @admin_required
    def get(self):
        lots = ParkingLot.query.all()

        lot_list = []
        for lot in lots:
            total_spots = len(lot.spots)
            occupied_spots = ParkingSpot.query.filter_by(lot_id=lot.id, is_occupied=True).count()
            available_spots = total_spots - occupied_spots

            lot_list.append({
                'id': lot.id,
                'prime_location_name': lot.prime_location_name,
                'address': lot.address,
                'pin_code': lot.pin_code,
                'price': lot.price,
                'number_of_spots': total_spots,
                'occupied_spots': occupied_spots,
                'available_spots': available_spots
            })

        return lot_list, 200

    @admin_required
    def post(self):
        args = lot_parser.parse_args()

        if args['number_of_spots'] <= 0:
            abort(400, message="Number of spots must be greater than 0")

        existing_lot = ParkingLot.query.filter_by(address=args['address']).first()
        if existing_lot:
            abort(400, message="A parking lot already exists at this address.")

        new_lot = ParkingLot(
            prime_location_name = args['prime_location_name'],
            address = args['address'],
            price = args['price'],
            pin_code = args['pin_code'],
            number_of_spots = args['number_of_spots'],
            )
        db.session.add(new_lot)
        db.session.commit()

        for i in range(1, args['number_of_spots'] + 1):
            spot = ParkingSpot(
                lot_id = new_lot.id,
                is_occupied = False,
                spot_number = i,
                spot_type = "compact"
            )
            db.session.add(spot)
        db.session.commit()

        return {'message': 'Parking lot created successfully', 'lot_id': new_lot.id}, 201

# api.add_resource(LotGetCreate, '/admin/lots')  

class LotUpdateDelete(Resource):
    @admin_required
    def get(self, lot_id):
        lot = ParkingLot.query.get_or_404(lot_id)
        return {
            'id': lot.id,
            'prime_location_name': lot.prime_location_name,
            'address': lot.address,
            'pin_code': lot.pin_code,
            'price': lot.price,
            'number_of_spots': lot.number_of_spots
        }, 200

    @admin_required
    def put(self, lot_id):
        args = lot_parser.parse_args()
        lot = ParkingLot.query.get_or_404(lot_id)

        if args['prime_location_name']: lot.prime_location_name = args['prime_location_name']
        if args['address']: lot.address = args['address']
        if args['pin_code']: lot.pin_code = args['pin_code']
        if args['price']: lot.price = args['price']

        # do the following only when all parking spots in the current parking lot are empty
        occupied_spots = ParkingSpot.query.filter_by(lot_id=lot.id, is_occupied=True).count()
        if occupied_spots > 0:
            abort(400, message="Cannot update lot with occupied spots")

        if args['number_of_spots'] and args['number_of_spots'] != lot.number_of_spots:            
            lot.number_of_spots = args['number_of_spots']
            
            # how to optimize this ?
            spots = ParkingSpot.query.filter_by(lot_id=lot.id).all()
            for spot in spots:
                db.session.delete(spot)
            
            for i in range(1, args['number_of_spots'] + 1):
                spot = ParkingSpot(
                    lot_id = lot.id,
                    is_occupied = False,
                    spot_number = i,
                    spot_type = "compact"
                )
                db.session.add(spot)

        db.session.commit()
        return {'message': f'Parking lot {lot.prime_location_name} updated successfully with {lot.number_of_spots} number of spots'}, 200

    @admin_required
    def delete(self, lot_id):
        lot = ParkingLot.query.get(lot_id)
        if not lot:
            abort(404, message="Parking lot not found")

        # Ensure all spots are unoccupied
        occupied_spots = ParkingSpot.query.filter_by(lot_id=lot.id, is_occupied=True).count()
        if occupied_spots > 0:
            abort(400, message="Cannot delete lot with occupied spots")
        db.session.delete(lot)
        db.session.commit()
        return {'message': 'Parking lot deleted successfully'}, 200
    
# api.add_resource(LotUpdateDelete, '/admin/lots/<int:lot_id>')

class LotSummary(Resource):
    @token_required
    def get(self, lot_id):
        lot = ParkingLot.query.get_or_404(lot_id)

        total_spots = len(lot.spots)
        occupied_spots = ParkingSpot.query.filter_by(lot_id=lot_id, is_occupied=True).count()
        available_spots = total_spots - occupied_spots

        spots = ParkingSpot.query.filter_by(lot_id=lot_id).all()

        return{
            "lot_id": lot.id,
            "prime_location_name": lot.prime_location_name,
            "address": lot.address,
            "pin_code": lot.pin_code,
            "price": lot.price,
            "number_of_spots": total_spots,
            "occupied_spots": occupied_spots,
            "available_spots": available_spots,
            "spots": [
                {
                    'spot_id': spot.id,
                    'spot_number': spot.spot_number,
                    'spot_type': spot.spot_type,
                    'is_occupied': spot.is_occupied
                } for spot in spots
            ]
        }, 200
    
# api.add_resource(LotSummary, '/admin/lots/<int:lot_id>/summary')

class SpotResource(Resource):
    @admin_required
    def get(self, lot_id, spot_number):
        spot = ParkingSpot.query.filter_by(lot_id=lot_id, spot_number=spot_number).first()
        if not spot:
            abort(404, message="Parking spot not found")
        return {
            "id": spot.id,
            "spot_number": spot.spot_number,
            "spot_type": spot.spot_type,
            "is_occupied": spot.is_occupied
        }, 200
    
    @admin_required
    def delete(self, lot_id, spot_number):
        spot = ParkingSpot.query.filter_by(lot_id=lot_id, spot_number=spot_number).first()
        if not spot:
            abort(404, message="Parking spot not found")

        if spot.is_occupied:
            abort(400, message="Cannot delete an occupied spot")
        
        db.session.delete(spot)
        db.session.commit()
        return {'message': 'Spot deleted successfully'}, 200
    
    @admin_required
    def put(self, lot_id, spot_number):
        spot = ParkingSpot.query.filter_by(lot_id=lot_id, spot_number=spot_number).first()
        if not spot:
            abort(404, message="Parking spot not found")

        args = spot_update_parser.parse_args()
        if args["spot_type"]:
            spot.spot_type = args["spot_type"]
        if args["is_occupied"] is not None:
            spot.is_occupied = args["is_occupied"]

        db.session.commit()
        return {"message": "Spot updated successfully"}, 200
    

class ActiveBookingResource(Resource):
    @admin_required
    def get(self, lot_id, spot_number):
        spot = ParkingSpot.query.filter_by(lot_id=lot_id, spot_number=spot_number).first()
        if not spot:
            abort(404, message="Parking spot not found")

        if not spot.is_occupied:
            abort(400, message="Spot is not currently occupied")

        active_booking = Booking.query.filter_by(spot_id=spot.id, end_time=None).first()
        if not active_booking:
            abort(404, message="No active booking found for this spot")

        vehicle = active_booking.vehicle
        if not vehicle:
            abort(404, message="Vehicle associated with this booking not found")

        IST = timezone(timedelta(hours=5, minutes=30))
        now = datetime.now(IST)

        start_time = active_booking.start_time
        if start_time.tzinfo is None:
            start_time = start_time.replace(tzinfo=IST)

        duration_hours = max(1, ceil((now - start_time).total_seconds() / 3600))
        estimated_cost = duration_hours * spot.lot.price

        return {
            "spot_id": spot.id,
            "customer_id": vehicle.user_id,
            "vehicle_number": vehicle.license_plate,
            "start_time": active_booking.start_time.isoformat(),
            "estimated_cost": estimated_cost
        }, 200


    
# api.add_resource(SpotResource, '/admin/lots/<int:lot_id>/spots/<int:spot_number>')

# WHAT's LEFT :: Admin should be able to see list of all users and their details. (username, spot used, reservation history etc.)

class VehicleResource(Resource):
    @token_required
    def get(self):
        current_user = g.current_user
        vehicles = Vehicle.query.filter_by(user_id=current_user.id).all()

        return [{
            'id': v.id,
            'license_plate': v.license_plate,
            'vehicle_type': v.vehicle_type
        } for v in vehicles], 200

    @token_required
    def post(self):
        current_user = g.current_user
        # data = VehicleResource.vehicle_parser.parse_args()
        req_args = vehicle_parser.parse_args()
        license_plate = req_args["license_plate"]
        vehicle_type = req_args["vehicle_type"]

        if Vehicle.query.filter_by(license_plate=license_plate).first():
            abort(400, message="A vehicle with this license plate already exists.")

        vehicle = Vehicle(
            license_plate=license_plate,
            vehicle_type=vehicle_type,
            user_id=current_user.id
        )

        db.session.add(vehicle)
        db.session.commit()

        return {"message": "Vehicle registered successfully.", "vehicle_id": vehicle.id}, 201

    @token_required
    def put(self):
        current_user = g.current_user
        data = vehicle_parser.copy()
        data.add_argument('vehicle_id', type=int, required=True, help="Vehicle ID is required to update.")
        args = data.parse_args()

        vehicle = Vehicle.query.filter_by(id=args['vehicle_id'], user_id=current_user.id).first()
        if not vehicle:
            abort(404, message="Vehicle not found or not owned by user.")

        vehicle.license_plate = args['license_plate']
        vehicle.vehicle_type = args['vehicle_type']
        db.session.commit()

        return {"message": "Vehicle updated successfully."}, 200

    @token_required
    def delete(self):
        current_user = g.current_user

        parser = reqparse.RequestParser()
        parser.add_argument('vehicle_id', type=int, required=True, help="Vehicle ID is required to delete.")
        args = parser.parse_args()

        vehicle = Vehicle.query.filter_by(id=args['vehicle_id'], user_id=current_user.id).first()
        if not vehicle:
            abort(404, message="Vehicle not found or not owned by user.")

        db.session.delete(vehicle)
        db.session.commit()

        return {"message": "Vehicle deleted successfully."}, 200 

class BookingResource(Resource):
    @token_required
    def get(self):
        current_user = g.current_user
        user_vehicle_ids = [v.id for v in current_user.vehicles]

        bookings = Booking.query.filter(Booking.vehicle_id.in_(user_vehicle_ids)).all()

        result = []
        for b in bookings:
            spot = b.spot
            lot = spot.lot if spot else None

            result.append({
                "id": b.id,
                "start_time": b.start_time.isoformat(),
                "end_time": b.end_time.isoformat() if b.end_time else None,
                "vehicle_id": b.vehicle_id,
                "vehicle_number": b.vehicle.license_plate,
                "spot_id": b.spot_id,
                "created_at": b.created_at.isoformat(),
                "spot_number": spot.spot_number if spot else "Deleted Spot",
                "spot_type": spot.spot_type if spot else "N/A",
                "lot_id": lot.id if lot else None,
                "location_name": lot.prime_location_name if lot else "Unknown",
                "address": lot.address if lot else "Unknown Address",
                "pin_code": lot.pin_code if lot else "Unknown",
                "status": "active" if not b.end_time else "completed",
                "price": lot.price if lot else 0
            })

        return result, 200

    @token_required
    def post(self):
        current_user = g.current_user
        parser = reqparse.RequestParser()
        parser.add_argument('vehicle_id', type=int, required=True)
        parser.add_argument('spot_id', type=int, required=True)
        args = parser.parse_args()

        start_time = datetime.now(timezone(timedelta(hours=5, minutes=30)))

        vehicle = Vehicle.query.filter_by(id=args['vehicle_id'], user_id=current_user.id).first()
        if not vehicle:
            abort(403, message="Vehicle not found or not owned by user.")

        spot = ParkingSpot.query.get(args['spot_id'])
        if not spot:
            abort(404, message="Parking spot not found.")

        if spot.is_occupied:
            abort(409, message="This spot is already marked as occupied.")

        # Check active overlapping bookings
        overlapping = Booking.query.filter(
            Booking.spot_id == spot.id,
            Booking.end_time == None
        ).first()
        if overlapping:
            abort(409, message="This spot already has an active booking.")

        vehicle_conflict = Booking.query.filter(
            Booking.vehicle_id == vehicle.id,
            Booking.end_time == None
        ).first()
        if vehicle_conflict:
            abort(409, message="This vehicle already has an active booking.")

        booking = Booking(
            vehicle_id=vehicle.id,
            spot_id=spot.id,
            start_time=start_time,
            end_time=None
        )

        spot.is_occupied = True  # ✅ Mark spot as occupied

        db.session.add(booking)
        db.session.commit()

        return {"message": "Booking started successfully.", "booking_id": booking.id}, 201


    @token_required
    def delete(self):
        current_user = g.current_user
        parser = reqparse.RequestParser()
        parser.add_argument('booking_id', type=int, required=True)
        args = parser.parse_args()

        booking = Booking.query.get(args['booking_id'])
        if not booking:
            abort(404, message="Booking not found.")

        if booking.vehicle.user_id != current_user.id:
            abort(403, message="You are not authorized to delete this booking.")

        booking.spot.is_occupied = False

        db.session.delete(booking)
        db.session.commit()

        return {"message": "Booking cancelled successfully."}, 200



class BookingReleaseResource(Resource):
    @token_required
    def patch(self, booking_id):
        current_user = g.current_user
        booking = Booking.query.get(booking_id)

        if not booking:
            abort(404, message="Booking not found.")

        if booking.vehicle.user_id != current_user.id:
            abort(403, message="You are not authorized to release this booking.")

        if booking.end_time:
            abort(400, message="This booking is already completed.")

        booking.end_time = datetime.now(timezone(timedelta(hours=5, minutes=30)))

        # ✅ Free the spot when booking is released
        booking.spot.is_occupied = False

        db.session.commit()

        return {
            "message": "Booking released successfully.",
            "end_time": booking.end_time.isoformat()
        }, 200




class UserLotsResource(Resource):
    @token_required
    def get(self):
        lots = ParkingLot.query.all() #tweak this later according to user preference

        lot_list = []
        for lot in lots:
            total_spots = len(lot.spots)
            occupied_spots = ParkingSpot.query.filter_by(lot_id=lot.id, is_occupied=True).count()
            available_spots = total_spots - occupied_spots

            lot_list.append({
                'id': lot.id,
                'prime_location_name': lot.prime_location_name,
                'address': lot.address,
                'pin_code': lot.pin_code,
                'price': lot.price,
                'number_of_spots': total_spots,
                'occupied_spots': occupied_spots,
                'available_spots': available_spots
            })

        return lot_list, 200
    

class Users(Resource):
    @admin_required
    def get(self):
        users = User.query.all()
        return [{
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "role": u.role.name if u.role else "No Role",
            "vehicles": [{
                "id": v.id,
                "license_plate": v.license_plate,
                "vehicle_type": v.vehicle_type
            } for v in u.vehicles]
        } for u in users], 200
    
class AdminBookingResource(Resource):
    @admin_required
    def get(self):
        bookings = Booking.query.all()

        result = []
        for b in bookings:
            spot = b.spot
            lot = spot.lot if spot else None

            result.append({
                "id": b.id,
                "start_time": b.start_time.isoformat(),
                "end_time": b.end_time.isoformat() if b.end_time else None,
                "vehicle_id": b.vehicle_id,
                "vehicle_number": b.vehicle.license_plate,
                "spot_id": b.spot_id,
                "created_at": b.created_at.isoformat(),
                "spot_number": spot.spot_number if spot else "Deleted Spot",
                "spot_type": spot.spot_type if spot else "N/A",
                "lot_id": lot.id if lot else None,
                "location_name": lot.prime_location_name if lot else "Unknown",
                "address": lot.address if lot else "Unknown Address",
                "pin_code": lot.pin_code if lot else "Unknown",
                "status": "active" if not b.end_time else "completed",
                "price": lot.price if lot else 0
            })

        return result, 200


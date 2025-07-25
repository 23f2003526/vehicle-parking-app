from celery import shared_task
import time
from backend.models import User, Booking, Vehicle, ParkingSpot, ParkingLot
from sqlalchemy.orm import joinedload
from main import db
from flask import current_app
from datetime import datetime
import os
import flask_excel as excel
from pyexcel import save_as

@shared_task(ignore_result = False)
def add(x,y):
    time.sleep(20)
    return x+y


@shared_task(ignore_result=False)
def create_csv(user_id):
    """
    Generate a CSV export of a user's booking history using flask-excel.
    """
    user = User.query.options(joinedload(User.vehicles)).get(user_id)
    if not user:
        return {"status": "error", "message": "User not found"}

    vehicle_ids = [v.id for v in user.vehicles]
    if not vehicle_ids:
        return {"status": "error", "message": "User has no vehicles"}

    bookings = (
        Booking.query
        .filter(Booking.vehicle_id.in_(vehicle_ids))
        .options(
            joinedload(Booking.vehicle),
            joinedload(Booking.spot).joinedload(ParkingSpot.lot)  
        )
        .all()
    )

    # Format bookings into list of dicts (rows)
    records = []
    for b in bookings:
        spot = b.spot
        lot = spot.lot if spot else None

        records.append({
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
            "price": lot.price if lot else 0,
        })

    # Save the file to disk
    export_dir = current_app.config.get("EXPORT_FOLDER", "./exports")
    os.makedirs(export_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"user_{user_id}_bookings_{timestamp}.csv"
    file_path = os.path.join(export_dir, filename)

    save_as(records=records, dest_file_name=file_path)

    return {
        "status": "success",
        "file": file_path,
        "message": f"{len(records)} bookings exported for user {user_id}"
    }
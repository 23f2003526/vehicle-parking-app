from collections import Counter, defaultdict
from backend.utils.email_templates import render_daily_reminder_html, render_monthly_report_html
from celery import shared_task
import time
from backend.models import Reservation, User, Booking, Vehicle, ParkingSpot, ParkingLot
from sqlalchemy.orm import joinedload
# from main import db
from flask import current_app
from datetime import datetime, timedelta, timezone
import os
import flask_excel as excel
from pyexcel import save_as
from backend.celery.mail_service import send_email

# @shared_task(ignore_result = False)
# def add(x,y):
#     time.sleep(20)
#     return x+y


@shared_task(ignore_result=False)
def create_csv(user_id):
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


@shared_task(ignore_result = True)
def email_reminder(to, subject, content):
    send_email(to, subject, content)

@shared_task(ignore_result = True)
def expire_stale_reservations():
    from main import db
    
    now = datetime.now(timezone(timedelta(hours=5, minutes=30)))
    stale_reservations = Reservation.query.filter(Reservation.expires_at <= now).all()
    
    print(f"Now: {now}, Stale: {stale_reservations}")

    for res in stale_reservations:
        res.spot.status = 'available'
        db.session.delete(res)

    db.session.commit()


IST = timezone(timedelta(hours=5, minutes=30))

def _today_ist_range():
    now = datetime.now(IST)
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
    return start, end

def _prev_month_ist_range():
    # First day of current month (IST)
    now = datetime.now(IST)
    first_this = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    # Last month
    last_month_end = first_this - timedelta(microseconds=1)
    first_last = last_month_end.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    # Label - "July 2025"
    month_label = last_month_end.strftime("%B %Y")
    return first_last, first_this, month_label

@shared_task(ignore_result=True)
def send_daily_reminders():
    """
    Sending daily reminder to users who:
      - have not booked or reserved a spot today,
      - there are new lots created today.
    Runs once daily at set time.
    """
    from main import db
    app = current_app._get_current_object()
    with app.app_context():
        start_today, end_today = _today_ist_range()

        # New lots created today
        new_lots_count = ParkingLot.query.filter(
            ParkingLot.created_at >= start_today,
            ParkingLot.created_at < end_today
        ).count()

        users = User.query.options(joinedload(User.vehicles)).all()
        for user in users:
            vehicle_ids = [v.id for v in user.vehicles]
            has_today_booking = False
            has_today_reservation = False

            if vehicle_ids:
                has_today_booking = db.session.query(Booking.id).filter(
                    Booking.vehicle_id.in_(vehicle_ids),
                    Booking.start_time >= start_today,
                    Booking.start_time < end_today
                ).first() is not None

                has_today_reservation = db.session.query(Reservation.id).filter(
                    Reservation.vehicle_id.in_(vehicle_ids),
                    Reservation.created_at >= start_today,
                    Reservation.created_at < end_today
                ).first() is not None

            # Only remind if no activity today OR if new lots were added today
            if not (has_today_booking or has_today_reservation) or new_lots_count > 0:
                content = render_daily_reminder_html(user, new_lots_count=new_lots_count)
                try:
                    send_email(user.email, "Your Daily Parking Reminder", content)
                except Exception as e:
                    # Log and continue
                    print(f"[daily_reminders] Failed sending to {user.email}: {e}")

@shared_task(ignore_result=True)
def send_monthly_reports():
    """
    On the 1st of every month (IST): compute stats for the previous month and email users.
    """
    app = current_app._get_current_object()
    with app.app_context():
        start_month, end_month, month_label = _prev_month_ist_range()

        users = User.query.options(joinedload(User.vehicles)).all()
        for user in users:
            if not user.email:
                continue

            vehicle_ids = [v.id for v in user.vehicles]
            if not vehicle_ids:
                # send a "no activity" report
                stats = {
                    "month_label": month_label,
                    "total_bookings": 0,
                    "total_spent": 0.0,
                    "most_used_lot": None,
                    "breakdown_by_lot": [],
                }
                html = render_monthly_report_html(user, stats)
                try:
                    send_email(user.email, f"Your {month_label} Parking Report", html)
                except Exception as e:
                    print(f"[monthly_reports] Failed sending to {user.email}: {e}")
                continue

            # Fetch bookings for previous month
            bookings = (
                Booking.query
                .filter(
                    Booking.vehicle_id.in_(vehicle_ids),
                    Booking.start_time >= start_month,
                    Booking.start_time < end_month,
                )
                .options(
                    joinedload(Booking.spot).joinedload(ParkingSpot.lot),
                    joinedload(Booking.vehicle),
                )
                .all()
            )

            total_bookings = len(bookings)

            # calculate spend aaaaaaaaaaaaaaaa
            total_spent = 0.0
            lot_counter = Counter()
            breakdown_map = defaultdict(int)

            for b in bookings:
                lot = b.spot.lot if b.spot and b.spot.lot else None
                lot_name = lot.prime_location_name if lot else "Unknown"
                    
                if lot and hasattr(lot, 'price') and lot.price:
                        start = b.start_time
                        end = b.end_time or datetime.now(IST)
                        # duration = end - start
                        hours = max(1, int((end - start).total_seconds() // 3600))
                        total_spent += hours * float(lot.price)

                lot_counter[lot_name] += 1
                breakdown_map[lot_name] += 1

            most_used_lot = None
            if lot_counter:
                most_used_lot = lot_counter.most_common(1)[0][0]

            breakdown_by_lot = [
                {"lot": lot_name, "count": count}
                for lot_name, count in sorted(breakdown_map.items(), key=lambda x: (-x[1], x[0]))
            ]

            stats = {
                "month_label": month_label,
                "total_bookings": total_bookings,
                "total_spent": total_spent,
                "most_used_lot": most_used_lot,
                "breakdown_by_lot": breakdown_by_lot,
            }

            html = render_monthly_report_html(user, stats)

            try:
                send_email(user.email, f"Your {month_label} Parking Report", html)
            except Exception as e:
                print(f"[monthly_reports] Failed sending to {user.email}: {e}")

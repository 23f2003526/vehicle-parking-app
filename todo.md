# TO DO

- celery -A main:celery_app worker -l INFO
- celery -A main:celery_app beat -l INFO
- ~/go/bin/MailHog

- yaml file
- project file
- video

# DONE

- make it so ki admin is created khud se
- confirm what is the length of salt that generate_password_hash generates -- I think 16
- Admin functionalities:
  Create/edit/delete parking lots.
  View parking lot details and spot status/summary.
  Automatically create parking spots based on the maximum capacity of the lot.
  View/delete parking spots (only if empty).

- In AvailableParkingLotsTable > openBookingModal is not working. Figure out a way how to automatically assign spot_id while booking. Fix what request frontend is sending to backend at /api/booking.

### I am now using Pinia.

- Call a Flask route like /export-parking-csv (POST) in frontend. After it is downloaded, send an alert to user.

- add amount paid column in Bookings Table.. update it when user clicks release. Display it in csv file generated.
- add links so user can switch from login and signup

- complete models.py
- watch live session 3 from YT.

- ADMIN ENDPOINTS: WHAT's LEFT :: Admin should be able to see list of all users and their details. (username, spot used, reservation history etc.)
- do I make a new component for ShowBookings.vue?
- ParkingLotView -> OpenOccupiedDetails -> Fix it so reserved main it shows details of user who reserved it.
- thinking whether to include a status in parking_spot : occupied, available and reserved. Cost calculation only starts when the status is changed from reserved to occupied.

- Summary
- Edit Profile

- Navbar (somewhat, not optimized at all)

- Landing Page

- celery tasks
- fix the delete and edit button disappearing issue when reloading in ParkingLotView.vue
- fix login and logout in navbar.

- Fix the bug that user can reserve an already Parked vehicle. (and vice versa?)

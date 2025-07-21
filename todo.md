# TO DO

- fix the delete and edit button disappearing issue when reloading in ParkingLotView.vue

- complete models.py
- watch live session 3 from YT.

- ADMIN ENDPOINTS: WHAT's LEFT :: Admin should be able to see list of all users and their details. (username, spot used, reservation history etc.)

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

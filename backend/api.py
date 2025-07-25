from main import app
from flask_restful import Api

from backend.routes import BookingResource, Signup, Login, Dashboard, LotGetCreate, LotUpdateDelete, LotSummary, SpotResource, UserLotsResource, VehicleResource, BookingReleaseResource, ActiveBookingResource, Users, AdminBookingResource

api = Api(app)

api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Dashboard, '/dashboard')


api.add_resource(LotGetCreate, '/admin/lots')  
api.add_resource(LotUpdateDelete, '/admin/lots/<int:lot_id>')

api.add_resource(LotSummary, '/lots/<int:lot_id>/summary') # use this for user side also

api.add_resource(SpotResource, '/admin/lots/<int:lot_id>/spots/<int:spot_number>')
api.add_resource(ActiveBookingResource, '/admin/lots/<int:lot_id>/spots/<string:spot_number>/active-booking')


api.add_resource(VehicleResource, '/vehicles')

api.add_resource(BookingResource, '/bookings')
api.add_resource(BookingReleaseResource, '/bookings/<int:booking_id>/release')

api.add_resource(UserLotsResource, '/lots')

api.add_resource(Users, '/admin/users')
api.add_resource(AdminBookingResource, '/admin/bookings')







from app import app
from flask_restful import Api

from backend.routes import Signup, Login, Dashboard, LotGetCreate, LotUpdateDelete, LotSummary, SpotResource

api = Api(app)

api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Dashboard, '/dashboard')


api.add_resource(LotGetCreate, '/admin/lots')  
api.add_resource(LotUpdateDelete, '/admin/lots/<int:lot_id>')
api.add_resource(LotSummary, '/admin/lots/<int:lot_id>/summary')

api.add_resource(SpotResource, '/admin/lots/<int:lot_id>/spots/<int:spot_number>')





from flask_restful import reqparse

signup_parser = reqparse.RequestParser()
signup_parser.add_argument("name", type=str, help='Name of the user is required', required=True, location='json')
signup_parser.add_argument("email", type=str, help='Email of the user is required', required=True, location='json')
signup_parser.add_argument("password", type=str, help='Password of the user is required', required=True, location='json')


login_parser = reqparse.RequestParser()
login_parser.add_argument('email', type=str, help='This field cannot be empty', required=True, location='json')
login_parser.add_argument('password', type=str, help='This field cannot be empty', required=True, location='json')

lot_parser = reqparse.RequestParser()
lot_parser.add_argument('prime_location_name', type=str, help='This field cannot be empty', required=True, location='json')
lot_parser.add_argument('address', type=str, help='This field cannot be empty', required=True, location='json')
lot_parser.add_argument('pin_code', type=int, help='This field cannot be empty', required=True, location='json')
lot_parser.add_argument('price', type=int, help='This field cannot be empty', required=True, location='json')
lot_parser.add_argument('number_of_spots', type=int, help='This field cannot be empty', required=True, location='json')

from flask import Flask, request, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource ,  reqparse, abort
from flask_login import LoginManager, login_required, current_user,logout_user
from model import db, User
from flask_cors import CORS


import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

app = Flask(__name__)
app.config['SECRET_KEY'] = '2#fJ7$kd_9W!sL@0'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


class RegisterResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help='Username cannot be blank')
        parser.add_argument('password', type=str, required=True, help='Password cannot be blank')

        args = parser.parse_args()

        username = args['username']
        password = args['password']

        # Validate data (already handled by reqparse, but can add more checks if needed)
        if not username or not password:
            return {'error': 'Please fill in all fields.'}, 400

        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return {'error': 'incorrect credentials.'}, 400

        # Create new user instance and save to database
        new_user = User(username=username, password=password)  # Ensure password is hashed in production
        db.session.add(new_user)
        db.session.commit()

        return {'message': 'Login successful'}, 201
    

api.add_resource(RegisterResource, '/register')

if __name__ == "__main__":
    app.run(port=5555, debug=True)
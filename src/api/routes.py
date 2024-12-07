"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

# jwt modules
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.

# /token POST
# This route is for when the user already exists and needs an access token.
# Create a query to check and return an access token for an existing user,
# or None if no user was found.
@api.route("/token", methods=["POST"])
def generate_token():

    # receive the request and convert the body of the request
    # into json format
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    # query the User table to see if the user exists
    email = email.lower()
    user = User.query.filter_by(email = email, password = password).first()

    if user is None:
        return jsonify({"msg": "Bad email or password"}), 401

    # if the user does exist, create an access token for them and
    # return a response
    access_token = create_access_token(identity=user.id)
    response = {
        "access_token": access_token,
        "user_id": user.id,
        "msg": f'Welcome {user.email}!'
    }

    return jsonify(response)

# /signup POST
# create a route for /signup that will add a user's email and password to the DB
@api.route('/signup', methods=["POST"])
def register_user():

    # receive the request and convert the body of the request
    # into json format
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    # query to check if email already exists
    email = email.lower()
    user = User.query.filter_by(email=email).first()

    # make a condition that the user is not None and that the email exists
    if user is not None and user.email == email:
        response = {
            'msg': 'User already exists'
        }
        return jsonify(response), 403

    # if the email does not exist, go ahead and make a new record in the DB
    # let's sign this person up
    user = User()
    user.email = email
    user.password = password
    user.is_active = True
    db.session.add(user)
    db.session.commit()

    response = {
        'msg': f'Congratulations, {user.email}! You have successfully signed up!'
    }
    return jsonify(response), 200












# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
# create a route for /private the will display the private page
# based on the users access token
@api.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200












@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200








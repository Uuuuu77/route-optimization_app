#!/usr/bin/python3

from flask import Flask, jsonify, request, abort
from models.user import db, User
from services import nearby_places, route_finder, my_location

app = Flask(__name__)

# Configure the database URI and initialize the database with your Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db.init_app(app)


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        abort(404, description="User not found")
    return jsonify(user.to_dict())


@app.route('/nearby-places', methods=['GET'])
def get_nearby_places_view():
    location = request.args.get('location')  # Get location from request args

    if not location:
        abort(400, description="Missing location parameter")

    try:
        data = nearby_places.get_nearby_places(location)
    except Exception as e:
        abort(500, description=str(e))

    return jsonify(data)


@app.route('/route-finder', methods=['GET'])
def find_route_view():
    start_location = request.args.get('start_location')  # Get start location
    end_location = request.args.get('end_location')  # Get end location

    if not start_location or not end_location:
        abort(400, description="Missing start_location end_location parameter")

    try:
        data = route_finder.find_route(start_location, end_location)
    except Exception as e:
        abort(500, description=str(e))

    return jsonify(data)


@app.route('/my-location', methods=['GET'])
def get_my_location_view():
    try:
        data = my_location.get_my_location()
    except Exception as e:
        abort(500, description=str(e))

    return jsonify(data)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

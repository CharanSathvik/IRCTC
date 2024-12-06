from flask import Blueprint, request, jsonify
from . import db
from .models import User, Train, Booking
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime
import os

bp = Blueprint('main', __name__)

# User Registration Endpoint
@bp.route('/api/register', methods=['POST'])
def register_user():
    data = request.get_json()
    new_user = User(
        username=data['username'],
        email=data['email'],
        role=data.get('role', 'user')  # Default role is "user"
    )
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully", "user_id": new_user.id}), 201

# User Login Endpoint
@bp.route('/api/login', methods=['POST'])
def login_user():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity={"id": user.id, "role": user.role})
        return jsonify({"message": "Login successful", "access_token": access_token}), 200
    return jsonify({"message": "Invalid username or password"}), 401

# Add New Train (Admin Only)
@bp.route('/api/admin/train', methods=['POST'])
def add_train():
    admin_api_key = request.headers.get('X-API-Key')
    if admin_api_key != os.getenv('ADMIN_API_KEY'):
        return jsonify({"message": "Unauthorized"}), 403

    data = request.get_json()
    new_train = Train(
        name=data['name'],
        source=data['source'],
        destination=data['destination'],
        total_seats=data['total_seats']
    )
    db.session.add(new_train)
    db.session.commit()
    return jsonify({"message": f"Train {new_train.name} added successfully", "train_id": new_train.id}), 201

# Get Seat Availability
@bp.route('/api/trains/availability', methods=['GET'])
def get_seat_availability():
    source = request.args.get('source')
    destination = request.args.get('destination')

    trains = Train.query.filter_by(source=source, destination=destination).all()
    results = [
        {
            "train_id": train.id,
            "name": train.name,
            "available_seats": train.total_seats - sum([b.seats_booked for b in train.bookings])
        }
        for train in trains
    ]
    return jsonify({"results": results}), 200

# Book a Seat
@bp.route('/api/trains/book', methods=['POST'])
@jwt_required()
def book_seat():
    user_data = get_jwt_identity()
    if user_data['role'] != 'user':
        return jsonify({"message": "Unauthorized"}), 403

    data = request.get_json()
    train = Train.query.get(data['train_id'])

    if not train:
        return jsonify({"message": "Train not found"}), 404

    seats_to_book = data.get('seats', 1)
    booked_seats = sum([b.seats_booked for b in train.bookings])

    if booked_seats + seats_to_book > train.total_seats:
        return jsonify({"message": "Not enough seats available"}), 409

    # Create Booking
    new_booking = Booking(
        user_id=user_data['id'],
        train_id=train.id,
        seats_booked=seats_to_book
    )
    db.session.add(new_booking)
    db.session.commit()

    return jsonify({"message": "Booking successful", "booking_id": new_booking.id}), 201

# Get Specific Booking Details
@bp.route('/api/bookings/<int:booking_id>', methods=['GET'])
@jwt_required()
def get_booking_details(booking_id):
    user_data = get_jwt_identity()
    booking = Booking.query.get(booking_id)

    if not booking or booking.user_id != user_data['id']:
        return jsonify({"message": "Booking not found or unauthorized access"}), 404

    return jsonify({
        "booking_id": booking.id,
        "train_id": booking.train_id,
        "seats_booked": booking.seats_booked,
        "timestamp": booking.timestamp.isoformat()
    }), 200

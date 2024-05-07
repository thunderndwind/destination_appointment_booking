from flask import request, jsonify
from main_app import app
from main_app.models import Booking, db

@app.before_first_request
def initialize():
    db.create_all()

@app.route('/')
def index():
    return "Hello, World! from volume"

@app.route('/api/getBookings', methods=['GET'])
def get_traveler_bookings():
    bookings = Booking.query.all()

    bookings_list = []
    for booking in bookings:
        booking_data = {
            'id': booking.id,
            'user_id': booking.user_id,
            'appointment_id': booking.appointment_id,
            'created_at': booking.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': booking.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        bookings_list.append(booking_data)

    return jsonify({'bookings': bookings_list})

@app.route('/api/createBooking', methods=['POST'])
def create_booking():
    data = request.get_json()

    user_id = data.get('user_id')
    appointment_id = data.get('appointment_id')

    if not all([user_id, appointment_id]):
        return jsonify({'error': 'Missing required fields'}), 400

    new_booking = Booking(
        user_id=user_id,
        appointment_id=appointment_id
    )

    db.session.add(new_booking)
    db.session.commit()

    return jsonify({'message': 'booking created successfully'}), 201

@app.route('/api/updateBooking/<int:booking_id>', methods=['PUT'])
def update_traveler_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if booking is None:
        return jsonify({'error': 'booking not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided in the request'}), 400

    try:
        booking.user_id = data.get('user_id', booking.user_id)
        booking.appointment_id = data.get('appointment_id', booking.appointment_id)

        db.session.commit()
        return jsonify({'message': 'booking updated successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error updating booking', 'details': str(e)}), 500

@app.route('/api/deleteBooking/<int:booking_id>', methods=['DELETE'])
def delete_traveler_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if booking is None:
        return jsonify({'error': 'booking not found'}), 404

    try:
        db.session.delete(booking)
        db.session.commit()
        return jsonify({'message': 'booking deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error deleting booking', 'details': str(e)}), 500
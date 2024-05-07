from flask import request, jsonify
import json
from main_app import app
from main_app.models import Appointment, db

@app.before_first_request
def initialize():
    db.create_all()

@app.route('/')
def index():
    return "Hello, World! from volume"

@app.route('/api/getAppointments', methods=['GET'])
def get_appointments():
    appointments = Appointment.query.all()

    appointments_list = []
    for appointment in appointments:
        appointment_data = {
            'id': appointment.id,
            'bus_destination_id': appointment.bus_destination_id,
            'date_time': appointment.date_time.strftime('%Y-%m-%d %H:%M:%S'),
            'capacity': appointment.capacity,
            'booked': appointment.booked,
            'created_at': appointment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': appointment.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        appointments_list.append(appointment_data)

    return jsonify({'appointments': appointments_list})

@app.route('/api/createAppointment', methods=['POST'])
def create_appointment():
    data = request.get_json()

    bus_destination_id = data.get('bus_destination_id')
    date_time = data.get('date_time')
    capacity = data.get('capacity')

    if not all([bus_destination_id, date_time, capacity]):
        return jsonify({'error': 'Missing required fields'}), 400

    new_appointment = Appointment(
        bus_destination_id=bus_destination_id,
        date_time=date_time,
        capacity=capacity
    )

    db.session.add(new_appointment)
    db.session.commit()

    return jsonify({'message': 'Appointment created successfully'}), 201

@app.route('/api/updateAppointment/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if appointment is None:
        return jsonify({'error': 'Appointment not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided in the request'}), 400

    try:
        appointment.bus_destination_id = data.get('bus_destination_id', appointment.bus_destination_id)
        appointment.date_time = data.get('date_time', appointment.date_time)
        appointment.capacity = data.get('capacity', appointment.capacity)

        db.session.commit()
        return jsonify({'message': 'Appointment updated successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error updating appointment', 'details': str(e)}), 500

@app.route('/api/deleteAppointment/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):

    appointment = Appointment.query.get(appointment_id)
    if appointment is None:
        return jsonify({'error': 'Appointment not found'}), 404

    try:
        db.session.delete(appointment)
        db.session.commit()
        return jsonify({'message': 'Appointment deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error deleting appointment', 'details': str(e)}), 500
    

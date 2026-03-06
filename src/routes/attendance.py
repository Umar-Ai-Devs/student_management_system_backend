from flask import Blueprint, jsonify, request
from src.extentions import db
from src.models.attendance import Attendance
from src.schemas.attendance_schema import AttendanceSchema
from marshmallow import ValidationError
from datetime import date




attendance_bp = Blueprint('attendance', __name__)



@attendance_bp.route('/attendance', methods=['POST'])
def mark_attendance():
    data = request.get_json()

    try:
        validated_data = AttendanceSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    attendance_data = AttendanceSchema().to_attendance(validated_data)

    attendance_record = Attendance(
        student_id=attendance_data['student_id'],
        date=attendance_data['date'],
        is_present=attendance_data['is_present']
    )

    db.session.add(attendance_record)
    db.session.commit()

    return jsonify({'message': 'Attendance marked successfully'}), 201

@attendance_bp.route('/attendance/<int:student_id>/<string:date_str>', methods=['GET'])
def get_attendance(student_id, date_str):
    try:
        date_obj = date.fromisoformat(date_str)
    except ValueError:
        return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    attendance_records = Attendance.query.filter_by(student_id=student_id, date=date_obj).all()

    if not attendance_records:
        return jsonify({'message': 'No attendance records found for the given student and date.'}), 404

    attendance_data = [
        {
            'id': record.id,
            'student_id': record.student_id,
            'date': record.date.isoformat(),
            'is_present': record.is_present
        }
        for record in attendance_records
    ]

    return jsonify(attendance_data), 200


@attendance_bp.route('/attendance/<int:attendance_id>', methods=['DELETE'])
def delete_attendance(attendance_id):
    attendance_record = Attendance.query.get(attendance_id)
    if not attendance_record:
        return jsonify({'message': 'Attendance record not found'}), 404

    db.session.delete(attendance_record)
    db.session.commit()

    return jsonify({'message': 'Attendance record deleted successfully'}), 200


@attendance_bp.route('/attendance/<int:attendance_id>', methods=['PUT'])
def update_attendance(attendance_id):
    attendance_record = Attendance.query.get(attendance_id)
    if not attendance_record:
        return jsonify({'message': 'Attendance record not found'}), 404

    data = request.get_json()

    try:
        validated_data = AttendanceSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    attendance_data = AttendanceSchema().to_attendance(validated_data)

    attendance_record.student_id = attendance_data['student_id']
    attendance_record.date = attendance_data['date']
    attendance_record.is_present = attendance_data['is_present']

    db.session.commit()

    return jsonify({'message': 'Attendance record updated successfully'}), 200
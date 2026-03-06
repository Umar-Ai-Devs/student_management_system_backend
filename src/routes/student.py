from flask import Blueprint, request, jsonify
from src.extentions import db
from src.models.student import Student
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.schemas.student_scema import StudentSchema
from marshmallow import ValidationError


student_bp = Blueprint('student', __name__)

@student_bp.route('/students', methods=['GET'])
@jwt_required()
def get_students():
    
    students = Student.query.all()

    student_list = []

    for student in students:
        student_data = {
            'id': student.id,
            'name': student.name,
            'email': student.email,
            'age': student.age,
            'department': student.department
        }
        student_list.append(student_data)

    return jsonify({'data': student_list}), 200

@student_bp.route('/students', methods=['POST'])
@jwt_required()
def add_student():

    data = request.get_json() 

    try:
        validated_data = StudentSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400




    name = data.get('name')
    email = data.get('email')
    age = data.get('age')
    department = data.get('department')

    if not name or not email or not age:
        return jsonify({'message': 'Missing required fields'}), 400
    
    existing_student = Student.query.filter_by(email=email).first()
    if existing_student:
        return jsonify({'message': 'Student with this email already exists'}), 400
    
    std = Student(name=name, email=email, age=age, department=department)

    db.session.add(std)
    db.session.commit()

    # Here you would normally add the student to the database

    return jsonify({'message': 'Student added successfully'}), 200



@student_bp.route('/students/<int:student_id>', methods=['DELETE'])
@jwt_required()
def delete_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'message': 'Student not found'}), 404

    db.session.delete(student)
    db.session.commit()

    return jsonify({'message': 'Student deleted successfully'}), 200



@student_bp.route('/students/<int:student_id>', methods=['PUT'])
@jwt_required()
def update_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'message': 'Student not found'}), 404

    data = request.get_json()

    try:
        validated_data = StudentSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    student.name = data.get('name', student.name)
    student.email = data.get('email', student.email)
    student.age = data.get('age', student.age)
    student.department = data.get('department', student.department)

    db.session.commit()

    return jsonify({'message': 'Student updated successfully'}), 200
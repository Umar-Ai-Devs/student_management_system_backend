from flask import Flask, render_template, request, redirect, url_for, flash
from flask import Blueprint, request, jsonify
from src.extentions import db
from src.models.teacher import Teacher
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.schemas.teachers_schema import TeacherSchema
from marshmallow import ValidationError

teacher_bp = Blueprint('teacher', __name__)

@teacher_bp.route('/teachers', methods=['GET'])
@jwt_required()
def get_teachers():
    teachers = Teacher.query.all()

    teacher_list = []

    for teacher in teachers:
        teacher_data = {
            'id': teacher.id,
            'name': teacher.name,
            'email': teacher.email,
            'age': teacher.age,
            'subject': teacher.subject
        }
        teacher_list.append(teacher_data)

    return jsonify({'data': teacher_list}), 200



@teacher_bp.route('/teachers', methods=['POST'])
@jwt_required()
def add_teacher():
    data = request.get_json()

    try:
        validated_data = TeacherSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    teacher_data = TeacherSchema().to_teacher(validated_data)

    teacher = Teacher(
        name=teacher_data['name'],
        age=teacher_data['age'],
        email=teacher_data['email'],
        subject=teacher_data['subject']
    )

    db.session.add(teacher)
    db.session.commit()

    return jsonify({'message': 'Teacher added successfully'}), 201


@teacher_bp.route('/teachers/<int:teacher_id>', methods=['DELETE'])
@jwt_required()
def delete_teacher(teacher_id):
    teacher = Teacher.query.get(teacher_id)
    if not teacher:
        return jsonify({'message': 'Teacher not found'}), 404

    db.session.delete(teacher)
    db.session.commit()

    return jsonify({'message': 'Teacher deleted successfully'}), 200


@teacher_bp.route('/teachers/<int:teacher_id>', methods=['PUT'])
@jwt_required()
def update_teacher(teacher_id):
    teacher = Teacher.query.get(teacher_id)
    if not teacher:
        return jsonify({'message': 'Teacher not found'}), 404

    data = request.get_json()

    try:
        validated_data = TeacherSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    teacher_data = TeacherSchema().to_teacher(validated_data)

    teacher.name = teacher_data['name']
    teacher.age = teacher_data['age']
    teacher.email = teacher_data['email']
    teacher.subject = teacher_data['subject']

    db.session.commit()

    return jsonify({'message': 'Teacher updated successfully'}), 200


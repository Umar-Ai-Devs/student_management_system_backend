from flask import Blueprint, request, jsonify
from src.extentions import db
from src.models.admin import Admin
from src.extentions import bcrypt
from flask_jwt_extended import create_access_token
from src.schemas.auth_schema import LoginSchema
from marshmallow import ValidationError
from datetime import date
import os
from werkzeug.utils import secure_filename

auth_bp = Blueprint('auth', __name__)
    

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        LoginSchema().load(request.form)
    except ValidationError as err:
        return jsonify(err.messages), 400

    email = request.form.get('email')
    password = request.form.get('password')
    
    admin = Admin.query.filter_by(email=email).first()
    if not bcrypt.check_password_hash(admin.password, password):
        return jsonify({'message': 'Invalid password'}), 401

    token = create_access_token(identity=str({"id":admin.id,"role":"admin"}))
    return jsonify({'token': token}), 200

@auth_bp.route('/register', methods=['POST'])
def register():

    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    image = request.files.get('image')

    filename = secure_filename(image.filename)
    upload_path = os.path.join('uploads/profile', filename)
    os.makedirs('uploads/profile', exist_ok=True)
    image.save(upload_path)


    if not name or not email or not password:
        return jsonify({'message': 'Missing required fields'}), 400

    existing_admin = Admin.query.filter_by(email=email).first()
    if existing_admin:
        return jsonify({'message': 'Admin with this email already exists'}), 400

    new_admin = Admin(
        name=name,
        email=email,
        password=bcrypt.generate_password_hash(password).decode('utf-8'),
        image=upload_path
    )
    
    db.session.add(new_admin)
    db.session.commit()

    return jsonify({'message': 'Admin registered successfully'}), 201
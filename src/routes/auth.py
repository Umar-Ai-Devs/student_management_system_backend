from flask import Blueprint, request, jsonify
from src.extentions import db
from src.models.admin import Admin
from src.extentions import bcrypt
from flask_jwt_extended import create_access_token
from src.schemas.auth_schema import LoginSchema, RegisterSchema
from marshmallow import ValidationError

auth_bp = Blueprint('auth', __name__)
    

@auth_bp.route('/login', methods=['POST'])
def login():
    # Handle both JSON and form data
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()

    try:
        LoginSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    email = data.get('email')
    password = data.get('password')
    
    admin = Admin.query.filter_by(email=email).first()
    if not admin:
        return jsonify({'message': 'Invalid email or password'}), 401
    
    if not bcrypt.check_password_hash(admin.password, password):
        return jsonify({'message': 'Invalid email or password'}), 401

    token = create_access_token(identity=str({"id":admin.id,"role":"admin"}))
    return jsonify({'token': token}), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        # Handle both JSON and form data
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()

        print(f"Received data: {data}")

        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        print(f"Name: {name}, Email: {email}, Password: {'***' if password else None}")

        if not name or not email or not password:
            print("Missing required fields")
            return jsonify({'message': 'Missing required fields'}), 400

        existing_admin = Admin.query.filter_by(email=email).first()
        if existing_admin:
            print(f"Admin already exists with email: {email}")
            return jsonify({'message': 'Admin with this email already exists'}), 400

        new_admin = Admin(
            name=name,
            email=email,
            password=bcrypt.generate_password_hash(password).decode('utf-8')
        )
        
        db.session.add(new_admin)
        db.session.commit()

        print("Admin registered successfully")
        return jsonify({'message': 'Admin registered successfully'}), 201
    
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return jsonify({'message': f'Error: {str(e)}'}), 500
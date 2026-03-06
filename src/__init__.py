import os
from flask import Flask
from src.extentions import db, jwt, bcrypt
from dotenv import load_dotenv

load_dotenv()  # load .env file

def create_app():
    app = Flask(__name__)

    # JWT Secret Key
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

    # Database credentials
    username = os.environ.get('DB_USERNAME')
    password = os.environ.get('DB_PASSWORD')
    host = os.environ.get('DB_HOST')
    port = int(os.environ.get('DB_PORT'))
    database = os.environ.get('DB_NAME')
    ca_path = r"C:\Users\umara\OneDrive\Desktop\My_Projects\Student_Management_System\student_management_system\Backend\ca-certificate.pem"

    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Pass SSL options
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "connect_args": {
            "ssl": {"ca": ca_path}
        }
    }

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # Register blueprints
    from src.routes.auth import auth_bp
    from src.routes.student import student_bp
    from src.routes.teacher import teacher_bp
    from src.routes.attendance import attendance_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(teacher_bp)
    app.register_blueprint(attendance_bp)

    with app.app_context():
        db.create_all()  # This will create tables

    return app
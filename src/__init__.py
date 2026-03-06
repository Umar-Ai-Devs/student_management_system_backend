from flask import Flask
from src.extentions import db, jwt, bcrypt

def create_app():
    app = Flask(__name__)

    # JWT Secret Key
    app.config['JWT_SECRET_KEY'] = 'your-secret-key-here'

    # Database credentials
    username = "avnadmin"
    password = "AVNS_dBtunhJhTrFCFeu82pQ"
    host = "mysql-2ef3e0dd-umaraidevs-b8b7.a.aivencloud.com"
    port = 28018
    database = "defaultdb"
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
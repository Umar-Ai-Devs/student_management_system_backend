from flask import Flask
from flask_cors import CORS
from src.extentions import db, bcrypt, jwt

from src.routes.auth import auth_bp
from src.routes.student import student_bp
from src.routes.teacher import teacher_bp
from src.routes.attendance import attendance_bp



def create_app():
    
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(student_bp, url_prefix='/api')
    app.register_blueprint(teacher_bp, url_prefix='/api')
    app.register_blueprint(attendance_bp, url_prefix='/api')
    



    app.config['SECRET_KEY'] = 'supersecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/db_lms_1'


    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        db.create_all()

    return app

from flask import Flask  # นำเข้า Flask สำหรับสร้างแอป
from flask_sqlalchemy import SQLAlchemy  # นำเข้า SQLAlchemy สำหรับจัดการฐานข้อมูล
from flask_login import LoginManager  # นำเข้า LoginManager สำหรับการจัดการการเข้าสู่ระบบ
from flask_bcrypt import Bcrypt  # นำเข้า Bcrypt สำหรับการเข้ารหัสรหัสผ่าน
import os  # นำเข้า os สำหรับการจัดการระบบไฟล์

# สร้างอินสแตนซ์ของ SQLAlchemy, Bcrypt และ LoginManager
db = SQLAlchemy()  # อินสแตนซ์สำหรับฐานข้อมูล
bcrypt = Bcrypt()  # อินสแตนซ์สำหรับการเข้ารหัสรหัสผ่าน
login_manager = LoginManager()  # อินสแตนซ์สำหรับการจัดการการเข้าสู่ระบบ

# สร้างแอป Flask ทั่วไป
app = Flask(__name__)  # สร้างแอป Flask

# การตั้งค่าคอนฟิก
app.config['SECRET_KEY'] = 'your_secret_key'  # กำหนดคีย์ลับสำหรับเซสชัน
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # ตั้งค่าการเชื่อมต่อฐานข้อมูล
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # ไดเรกทอรีที่ไฟล์อัปโหลดจะถูกเก็บ
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # จำกัดขนาดไฟล์อัปโหลดสูงสุด 16MB

# ตรวจสอบว่าไดเรกทอรีสำหรับอัปโหลดมีอยู่แล้วหรือไม่
if not os.path.exists(app.config['UPLOAD_FOLDER']):  # ถ้าไม่มี
    os.makedirs(app.config['UPLOAD_FOLDER'])  # สร้างไดเรกทอรี

# เริ่มต้นส่วนเสริมด้วยแอป
db.init_app(app)  # เริ่มต้น SQLAlchemy
bcrypt.init_app(app)  # เริ่มต้น Bcrypt
login_manager.init_app(app)  # เริ่มต้น LoginManager

# นำเข้ามอเดลและบลูพริ้นท์หลังจากเริ่มต้นแอป
from .models import User  # นำเข้ามอเดล User
from .routes import flask  # นำเข้าบลูพริ้นท์ flask

app.register_blueprint(flask)  # ลงทะเบียนบลูพริ้นท์

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # โหลดผู้ใช้จากฐานข้อมูล

# Optional: บรรทัดนี้ทำให้แอปทำงานหากสคริปต์นี้ถูกเรียกใช้งานโดยตรง
if __name__ == "__main__":  # ถ้าเป็นสคริปต์หลัก
    app.run(debug=True)  # เริ่มเซิร์ฟเวอร์ในโหมดดีบัก

from flask_wtf import FlaskForm  # นำเข้า FlaskForm สำหรับสร้างฟอร์ม
from wtforms.fields import StringField, EmailField, PasswordField, SubmitField, FileField, BooleanField  # นำเข้าฟิลด์ต่าง ๆ
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError  # นำเข้าตัวตรวจสอบ
from flask_wtf.file import FileAllowed  # นำเข้า FileAllowed สำหรับตรวจสอบประเภทไฟล์
from CTWApp.models import User  # นำเข้าโมเดล User
from CTWApp import db  # นำเข้า db จาก CTWApp

class LoginForm(FlaskForm):
    username = StringField(
        label='Username',  # ช่องสำหรับชื่อผู้ใช้
        validators=[DataRequired(), Length(min=4, max=50)]  # ตรวจสอบว่าต้องกรอกข้อมูลและความยาวอยู่ในช่วง 4-50 ตัวอักษร
    )
    password = PasswordField(
        label='Password',  # ช่องสำหรับรหัสผ่าน
        validators=[DataRequired()]  # ตรวจสอบว่าต้องกรอกข้อมูล
    )
    remember = BooleanField('Remember Me')  # ตัวเลือก "จดจำฉัน"
    submit = SubmitField('Login')  # ปุ่ม "เข้าสู่ระบบ"

class RegisterForm(FlaskForm):
    username = StringField(
        label='Username',  # ช่องสำหรับชื่อผู้ใช้
        validators=[DataRequired(), Length(min=4, max=50)]  # ตรวจสอบว่าต้องกรอกข้อมูลและความยาวอยู่ในช่วง 4-50 ตัวอักษร
    )
    email = EmailField(
        label='Email Address',  # ช่องสำหรับอีเมล
        validators=[DataRequired(), Email()]  # ตรวจสอบว่าต้องกรอกข้อมูลและเป็นอีเมลที่ถูกต้อง
    )
    fname = StringField(
        label='First Name',  # ช่องสำหรับชื่อจริง
        validators=[DataRequired(), Length(min=1, max=50)]  # ตรวจสอบว่าต้องกรอกข้อมูลและความยาวอยู่ในช่วง 1-50 ตัวอักษร
    )
    lname = StringField(
        label='Last Name',  # ช่องสำหรับนามสกุล
        validators=[DataRequired(), Length(min=1, max=50)]  # ตรวจสอบว่าต้องกรอกข้อมูลและความยาวอยู่ในช่วง 1-50 ตัวอักษร
    )
    password = PasswordField(
        label='Password',  # ช่องสำหรับรหัสผ่าน
        validators=[DataRequired()]  # ตรวจสอบว่าต้องกรอกข้อมูล
    )
    confirm_password = PasswordField(
        label='Confirm Password',  # ช่องสำหรับยืนยันรหัสผ่าน
        validators=[DataRequired(), EqualTo('password')]  # ตรวจสอบว่าต้องกรอกข้อมูลและยืนยันรหัสผ่านให้ตรงกัน
    )
    avatar = FileField(
        label='Profile Picture',  # ช่องสำหรับรูปโปรไฟล์
        validators=[FileAllowed(['jpg', 'png'], 'Images only!')]  # ตรวจสอบว่าเป็นไฟล์ภาพ JPG หรือ PNG เท่านั้น
    )
    submit = SubmitField(label='Register')  # ปุ่ม "ลงทะเบียน"

    def validate_username(self, username):
        user = db.session.scalar(db.select(User).where(User.username == username.data))  # ตรวจสอบชื่อผู้ใช้ในฐานข้อมูล
        if user:
            raise ValidationError('The username is taken. Please choose a different one!')  # แจ้งเตือนหากชื่อผู้ใช้ถูกใช้แล้ว

    def validate_email(self, email):
        user = db.session.scalar(db.select(User).where(User.email == email.data))  # ตรวจสอบอีเมลในฐานข้อมูล
        if user:
            raise ValidationError('The email is taken. Please choose a different one!')  # แจ้งเตือนหากอีเมลถูกใช้แล้ว

class UpdateProfileForm(FlaskForm):
    username = StringField(
        label='Username',  # ช่องสำหรับชื่อผู้ใช้
        validators=[DataRequired(), Length(min=4, max=50)]  # ตรวจสอบว่าต้องกรอกข้อมูลและความยาวอยู่ในช่วง 4-50 ตัวอักษร
    )
    email = EmailField(
        label='Email Address',  # ช่องสำหรับอีเมล
        validators=[DataRequired(), Email()]  # ตรวจสอบว่าต้องกรอกข้อมูลและเป็นอีเมลที่ถูกต้อง
    )
    fname = StringField(
        label='First Name',  # ช่องสำหรับชื่อจริง
        validators=[DataRequired(), Length(min=1, max=50)]  # ตรวจสอบว่าต้องกรอกข้อมูลและความยาวอยู่ในช่วง 1-50 ตัวอักษร
    )
    lname = StringField(
        label='Last Name',  # ช่องสำหรับนามสกุล
        validators=[DataRequired(), Length(min=1, max=50)]  # ตรวจสอบว่าต้องกรอกข้อมูลและความยาวอยู่ในช่วง 1-50 ตัวอักษร
    )
    password = PasswordField(
        label='Password',  # ช่องสำหรับรหัสผ่าน
        validators=[Length(min=6)],  # ทำให้รหัสผ่านเป็นตัวเลือกและกำหนดความยาวขั้นต่ำ
        render_kw={"placeholder": "Leave blank to keep current password"}  # เพิ่ม placeholder เพื่อแนะนำให้ผู้ใช้ทราบว่าหากไม่กรอกรหัสผ่านจะใช้รหัสผ่านเดิม
    )
    confirm_password = PasswordField(
        label='Confirm Password',  # ช่องสำหรับยืนยันรหัสผ่าน
        validators=[EqualTo('password')]  # ทำให้การยืนยันรหัสผ่านเป็นตัวเลือก
    )
    avatar = FileField(
        label='Profile Picture',  # ช่องสำหรับรูปโปรไฟล์
        validators=[FileAllowed(['jpg', 'png'], 'Images only!')]  # ตรวจสอบว่าเป็นไฟล์ภาพ JPG หรือ PNG เท่านั้น
    )
    submit = SubmitField(label='Update')  # ปุ่ม "อัปเดต"

class CTForm(FlaskForm):
    coperatename = StringField(
        label='Cooperative Name',  # ช่องสำหรับชื่อสถานที่ฝึกงาน
        validators=[DataRequired(), Length(min=1, max=50)]  # ตรวจสอบว่าต้องกรอกข้อมูลและความยาวอยู่ในช่วง 1-50 ตัวอักษร
    )
    contact = StringField(
        label='Contact Information',  # ช่องสำหรับข้อมูลการติดต่อ
        validators=[DataRequired(), Length(min=1, max=50)]  # ตรวจสอบว่าต้องกรอกข้อมูลและความยาวอยู่ในช่วง 1-50 ตัวอักษร
    )
    superviser = StringField(
        label='Supervisor Name',  # ช่องสำหรับชื่อผู้ควบคุม
        validators=[DataRequired(), Length(min=1, max=100)]  # ตรวจสอบว่าต้องกรอกข้อมูลและความยาวอยู่ในช่วง 1-100 ตัวอักษร
    )
    detail = StringField(
        label='Details',  # ช่องสำหรับรายละเอียด
        validators=[Length(max=100)]  # ตรวจสอบความยาวสูงสุด 100 ตัวอักษร
    )
    submit = SubmitField(label='Add Record')  # ปุ่ม "เพิ่มข้อมูล"

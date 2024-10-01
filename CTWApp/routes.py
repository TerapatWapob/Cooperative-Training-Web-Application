from flask import Blueprint, render_template, redirect, url_for, flash, request  # นำเข้าโมดูลที่ใช้ใน Flask
from flask_login import login_user, current_user, login_required, logout_user  # นำเข้าโมดูลสำหรับการจัดการผู้ใช้
from werkzeug.utils import secure_filename  # ใช้สำหรับการจัดการไฟล์
from CTWApp import db, bcrypt, app  # นำเข้า db, bcrypt, และ app จาก CTWApp
from .forms import LoginForm, RegisterForm, UpdateProfileForm, CTForm  # นำเข้าแบบฟอร์มที่ใช้
from .models import User, CT  # นำเข้าโมเดล User และ CT
import os  # นำเข้าโมดูลสำหรับจัดการไฟล์และเส้นทาง

flask = Blueprint('flask', __name__)  # สร้าง Blueprint สำหรับการจัดการเส้นทาง

@flask.route('/')
def home():
    cts = CT.query.all()  # ดึงข้อมูล CT ทั้งหมด
    return render_template('index.html', title='CTWApp - Home', cts=cts)  # แสดงหน้าโฮมเพจ

@flask.route('/user/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('flask.manage_ct'))  # ถ้าผู้ใช้ล็อกอินแล้วให้เปลี่ยนเส้นทางไปที่หน้า manage_ct

    form = LoginForm()  # สร้างออบเจกต์ของ LoginForm
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()  # ค้นหาผู้ใช้ตามชื่อ
        if user and bcrypt.check_password_hash(user.password, form.password.data):  # ตรวจสอบรหัสผ่าน
            login_user(user, remember=form.remember.data)  # ล็อกอินผู้ใช้
            flash('Login successful!', 'success')  # แสดงข้อความล็อกอินสำเร็จ
            return redirect(url_for('flask.manage_ct'))  # เปลี่ยนเส้นทางไปที่ manage_ct
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')  # แสดงข้อความล็อกอินไม่สำเร็จ

    return render_template('user/login.html', title='Login', form=form)  # แสดงฟอร์มล็อกอิน

@flask.route('/user/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('flask.account'))  # ถ้าผู้ใช้ล็อกอินแล้วให้เปลี่ยนเส้นทางไปที่หน้า account

    form = RegisterForm()  # สร้างออบเจกต์ของ RegisterForm
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # สร้างรหัสผ่านที่เข้ารหัส
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            fname=form.fname.data,
            lname=form.lname.data
        )
        db.session.add(user)  # เพิ่มผู้ใช้ใหม่ในฐานข้อมูล
        db.session.commit()  # บันทึกการเปลี่ยนแปลง
        flash('Your account has been created!', 'success')  # แสดงข้อความบัญชีถูกสร้างสำเร็จ
        return redirect(url_for('flask.login'))  # เปลี่ยนเส้นทางไปที่หน้า login

    return render_template('user/register.html', title='Register', form=form)  # แสดงฟอร์มการลงทะเบียน

@flask.route('/user/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateProfileForm()  # สร้างออบเจกต์ของ UpdateProfileForm
    if form.validate_on_submit():
        # อัปเดตข้อมูลของผู้ใช้
        current_user.fname = form.fname.data
        current_user.lname = form.lname.data

        # จัดการการอัปโหลดไฟล์
        if form.avatar.data:
            avatar = form.avatar.data
            filename = secure_filename(avatar.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            avatar.save(file_path)
            current_user.avatar = filename

        # อัปเดตรหัสผ่านถ้ามีการระบุ
        if form.password.data:
            if form.confirm_password.data == form.password.data:  # ตรวจสอบว่ารหัสผ่านยืนยันตรงกัน
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                current_user.password = hashed_password
            else:
                flash('Passwords do not match!', 'danger')  # แสดงข้อความรหัสผ่านไม่ตรงกัน
                return redirect(url_for('flask.account'))  # เปลี่ยนเส้นทางไปที่หน้า account

        db.session.commit()  # บันทึกการเปลี่ยนแปลง
        flash('Your account has been updated!', 'success')  # แสดงข้อความบัญชีถูกอัปเดตสำเร็จ
        return redirect(url_for('flask.account'))  # เปลี่ยนเส้นทางไปที่หน้า account

    # เตรียมข้อมูลในฟอร์มด้วยข้อมูลผู้ใช้ปัจจุบัน
    form.username.data = current_user.username
    form.email.data = current_user.email
    form.fname.data = current_user.fname
    form.lname.data = current_user.lname

    return render_template('user/account.html', title='Profile Detail', form=form)  # แสดงข้อมูลโปรไฟล์

@flask.route('/user/logout')
@login_required
def logout():
    logout_user()  # ล็อกเอาท์ผู้ใช้
    flash('You have been logged out.', 'info')  # แสดงข้อความล็อกเอาท์
    return redirect(url_for('flask.home'))  # เปลี่ยนเส้นทางไปที่หน้าโฮม

@flask.route('/ct', methods=['GET', 'POST'])
@login_required
def manage_ct():
    form = CTForm()  # สร้างออบเจกต์ของ CTForm
    if form.validate_on_submit():
        # สร้างข้อมูล CT ใหม่
        new_ct = CT(
            coperatename=form.coperatename.data,
            contact=form.contact.data,
            superviser=form.superviser.data,
            detail=form.detail.data,
            user_id=current_user.id  # เชื่อมโยงข้อมูล CT กับผู้ใช้ปัจจุบัน
        )
        db.session.add(new_ct)  # เพิ่มข้อมูล CT ใหม่ในฐานข้อมูล
        db.session.commit()  # บันทึกการเปลี่ยนแปลง
        flash('CT record has been added!', 'success')  # แสดงข้อความข้อมูล CT ถูกเพิ่ม
        return redirect(url_for('flask.manage_ct'))  # เปลี่ยนเส้นทางไปที่ manage_ct

    # ดึงข้อมูล CT ทั้งหมดสำหรับผู้ใช้ปัจจุบัน
    cts = CT.query.filter_by(user_id=current_user.id).all()

    return render_template('CTW/index.html', title='Manage CT Records', form=form, cts=cts)  # แสดงข้อมูล CT

@flask.route('/add_record', methods=['GET', 'POST'])
@login_required
def add_record():
    form = CTForm()  # สร้างออบเจกต์ของ CTForm

    if form.validate_on_submit():
        new_ct = CT(
            coperatename=form.coperatename.data,
            contact=form.contact.data,
            superviser=form.superviser.data,
            detail=form.detail.data,
            user_id=current_user.id
        )
        db.session.add(new_ct)  # เพิ่มข้อมูล CT ใหม่ในฐานข้อมูล
        db.session.commit()  # บันทึกการเปลี่ยนแปลง
        flash('New CT record has been added!', 'success')  # แสดงข้อความข้อมูล CT ใหม่ถูกเพิ่ม
        return redirect(url_for('flask.manage_ct'))  # เปลี่ยนเส้นทางไปที่ manage_ct

    return render_template('addrecord.html', title='Add New Record', form=form)  # แสดงฟอร์มเพิ่มข้อมูลใหม่

@flask.route('/delete_ct/<int:ct_id>', methods=['POST'])
@login_required
def delete_record(ct_id):
    # ดึงข้อมูล CT โดยใช้ ID
    ct = CT.query.get_or_404(ct_id)

    # ตรวจสอบว่าผู้ใช้ปัจจุบันเป็นเจ้าของข้อมูล
    if ct.user_id != current_user.id:
        flash('You do not have permission to delete this record.', 'danger')  # แสดงข้อความไม่มีสิทธิ์ลบ
        return redirect(url_for('flask.home'))  # เปลี่ยนเส้นทางไปที่หน้าโฮม

    # ลบข้อมูล CT ออกจากฐานข้อมูล
    db.session.delete(ct)
    db.session.commit()  # บันทึกการเปลี่ยนแปลง

    flash('CT record has been deleted!', 'success')  # แสดงข้อความข้อมูล CT ถูกลบ
    return redirect(url_for('flask.manage_ct'))  # เปลี่ยนเส้นทางไปที่ manage_ct

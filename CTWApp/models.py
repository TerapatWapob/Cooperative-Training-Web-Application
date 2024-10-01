from flask_sqlalchemy import SQLAlchemy  # นำเข้า SQLAlchemy สำหรับจัดการฐานข้อมูล
from flask_login import UserMixin  # นำเข้า UserMixin สำหรับการจัดการผู้ใช้
from sqlalchemy import Integer, String, Boolean, ForeignKey  # นำเข้าชนิดข้อมูลและคีย์ต่าง ๆ
from sqlalchemy.orm import relationship, mapped_column, Mapped, WriteOnlyMapped  # นำเข้าฟังก์ชันและคลาสสำหรับการแมพข้อมูล
from CTWApp import db  # นำเข้า db จาก CTWApp

class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # กำหนด id เป็น Primary Key และชนิดข้อมูลเป็น Integer
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)  # กำหนด username เป็น String, ต้องมีค่าและต้องไม่ซ้ำ
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)  # กำหนด email เป็น String, ต้องมีค่าและต้องไม่ซ้ำ
    password: Mapped[str] = mapped_column(String(50), nullable=False)  # กำหนด password เป็น String, ต้องมีค่า
    fname: Mapped[str] = mapped_column(String(50), nullable=False)  # กำหนด fname เป็น String, ต้องมีค่า
    lname: Mapped[str] = mapped_column(String(50), nullable=False)  # กำหนด lname เป็น String, ต้องมีค่า

    # กำหนดความสัมพันธ์กับ CT
    cts: WriteOnlyMapped['CT'] = relationship('CT', back_populates='user')  # ความสัมพันธ์แบบ one-to-many กับ CT

    def __repr__(self):
        return f'<User: {self.username}>'  # แสดงตัวแทนของ User

class CT(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # กำหนด id เป็น Primary Key และชนิดข้อมูลเป็น Integer
    coperatename: Mapped[str] = mapped_column(String(50), nullable=False)  # กำหนด coperatename เป็น String, ต้องมีค่า
    contact: Mapped[str] = mapped_column(String(50), nullable=False)  # กำหนด contact เป็น String, ต้องมีค่า
    superviser: Mapped[str] = mapped_column(String(100), nullable=False)  # กำหนด superviser เป็น String, ต้องมีค่า
    detail: Mapped[str] = mapped_column(String(1000), nullable=True)  # กำหนด detail เป็น String, อาจมีค่า

    # คีย์ต่างที่เชื่อมโยงกับ User
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))  # เชื่อมโยง user_id กับ Primary Key ของ User
    user: Mapped[User] = relationship('User', back_populates='cts')  # ความสัมพันธ์แบบ many-to-one กับ User

    def __repr__(self):
        return f'<CT: {self.coperatename}>'  # แสดงตัวแทนของ CT

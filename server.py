from CTWApp import app, db  # นำเข้า app และ db จาก CTWApp

with app.app_context():  # เปิดใช้งาน application context
    db.create_all()  # สร้างตารางฐานข้อมูลทั้งหมด

if __name__ == "__main__":  # ตรวจสอบว่ารันไฟล์นี้เป็นไฟล์หลัก
    app.run(debug=False)  # เรียกใช้งานแอพในโหมด debug

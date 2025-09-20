รัน run.py

user1
pass1

จุดเริ่มของโปรแกรม
  run.py
    เป็น entry point ของระบบ
    ทำหน้าที่สร้างอินสแตนซ์ MainController
    เรียก mainloop() ของ Tkinter เพื่อรันหน้าต่างหลัก

Controller
  app/controllers/main_controller.py
    สร้างโมเดลทั้งหมด (Project, User, Pledge, Reward)
    จัดการ dictionary ของ frames ที่เป็นวิวทั้งหมด
    มีหน้าที่ควบคุมการสลับหน้าและโหลดข้อมูลก่อนแสดง
    มีเมทอดช่วย เช่น:
      การแสดงรายละเอียดโครงการ
      การคำนวณสถิติผู้ใช้

Models
  ProjectModel / UserModel / PledgeModel / RewardModel
    เชื่อมต่อกับ CSVStore เพื่ออ่าน/เขียนข้อมูล CSV
    ใช้ dataclass ห่อหุ้มโครงสร้างข้อมูล
    มีเมทอดตามหน้าที่ เช่น:
      ProjectModel  อัปเดตยอดระดมทุน
      UserModel  ตรวจสอบการล็อกอิน
      PledgeModel  จัดการคำมั่น, อ้างถึง ProjectModel และ RewardModel เพื่อตรวจสอบ/อัปเดต
      RewardModel  ลดโควตาของรางวัลเมื่อถูกเลือก

Views
  BaseView
    เป็น Tkinter Frame พื้นฐาน
    มีเมทอด show() สำหรับยกหน้าปัจจุบันขึ้นมา
    MainMenuView
    เมนูเรียบง่ายสำหรับโครงสร้างหลัก
  LoginView
    แบบฟอร์มกรอกข้อมูลผู้ใช้
    do_login เรียก UserModel.check_login ถ้าสำเร็จ  controller บันทึกผู้ใช้แล้วสลับไปยังเมนูผู้ใช้
  ReadView
    ศูนย์กลางสำหรับการสำรวจโครงการ
    มีเครื่องมือค้นหา/กรอง/จัดเรียง
    ปุ่มเปิดรายละเอียด (go_to_detail)
    ปุ่มสนับสนุน (on_support)  เปิดฟอร์มย่อย เรียก PledgeModel.add_pledge และรีเฟรชตาราง
  DetailView
    แสดงรายละเอียดโครงการ
    ใช้ load_project ดึงข้อมูล
    มีปุ่มย้อนกลับ (อ้างถึงหน้าก่อนหน้าใน MainController)
  UserMenuView
    แสดงคำมั่นของผู้ใช้จาก show_user_pledges
    มีปุ่มไปยังหน้ารายละเอียด, หน้าโครงการ, หน้า stats
  UserStatsView
    แสดงข้อมูลสถิติ (จำนวนคำมั่น, ยอดรวม, จำนวนถูกปฏิเสธ)
    ใช้ set_stats ที่รับค่าจาก MainController.show_user_stats

เส้นทางการทำงานหลัก (Routes / Actions)
  1.	Login  UserMenu
    กรอกข้อมูลใน LoginView
    ตรวจสอบผ่าน UserModel
    ถ้าสำเร็จ  ไปเมนูผู้ใช้
  2.	UserMenu
    เลือกดูคำมั่น/โครงการ/สถิติ
  3.	ReadView
    ค้นหา/กรองโครงการ
    สนับสนุน  บันทึกคำมั่น + อัปเดตยอดโครงการ/รางวัล
  4.	DetailView
    ดูรายละเอียดโครงการแบบเต็ม
  5.	UserStatsView
    แสดงสถิติการสนับสนุน

MainController = ตัวกลาง
  เชื่อม View ↔ Model
  จัดการการสลับหน้าและส่งข้อมูล
  Models = ชั้นข้อมูล
  อ่าน/เขียนจาก CSV และอัปเดตสถานะ
  Views = อินเทอร์เฟซผู้ใช้
  Tkinter UI ที่โต้ตอบกับผู้ใช้
  การสื่อสาร
  View ส่ง action → Controller → Model
Model อัปเดตข้อมูล → Controller ดึงข้อมูลกลับ → View แสดงผล


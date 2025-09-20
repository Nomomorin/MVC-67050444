# MVC Tkinter Crowdfunding App

โปรแกรมตัวอย่างระบบ **Crowdfunding** ที่สร้างด้วย **Python + Tkinter** โดยใช้สถาปัตยกรรม **MVC (Model-View-Controller)**  
จัดเก็บข้อมูลด้วย **CSV** และใช้ **dataclass** จัดการโครงสร้างข้อมูล




Username: user1
Password: pass1


## จุดเริ่มของโปรแกรม

### `run.py`
- เป็น entry point ของระบบ  
- สร้างอินสแตนซ์ `MainController`  
- เรียก `mainloop()` ของ Tkinter เพื่อรันหน้าต่างหลัก  

---

## Controller

### `main_controller.py`
- สร้างโมเดลทั้งหมด (Project, User, Pledge, Reward)  
- จัดการ dictionary ของ frames ที่เป็นวิวทั้งหมด  
- ควบคุมการสลับหน้าและโหลดข้อมูลก่อนแสดง  
- มีเมทอดช่วย เช่น:
  - แสดงรายละเอียดโครงการ  
  - คำนวณสถิติผู้ใช้  

---

## Models

- **ProjectModel**  
  อัปเดตยอดระดมทุน  

- **UserModel**  
  ตรวจสอบการล็อกอิน  

- **PledgeModel**  
  จัดการคำมั่น (pledge)  
  อ้างถึง `ProjectModel` และ `RewardModel` เพื่อตรวจสอบและอัปเดตข้อมูล  

- **RewardModel**  
  ลดโควตาของรางวัลเมื่อถูกเลือก  

- **CSVStore**  
  บริการกลางสำหรับอ่าน/เขียน CSV  

> ทุกโมเดลห่อหุ้มข้อมูลด้วย **dataclass** เพื่อความเป็นระเบียบ  

---

## Views

- **BaseView**  
  Tkinter Frame พื้นฐาน มีเมทอด `show()` สำหรับแสดงหน้า  

- **LoginView**  
  ฟอร์มล็อกอิน → เรียก `UserModel.check_login`  

- **MainMenuView**  
  เมนูหลักแบบเรียบง่าย  

- **ReadView**  
  ศูนย์กลางสำหรับการสำรวจโครงการ  
  - ค้นหา/กรอง/จัดเรียง  
  - สนับสนุนโครงการ (`PledgeModel.add_pledge`)  

- **DetailView**  
  แสดงรายละเอียดโครงการ (มีปุ่มย้อนกลับ)  

- **UserMenuView**  
  แสดงคำมั่นของผู้ใช้  
  - นำทางไปยังโครงการ / รายละเอียด / สถิติ  

- **UserStatsView**  
  แสดงข้อมูลสถิติ เช่น:
  - จำนวนคำมั่น  
  - ยอดรวม  
  - การถูกปฏิเสธ  

---

## เส้นทางการทำงานหลัก (Routes / Actions)

1. **Login → UserMenu**  
   - กรอกข้อมูลใน LoginView  
   - ตรวจสอบผ่าน UserModel  
   - ถ้าสำเร็จ → ไปเมนูผู้ใช้  

2. **UserMenu**  
   - เลือกดูคำมั่น / โครงการ / สถิติ  

3. **ReadView**  
   - ค้นหา/กรองโครงการ  
   - สนับสนุน → บันทึกคำมั่น + อัปเดตยอดโครงการ/รางวัล  

4. **DetailView**  
   - ดูรายละเอียดโครงการแบบเต็ม  

5. **UserStatsView**  
   - แสดงสถิติการสนับสนุน  

---

## ภาพรวมการสื่อสาร MVC

- **MainController = ตัวกลาง**  
  - เชื่อม **View ↔ Model**  
  - จัดการการสลับหน้าและส่งข้อมูล  

- **Models = ชั้นข้อมูล**  
  - อ่าน/เขียนจาก CSV และอัปเดตสถานะ  

- **Views = อินเทอร์เฟซผู้ใช้**  
  - Tkinter UI ที่โต้ตอบกับผู้ใช้  

- **การไหลของข้อมูล**  
  - View ส่ง action → Controller → Model  
  - Model อัปเดตข้อมูล → Controller ดึงข้อมูลกลับ → View แสดงผล  



.



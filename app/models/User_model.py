from dataclasses import dataclass
from typing import List, Optional
from pathlib import Path
from app.services.csv_store import CSVStore
from datetime import date

@dataclass
class User:
    id: int
    username: str
    password: str
    name: str
    reject_count: int

class UserModel:
    #-- init --- สร้างไฟล์ csv สำหรับเก็บข้อมูล
    def __init__(self, csv_path: Path = Path("data/user.csv")):
        self.store = CSVStore(csv_path, fieldnames=["id", "username", "password", "name"])

    #อ่านข้อมูลทั้งหมดจาก csv
    def list_items(self) -> List[User]:
        rows = self.store.read_all()
        return [User(int(r["id"]), r["username"], r["password"], r["name"])  for r in rows]

    # ตรวจสอบการ login
    def check_login(self, username: str, password: str) -> bool:
        rows = self.store.read_all()
        for r in rows:
            if r["username"] == username and r["password"] == password:
                return r
        return None
    
    # เพิ่ม reject count ของ user
    def increment_reject(self, user_id: int):
        rows = self.store.read_all()
        for r in rows:
            if int(r["id"]) == user_id:
                r["reject_count"] = str(int(r.get("reject_count","0")) + 1)
                break
        self.store.write_all(rows)
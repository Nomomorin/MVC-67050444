from dataclasses import dataclass
from typing import List, Optional
from pathlib import Path
from app.services.csv_store import CSVStore
from datetime import datetime

@dataclass
class Project:
    id: int
    name: str
    fundraising_target: int
    fundraising_current: int
    deadline: datetime

class ProjectModel:
    #-- init --- สร้างไฟล์ csv สำหรับเก็บข้อมูล
    def __init__(self, csv_path: Path = Path("data/project.csv")):
        self.store = CSVStore(csv_path, fieldnames=["id", "name", "fundraising_target", "fundraising_current", "deadline"])

    #อ่านข้อมูลทั้งหมดจาก csv
    def list_items(self) -> List[Project]:
        rows = self.store.read_all()
        return [Project(int(r["id"]), r["name"], int(r["fundraising_target"]), int(r["fundraising_current"]), datetime.strptime(r["deadline"], "%Y-%m-%d").date())  for r in rows]

    # แก้ไขข้อมูลใหม่ เงินสนับสนุนปัจจุบัน
    def update_current_amount(self, project_id: int, amount: int):
        """เพิ่มยอด fundraising_current ของโครงการตาม project_id"""
        rows = self.store.read_all()
        updated = False
        for r in rows:
            if int(r["id"]) == int(project_id):
                r["fundraising_current"] = str(int(r["fundraising_current"]) + amount)
                updated = True
                break
        if updated:
            self.store.write_all(rows)
        else:
            raise ValueError(f"Project with id={project_id} not found")

"""     def add_item(self, name: str, fundraising_target: int, fundraising_current : int, deadline : datetime) -> None:
        rows = self.store.read_all()
        new_id = max([int(r["id"]) for r in rows], default=0) + 1
        self.store.append({"id": str(new_id), "name": name.strip(), "fundraising_target": str(fundraising_target), "fundraising_current": str(fundraising_current), "deadline": str(deadline)})

    def update_item(self, item_id: int, name: str, fundraising_target: int, fundraising_current : int, deadline : datetime) -> bool:
        rows = self.store.read_all()
        found = False
        for r in rows:
            if int(r["id"]) == item_id:
                r["name"], r["fundraising_target"], r["fundraising_current"], r["deadline"]  = name.strip(), int(fundraising_target), int(fundraising_current), str(deadline)
                found = True
        if found:
            self.store.write_all(rows)
        return found

    def delete_item(self, item_id: int) -> bool:
        rows = self.store.read_all()
        new_rows = [r for r in rows if int(r["id"]) != item_id]
        if len(new_rows) == len(rows):
            return False
        self.store.write_all(new_rows)
        return True """

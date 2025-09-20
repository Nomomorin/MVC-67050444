from dataclasses import dataclass
from typing import List, Optional
from pathlib import Path
from app.services.csv_store import CSVStore
from datetime import date

@dataclass
class RewardTier:
    id: int
    name: str
    minimum_support: int
    quota_remaining: int
    project_id: int

class RewardTierModel:
    #-- init --- สร้างไฟล์ csv สำหรับเก็บข้อมูล
    def __init__(self, csv_path: Path = Path("data/items.csv")):
        self.store = CSVStore(csv_path, fieldnames=["id", "name", "minimum_support", "quota_remaining", "project_id"])

    #อ่านข้อมูลทั้งหมดจาก csv
    def list_items(self) -> List[RewardTier]:
        rows = self.store.read_all()
        return [RewardTier(int(r["id"]), r["name"], int(r["minimum_support"]), int(r["quota_remaining"]), int(r["project_id"]))  for r in rows]

    # เพิ่มข้อมูลใหม่
    def add_item(self, name: str, minimum_support: int, quota_remaining : int, project_id : int) -> None:
        rows = self.store.read_all()
        new_id = max([int(r["id"]) for r in rows], default=0) + 1
        self.store.append({"id": str(new_id), "name": name.strip(), "minimum_support": str(minimum_support), "quota_remaining": str(quota_remaining), "Deadline": str(project_id)})

    # แก้ไขข้อมูล
    def update_item(self, item_id: int, name: str, minimum_support: int, quota_remaining : int, project_id : int) -> bool:
        rows = self.store.read_all()
        found = False
        for r in rows:
            if int(r["id"]) == item_id:
                r["name"], r["minimum_support"], r["quota_remaining"], r["project_id"]  = name.strip(), int(minimum_support), int(quota_remaining), str(project_id)
                found = True
        if found:
            self.store.write_all(rows)
        return found

    # ลบข้อมูล
    def delete_item(self, item_id: int) -> bool:
        rows = self.store.read_all()
        new_rows = [r for r in rows if int(r["id"]) != item_id]
        if len(new_rows) == len(rows):
            return False
        self.store.write_all(new_rows)
        return True

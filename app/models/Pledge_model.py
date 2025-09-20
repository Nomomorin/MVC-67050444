from dataclasses import dataclass
from typing import List, Optional
from pathlib import Path
from app.services.csv_store import CSVStore
from datetime import datetime

@dataclass
class Pledge:
    id: int
    user_id : int
    project_id: str
    amount: int
    timestamp: int
    reward_level: int

class PledgeModel:
    #-- init --- สร้างไฟล์ csv สำหรับเก็บข้อมูล
    def __init__(self, csv_path: Path = Path("data/pledges.csv"), project_model=None, reward_model=None, user_model=None):
        self.store = CSVStore(csv_path, fieldnames=["id","user_id","project_id","amount","timestamp","reward_level"])
        self.project_model = project_model
        self.reward_model = reward_model
        self.user_model = user_model
    #อ่านข้อมูลทั้งหมดจาก csv
    def list_items(self) -> List[Pledge]:
        rows = self.store.read_all()
        return [Pledge(int(r["id"]), r["name"], int(r["user_id"]), int(r["project_id"]), int(r["amouse"]), datetime(r["timestamp"]), int(r["reward_level"]))  for r in rows]
    
    # เพิ่มข้อมูลใหม่
    def add_item(self, user_id: str, project_id: int, amount : int, timestamp : int, reward_level) -> None:
        rows = self.store.read_all()
        new_id = max([int(r["id"]) for r in rows], default=0) + 1
        self.store.append({"id": str(new_id), "ีuser_id": user_id.strip(), "project_id": str(project_id), "amount": str(amount), "timestamp": str(timestamp), "reward_level": str(reward_level)})

    # แก้ไขข้อมูล
    def update_item(self, item_id: int, user_id: str, project_id: int, amount : datetime, timestamp : int, reward_level) -> bool:
        rows = self.store.read_all()
        found = False
        for r in rows:
            if int(r["id"]) == item_id:
                r["user_id"], r["project_id"], r["amount"], r["timestamp"], r["reward_level"]  = user_id.strip(), int(project_id), int(amount), str(timestamp), str(reward_level)
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
    
    # เอาข้อมูลทั้งหมดของ user_id ที่ระบุ
    def list_items_by_user_id(self, user_id: int) -> List[Pledge]:
        rows = self.store.read_all()
        pledges = [
            Pledge(
                id=int(r["id"]),
                user_id=int(r["user_id"].strip()),    
                project_id=int(r["project_id"]),
                amount=int(r["amount"]),
                timestamp=datetime.fromisoformat(r["timestamp"]),
                reward_level=r["reward_level"].strip() if r["reward_level"] else None
            )
            for r in rows
        ]

        if user_id is not None:
            pledges = [p for p in pledges if int(p.user_id) == int(user_id)]

        return pledges
    
    # ข้อมูล pledge ใหม่
    def add_pledge(self, user_id: int, project_id: int, amount: int, reward_level: Optional[int] = None):
        # ตรวจสอบ reward
        if reward_level is not None:
            reward = self.reward_model.get_by_id(reward_level)
            if reward is None:
                self.user_model.increment_reject(user_id)
                raise ValueError("Reward not found")
            if amount < reward.minimum_support:
                self.user_model.increment_reject(user_id)
                raise ValueError("Amount is less than reward minimum")
            if reward.quota_remaining <= 0:
                self.user_model.increment_reject(user_id)
                raise ValueError("Reward quota exceeded")

        # สร้าง pledge ใหม่
        rows = self.store.read_all()
        new_id = max([int(r["id"]) for r in rows], default=0) + 1
        self.store.append({
            "id": str(new_id),
            "user_id": str(user_id),
            "project_id": str(project_id),
            "amount": str(amount),
            "timestamp": datetime.now().isoformat(),
            "reward_level": str(reward_level) if reward_level else ""
        })

        # อัปเดต project
        self.project_model.update_current_amount(project_id, amount)

        # ลด quota ของ reward
        if reward_level is not None:
            self.reward_model.decrement_quota(reward_level)
    # ลด quota ของ reward
    def decrement_quota(self, reward_id: int):
        rows = self.store.read_all()
        for r in rows:
            if int(r["id"]) == reward_id:
                r["quota_remaining"] = str(int(r["quota_remaining"]) - 1)
                break
        self.store.write_all(rows)

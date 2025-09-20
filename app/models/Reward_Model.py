from dataclasses import dataclass
from typing import List, Optional
from app.services.csv_store import CSVStore
from pathlib import Path

@dataclass
class RewardTier:
    id: int
    name: str
    minimum_support: int
    quota_remaining: int
    project_id: int

class RewardModel:
    #-- init --- สร้างไฟล์ csv สำหรับเก็บข้อมูล
    def __init__(self, csv_path: Path = Path("data/rewards.csv")):
        self.store = CSVStore(csv_path, fieldnames=["id","name","minimum_support","quota_remaining","project_id"])

      #อ่านข้อมูลจาก csv จาก id 
    def get_by_id(self, reward_id: int) -> Optional[RewardTier]:
        rows = self.store.read_all()
        for r in rows:
            if int(r["id"]) == reward_id:
                return RewardTier(
                    int(r["id"]),
                    r["name"],
                    int(r["minimum_support"]),
                    int(r["quota_remaining"]),
                    int(r["project_id"])
                )
        return None
    
      # ลด quota ของ reward
    def decrement_quota(self, reward_id: int):
        rows = self.store.read_all()
        for r in rows:
            if int(r["id"]) == reward_id:
                r["quota_remaining"] = str(int(r["quota_remaining"]) - 1)
                break
        self.store.write_all(rows)

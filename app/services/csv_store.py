from pathlib import Path
import csv
from typing import List, Dict

class CSVStore:
    #-- init --- สร้างไฟล์ csv สำหรับเก็บข้อมูล
    def __init__(self, file_path: Path, fieldnames: list[str]):
        self.file_path = Path(file_path)
        self.fieldnames = fieldnames
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            with self.file_path.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()

    #อ่านข้อมูลทั้งหมดจาก csv
    def read_all(self) -> List[Dict[str, str]]:
        with self.file_path.open("r", newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    # เพิ่มข้อมูลใหม่
    def append(self, row: Dict[str, str]) -> None:
        with self.file_path.open("a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writerow(row)
    # แก้ไขข้อมูล
    def write_all(self, rows: List[Dict[str, str]]) -> None:
        with self.file_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(rows)
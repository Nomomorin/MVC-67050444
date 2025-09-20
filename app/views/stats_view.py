import tkinter as tk
from tkinter import ttk
from .base_view import BaseView

class UserStatsView(BaseView):
    #หน้าแสดงสถิติการสนับสนุนของ user
    def __init__(self, master, controller):
        super().__init__(master, controller)

        ttk.Label(self, text="สถิติการสนับสนุนของฉัน", font=("Arial", 18)).pack(pady=12)

        self.success_var = tk.StringVar()
        self.reject_var = tk.StringVar()
        self.total_amount_var = tk.StringVar()

        frame = ttk.Frame(self)
        frame.pack(pady=10, fill="x", padx=12)

        ttk.Label(frame, text="จำนวนการสนับสนุนสำเร็จ:").grid(row=0, column=0, sticky="w", pady=4)
        ttk.Label(frame, textvariable=self.success_var, font=("Arial", 14)).grid(row=0, column=1, sticky="w")

        ttk.Label(frame, text="จำนวนที่ถูกปฏิเสธ:").grid(row=1, column=0, sticky="w", pady=4)
        ttk.Label(frame, textvariable=self.reject_var, font=("Arial", 14)).grid(row=1, column=1, sticky="w")

        ttk.Label(frame, text="ยอดรวมสนับสนุนทั้งหมด:").grid(row=2, column=0, sticky="w", pady=4)
        ttk.Label(frame, textvariable=self.total_amount_var, font=("Arial", 14)).grid(row=2, column=1, sticky="w")

        ttk.Button(self, text="Back", command=lambda: controller.show_page("usermenu")).pack(pady=12)

    def set_stats(self, success_count, reject_count, total_amount):
        self.success_var.set(f"{success_count} ครั้ง")
        self.reject_var.set(f"{reject_count} ครั้ง")
        self.total_amount_var.set(f"{total_amount} บาท")

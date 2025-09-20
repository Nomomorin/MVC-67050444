# app/views/stats_view.py
import tkinter as tk
from tkinter import ttk
from .base_view import BaseView

class StatsView(BaseView):
    #หน้าแสดงสถิติ
    def __init__(self, master, controller):
        super().__init__(master, controller)

        ttk.Label(self, text="สรุปสถิติ", font=("Arial", 18)).pack(pady=12)

        self.success_var = tk.StringVar()
        self.reject_var = tk.StringVar()

        ttk.Label(self, text="การสนับสนุนที่สำเร็จ:").pack(anchor="w", padx=12, pady=4)
        ttk.Label(self, textvariable=self.success_var, font=("Arial", 14)).pack(anchor="w", padx=24)

        ttk.Label(self, text="การสนับสนุนที่ถูกปฏิเสธ:").pack(anchor="w", padx=12, pady=4)
        ttk.Label(self, textvariable=self.reject_var, font=("Arial", 14)).pack(anchor="w", padx=24)

        ttk.Button(self, text="Back", command=lambda: controller.show_page("menu")).pack(pady=12)

    def set_stats(self, success_count, reject_count):
        self.success_var.set(f"{success_count} ครั้ง")
        self.reject_var.set(f"{reject_count} ครั้ง")

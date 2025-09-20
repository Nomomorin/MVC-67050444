import tkinter as tk
from tkinter import ttk
from .base_view import BaseView

class DetailView(BaseView):
    #หน้าแสดงรายละเอียดโครงการ
    def __init__(self, master, controller):
        super().__init__(master, controller)

        self.project = None 

        self.title_lbl = ttk.Label(self, text="Project Detail", font=("Arial", 18))
        self.title_lbl.pack(pady=10)

        self.info_frame = ttk.Frame(self)
        self.info_frame.pack(pady=10, padx=20, fill="x")

        self.name_lbl = ttk.Label(self.info_frame, text="Name: ", font=("Arial", 14))
        self.name_lbl.pack(anchor="w", pady=4)

        self.target_lbl = ttk.Label(self.info_frame, text="Target: ", font=("Arial", 12))
        self.target_lbl.pack(anchor="w", pady=2)

        self.current_lbl = ttk.Label(self.info_frame, text="Current: ", font=("Arial", 12))
        self.current_lbl.pack(anchor="w", pady=2)

        self.deadline_lbl = ttk.Label(self.info_frame, text="Deadline: ", font=("Arial", 12))
        self.deadline_lbl.pack(anchor="w", pady=2)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self, orient="horizontal",
                                            length=300, mode="determinate",
                                            variable=self.progress_var, maximum=100)
        self.progress_bar.pack(pady=10)

        ttk.Button(self, text="Back", command=self.on_back).pack(pady=8)

    def load_project(self, project):
        """โหลด project ที่เลือกมาแสดงผล"""
        self.project = project
        self.title_lbl.config(text=f"Project: {project.name}")
        self.name_lbl.config(text=f"Name: {project.name}")
        self.target_lbl.config(text=f"Target: {project.fundraising_target}")
        self.current_lbl.config(text=f"Current: {project.fundraising_current}")
        self.deadline_lbl.config(text=f"Deadline: {project.deadline}")

        percent = 0
        if project.fundraising_target > 0:
            percent = (project.fundraising_current / project.fundraising_target) * 100
        self.progress_var.set(percent)

    def on_back(self):
        if self.controller.previous_page:
            self.controller.show_page(self.controller.previous_page)
        else:
            self.controller.show_page("read")  

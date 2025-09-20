from tkinter import ttk
from .base_view import BaseView

class MainMenuView(BaseView):
    def __init__(self, master, controller):
        super().__init__(master, controller)

        ttk.Label(self, text="Main Menu", font=("Arial", 18)).pack(pady=20)

        ttk.Button(self, text="Read Items", command=lambda: controller.show_page("read")).pack(pady=5)

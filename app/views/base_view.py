import tkinter as tk
from tkinter import ttk

class BaseView(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

    def show(self):
        self.lift()

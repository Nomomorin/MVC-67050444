import tkinter as tk
from tkinter import ttk, messagebox
from .base_view import BaseView

class LoginView(BaseView):
    #สำหรับหน้า login
    def __init__(self, master, controller):
        super().__init__(master, controller)

        ttk.Label(self, text="Login", font=("Arial", 16)).pack(pady=10)

        form = ttk.Frame(self)
        form.pack(pady=10)

        ttk.Label(form, text="Username").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.username_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.username_var).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form, text="Password").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.password_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.password_var, show="*").grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(self, text="Login", command=self.do_login).pack(pady=10)

    def do_login(self):
        username = self.username_var.get()
        password = self.password_var.get()

        user = self.controller.User_model.check_login(username, password)
        if user:
            self.controller.current_user = user
            messagebox.showinfo("Success", f"Welcome {user['name']}")
            self.controller.show_page("usermenu")  
        else:
            messagebox.showerror("Error", "Invalid username or password")

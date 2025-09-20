import tkinter as tk
from tkinter import ttk, messagebox
from .base_view import BaseView

class UserMenuView(BaseView):
      #หน้าเมนูหลักของ user
      def __init__(self, master, controller):
            super().__init__(master, controller)

            ttk.Label(self, text="Menu", font=("Arial", 16)).pack(pady=10)

            form = ttk.Frame(self)
            form.pack(pady=10)

            cols = ("id", "project_name", "amount", "timestamp", "reward_level")
            self.table = ttk.Treeview(self, columns=cols, show="headings")
            for col in cols:
                  self.table.heading(col, text=col.capitalize())
            self.table.pack(fill="both", expand=True, padx=12, pady=12)

            btn_frame = ttk.Frame(self)
            btn_frame.pack(pady=8)
            ttk.Button(btn_frame, text="Detail", command=self.on_detail).pack(side="left", padx=4)
            ttk.Button(btn_frame, text="Support", command=self.on_to_read).pack(side="left", padx=4)
            ttk.Button(btn_frame, text="Stat", command=self.show_stats).pack(pady=6)

      def set_rows(self, rows):
            for i in self.table.get_children():
                  self.table.delete(i)
            for r in rows:
                  self.table.insert("", "end", values=(r["id"], r["project_name"], r["amount"], r["timestamp"], r["reward_level"]))

      def on_to_read(self):
            self.controller.show_page("read")
      def show_stats(self):
            self.controller.show_stats()
      def get_selected_id(self):
            selected = self.table.selection()
            if not selected:
                  return None
            vals = self.table.item(selected[0], "values")
            return int(vals[0])


      def on_detail(self):
            item_id = self.get_selected_id()
            if item_id is None:
                  messagebox.showerror("Error", "Please select a row to view details.")
                  return 

            self.controller.go_to_detail(item_id, from_page="usermenu")
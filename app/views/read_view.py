from tkinter import ttk, messagebox
import tkinter as tk
from .base_view import BaseView

class ReadView(BaseView):
    #หน้าแสดงรายการโครงการทั้งหมด  และเลือกสนับสนุน โครงการ
    def __init__(self, master, controller):
        super().__init__(master, controller)


        ttk.Label(self, text="All Items", font=("Arial", 16)).pack(pady=10)

        control_frame = ttk.Frame(self)
        control_frame.pack(fill="x", padx=12, pady=6)

        ttk.Label(control_frame, text="Search:").pack(side="left")
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(control_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side="left", padx=6)
        ttk.Button(control_frame, text="Go", command=self.apply_filters).pack(side="left")

        ttk.Label(control_frame, text="Category:").pack(side="left", padx=(12,0))
        self.category_var = tk.StringVar()
        self.category_cb = ttk.Combobox(control_frame, textvariable=self.category_var,values=["All", "การศึกษา", "สุขภาพ", "สิ่งแวดล้อม"], width=15)
        self.category_cb.current(0)
        self.category_cb.pack(side="left", padx=6)
        ttk.Button(control_frame, text="Filter", command=self.apply_filters).pack(side="left")

        ttk.Label(control_frame, text="Sort by:").pack(side="left", padx=(12,0))
        self.sort_var = tk.StringVar()
        self.sort_cb = ttk.Combobox(control_frame, textvariable=self.sort_var,values=["Newest", "Deadline Soon", "Most Funded"], width=15)
        self.sort_cb.current(0)
        self.sort_cb.pack(side="left", padx=6)
        ttk.Button(control_frame, text="Apply", command=self.apply_filters).pack(side="left")


        cols = ("id", "name", "fundraising_target", "fundraising_current", "deadline")
        self.table = ttk.Treeview(self, columns=cols, show="headings")
        for col in cols:
            self.table.heading(col, text=col.capitalize())
        self.table.pack(fill="both", expand=True, padx=12, pady=12)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=8)
        ttk.Button(btn_frame, text="Support", command=self.on_support).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Detail", command=self.on_detail).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Back", command=self.on_back).pack(side="left", padx=4)
        #ttk.Button(btn_frame, text="Back", command=lambda: controller.show_page("menu")).pack(side="left", padx=4)

    def set_rows(self, rows):
        for i in self.table.get_children():
            self.table.delete(i)
        for r in rows:
            self.table.insert("", "end", values=(r.id, r.name, r.fundraising_target, r.fundraising_current, r.deadline))

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
        self.controller.go_to_detail(item_id, from_page="read")

    def on_back(self):
        self.controller.show_page("usermenu")

    def on_update(self):
        item_id = self.get_selected_id()
        if item_id is None:
            messagebox.showerror("Error", "Please select a row to update.")
            return
        self.controller.go_to_update(item_id)

    def on_delete(self):
        item_id = self.get_selected_id()
        if item_id is None:
            messagebox.showerror("Error", "Please select a row to delete.")
            return
        self.controller.go_to_delete(item_id)


    def apply_filters(self):
        rows = self.controller.Project_model.list_items()

        keyword = self.search_var.get().lower()
        if keyword:
            rows = [r for r in rows if keyword in r.name.lower()]

        category = self.category_var.get()
        if category and category != "All":
            rows = [r for r in rows if category in r.name]

        sort_option = self.sort_var.get()
        if sort_option == "Newest":
            rows.sort(key=lambda r: r.id, reverse=True)
        elif sort_option == "Deadline Soon":
            rows.sort(key=lambda r: r.deadline)  
        elif sort_option == "Most Funded":
            rows.sort(key=lambda r: r.fundraising_current, reverse=True)

        self.set_rows(rows)

    def refresh(self): 
        self.apply_filters()

    def on_support(self):
        item_id =  self.get_selected_id()
        if item_id is None:
            messagebox.showerror("Error", "Please select a project to support.")
            return

        project = next((p for p in self.controller.Project_model.list_items() if p.id == item_id), None)
        if not project:
            messagebox.showerror("Error", "Project not found.")
            return

        top = tk.Toplevel(self)
        top.title("Support Project")

        ttk.Label(top, text=f"Support Project: {project.name}", font=("Arial", 12)).pack(pady=6)
        ttk.Label(top, text="Enter amount:").pack()

        amount_var = tk.StringVar()
        entry = ttk.Entry(top, textvariable=amount_var)
        entry.pack(pady=4)

        def do_support():
            try:
                amount = int(amount_var.get())
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number.")
                return

            min_support = 100
            if amount < min_support:
                messagebox.showerror("Error", f"Minimum support is {min_support}.")
                return

            self.controller.Pledge_model.add_pledge(
                user_id=int(self.controller.current_user["id"]),
                project_id=project.id,
                amount=amount
            )

            self.controller.Project_model.update_current_amount(
                project.id, project.fundraising_current + amount
            )

            messagebox.showinfo("Success", "Thank you for your support!")
            top.destroy()
            self.refresh()

        ttk.Button(top, text="Confirm", command=do_support).pack(pady=6)
        ttk.Button(top, text="Cancel", command=top.destroy).pack()
import tkinter as tk
from tkinter import messagebox
from app.models.Project_model import ProjectModel
from app.models.User_model import UserModel
from app.models.Pledge_model import PledgeModel
from app.models.Reward_Model import RewardModel
from app.views.main_menu_view import MainMenuView
from app.views.user_menu_view import UserMenuView
from app.views.stats_view import StatsView
from app.views.read_view import ReadView
from app.views.login_liew import LoginView
from app.views.detail_view import DetailView

class MainController(tk.Tk):
    #-- init --- สร้างหน้าต่างหลัก
    def __init__(self):
        super().__init__()
        self.title("MVC")
        self.geometry("1025x400")

        self.current_user = None

        self.Project_model = ProjectModel()
        self.User_model = UserModel()
        self.Reward_model = RewardModel()
        self.Pledge_model = PledgeModel(
            project_model=self.Project_model,
            reward_model=self.Reward_model,
            user_model=self.User_model
        )
        self.frames = {}

        self.previous_page = None

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        for V, name in [
            (UserMenuView, "usermenu"),
            (ReadView, "read"),
            (LoginView, "login"),
            (DetailView, "detail"),
            (StatsView, "stats")
        ]:
            frame = V(container, self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_page("login")

    #--- show page --- สำหรับแสดงหน้าต่างๆ
    def show_page(self, name):
        frame = self.frames[name]
        if name == "read":
            frame.set_rows(self.Project_model.list_items())
        if name == "usermenu":
            self.show_user_pledges(frame=frame)
            #frame.set_rows(self.Pledge_model.list_items_by_user_id(self.current_user["id"]))
        frame.show()

    # --- Add ---
    def add_item(self, name, qty):
        self.model.add_item(name, int(qty))

        # --- detail ---
    def go_to_detail(self, item_id, from_page=None):
        item = next((i for i in self.Project_model.list_items() if i.id == item_id), None)
        if not item:
            messagebox.showerror("Error", "Item not found")
            return
        if from_page:
            self.previous_page = from_page
        self.frames["detail"].load_project(item)
        self.show_page("detail")


    # --- Update ---
    def go_to_update(self, item_id):
        item = next((i for i in self.model.list_items() if i.id == item_id), None)
        if not item:
            messagebox.showerror("Error", "Item not found")
            return
        self.frames["update"].load_item(item)
        self.show_page("update")

    def update_item(self, item_id, name, qty):
        if not self.model.update_item(int(item_id), name, int(qty)):
            raise Exception("Update failed")

    # --- Delete ---
    def go_to_delete(self, item_id):
        item = next((i for i in self.model.list_items() if i.id == item_id), None)
        if not item:
            messagebox.showerror("Error", "Item not found")
            return
        self.frames["delete"].load_item(item)
        self.show_page("delete")

    def delete_item(self, item_id):
        if not self.model.delete_item(int(item_id)):
            raise Exception("Delete failed")
        
    #แสดงโครงการที่ user สนับสนุน
    def show_user_pledges(self, frame):
        pledges = self.Pledge_model.list_items_by_user_id(int(self.current_user["id"]))
        projects = self.Project_model.list_items()
        project_lookup = {p.id: p.name for p in projects}

        rows = []
        for pledge in pledges:
            rows.append({
                "id": pledge.id,
                "project_id": pledge.project_id,
                "project_name": project_lookup.get(pledge.project_id, "Unknown"),
                "amount": pledge.amount,
                "timestamp": pledge.timestamp,
                "reward_level": pledge.reward_level
            })

        frame.set_rows(rows)

    #--- สถิติ --- ของ user
    def show_stats(self):
        total_success = len(self.Pledge_model.list_items())   
        total_rejects = self.User_model.get_total_rejects()  

        self.frames["stats"].set_stats(total_success, total_rejects)
        self.show_page("stats")
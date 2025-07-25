import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def generate_new_id(tasks):
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1

def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class TaskTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Tracker")
        self.root.geometry("850x500")
        self.root.configure(bg="#1e1e2f")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", 
                        background="#2d2d3c",
                        foreground="white",
                        rowheight=28,
                        fieldbackground="#2d2d3c",
                        font=("Segoe UI", 11))
        style.map('Treeview', background=[('selected', '#4444aa')])
        style.configure("Treeview.Heading", font=("Segoe UI Semibold", 12), background="#44475a", foreground="white")

        style.configure("TButton", font=("Segoe UI", 10), padding=6)

        self.tree = ttk.Treeview(root, columns=("ID", "Description", "Status", "Created", "Updated"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Description", text="Përshkrimi")
        self.tree.heading("Status", text="Statusi")
        self.tree.heading("Created", text="Krijuar më")
        self.tree.heading("Updated", text="Përditësuar")

        self.tree.column("ID", width=40)
        self.tree.column("Description", width=250)
        self.tree.column("Status", width=120)
        self.tree.column("Created", width=180)
        self.tree.column("Updated", width=180)

        self.tree.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        button_frame = tk.Frame(root, bg="#1e1e2f")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Shto", command=self.add_task, bg="#4CAF50", fg="white", relief="flat", width=12).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Fshi", command=self.delete_task, bg="#f44336", fg="white", relief="flat", width=12).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Done", command=lambda: self.update_status("done"), bg="#3c91e6", fg="white", relief="flat", width=12).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="In Progress", command=lambda: self.update_status("in-progress"), bg="#ff9800", fg="white", relief="flat", width=12).grid(row=0, column=3, padx=5)
        tk.Button(button_frame, text="Todo", command=lambda: self.update_status("todo"), bg="#9c27b0", fg="white", relief="flat", width=12).grid(row=0, column=4, padx=5)

        self.refresh_tasks()

    def refresh_tasks(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for task in load_tasks():
            self.tree.insert("", "end", values=(
                task["id"],
                task["description"],
                self.style_status(task["status"]),
                task["createdAt"],
                task["updatedAt"]
            ))

    def style_status(self, status):
        emojis = {
            "todo": "TODO",
            "in-progress": "In Progress",
            "done": "Done"
        }
        return emojis.get(status, status)

    def add_task(self):
        description = simpledialog.askstring("Shto Detyrë", "Shkruaj përshkrimin:")
        if description:
            tasks = load_tasks()
            new_task = {
                "id": generate_new_id(tasks),
                "description": description,
                "status": "todo",
                "createdAt": current_time(),
                "updatedAt": current_time()
            }
            tasks.append(new_task)
            save_tasks(tasks)
            self.refresh_tasks()

    def delete_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Kujdes", "Zgjidh një detyrë për të fshirë.")
            return
        task_id = int(self.tree.item(selected[0])["values"][0])
        tasks = load_tasks()
        tasks = [t for t in tasks if t["id"] != task_id]
        save_tasks(tasks)
        self.refresh_tasks()

    def update_status(self, new_status):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Kujdes", "Zgjidh një detyrë për të përditësuar.")
            return
        task_id = int(self.tree.item(selected[0])["values"][0])
        tasks = load_tasks()
        for t in tasks:
            if t["id"] == task_id:
                t["status"] = new_status
                t["updatedAt"] = current_time()
                break
        save_tasks(tasks)
        self.refresh_tasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskTrackerGUI(root)
    root.mainloop()

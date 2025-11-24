import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import datetime
from tkcalendar import DateEntry

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do App")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        # Style configuration
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Helvetica", 10, "bold"), padding=5)
        style.configure("TEntry", padding=5)
        style.configure("TLabel", font=("Helvetica", 12))
        
        # Main container
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Add New Task", padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 10))

        # Task entry
        ttk.Label(input_frame, text="Task:").grid(row=0, column=0, sticky="w")
        self.task_var = tk.StringVar()
        self.task_entry = ttk.Entry(input_frame, textvariable=self.task_var, width=40)
        self.task_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        
        # Priority selection
        ttk.Label(input_frame, text="Priority:").grid(row=1, column=0, sticky="w")
        self.priority_var = tk.StringVar(value="Medium")
        priorities = ["High", "Medium", "Low"]
        self.priority_combo = ttk.Combobox(input_frame, textvariable=self.priority_var, values=priorities, state="readonly", width=10)
        self.priority_combo.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Due date
        ttk.Label(input_frame, text="Due Date:").grid(row=1, column=2, sticky="w")
        self.due_date = DateEntry(input_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.due_date.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        # Add button
        add_btn = ttk.Button(input_frame, text="Add Task", command=self.add_task)
        add_btn.grid(row=2, column=0, columnspan=4, pady=10)
        self.task_entry.bind("<Return>", self.add_task)

        # Tasks list
        list_frame = ttk.LabelFrame(main_frame, text="Tasks", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview for tasks
        columns = ("Task", "Priority", "Due Date", "Status")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # Configure columns
        self.tree.heading("Task", text="Task")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Due Date", text="Due Date")
        self.tree.heading("Status", text="Status")
        
        self.tree.column("Task", width=200)
        self.tree.column("Priority", width=70)
        self.tree.column("Due Date", width=100)
        self.tree.column("Status", width=70)

        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Pack tree and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Control buttons
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=10)

        ttk.Button(control_frame, text="Delete", command=self.delete_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Mark Complete", command=self.mark_done).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Clear All", command=self.clear_all).pack(side=tk.RIGHT, padx=5)

        # Load tasks
        self.tasks_file = "tasks.txt"
        self.load_tasks()

    def add_task(self, event=None):
        task = self.task_var.get().strip()
        if task:
            priority = self.priority_var.get()
            due_date = self.due_date.get_date().strftime("%Y-%m-%d")
            self.tree.insert("", tk.END, values=(task, priority, due_date, "Pending"))
            self.task_var.set("")
            self.save_tasks()

    def delete_task(self):
        selected = self.tree.selection()
        if selected:
            if messagebox.askyesno("Confirm", "Delete selected task?"):
                self.tree.delete(selected)
                self.save_tasks()

    def mark_done(self):
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            task_values = list(self.tree.item(item)['values'])
            task_values[3] = "Completed"
            self.tree.item(item, values=task_values)
            self.save_tasks()

    def clear_all(self):
        if messagebox.askyesno("Confirm", "Clear all tasks?"):
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.save_tasks()

    def load_tasks(self):
        if os.path.exists(self.tasks_file):
            try:
                with open(self.tasks_file, "r", encoding="utf-8") as f:
                    for line in f:
                        task_data = line.strip().split("|")
                        if len(task_data) == 4:
                            self.tree.insert("", tk.END, values=task_data)
            except:
                messagebox.showerror("Error", "Could not load tasks")

    def save_tasks(self):
        try:
            with open(self.tasks_file, "w", encoding="utf-8") as f:
                for item in self.tree.get_children():
                    values = self.tree.item(item)['values']
                    f.write(f"{values[0]}|{values[1]}|{values[2]}|{values[3]}\n")
        except:
            messagebox.showerror("Error", "Could not save tasks")
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

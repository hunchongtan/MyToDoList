import os
import json
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

def get_sun():
    datetime_now = datetime.now()
    sun = ""
    if datetime_now.hour < 12:
        sun = "Morning"
    elif datetime_now.hour < 18:
        sun = "Afternoon"
    else:
        sun = "Evening"
    return sun

class Manager():
    def __init__(self, sun, data, config_path):

        self.user_name = data["settings"]["name"]
        self.task_counter = data["settings"]["task_counter"]
        self.task_dict = data["tasks"]
        self.config_path = config_path

        self.root = tk.Tk()
        self.root.title("Todolist")
        self.root.geometry("1000x800")

        menubar = tk.Menu(self.root)

        self.greeting_message = tk.StringVar()
        self.greeting_message.set(f"Good {sun} {self.user_name}!!")

        self.datetime_message = tk.StringVar()
        datetime_now = datetime.now()
        self.datetime_message.set(datetime_now.date())

        addtaskmenu = tk.Menu(menubar, tearoff=0)
        addtaskmenu.add_command(label="Add new Task", command=lambda:self.add_task())
        addtaskmenu.add_command(label="Edit Task")
        addtaskmenu.add_command(label="Delete Task")
        menubar.add_cascade(menu=addtaskmenu, label="Tasks")

        settingsmenu = tk.Menu(menubar, tearoff=0)
        settingsmenu.add_command(label="Edit Name", command=lambda:self.edit_name())
        menubar.add_cascade(menu=settingsmenu, label="Settings")

        self.root.config(menu=menubar)

        tk.Label(self.root, textvariable=self.greeting_message, font=('Arial', 18)).grid(row=0, column=0)

        tk.Button(self.root, textvariable=self.datetime_message, font=('Arial', 18), command=lambda:self.edit_date()).grid(row=0, column=1)

        tk.Label(self.root, text="Today's Tasks", font=('Arial', 18)).grid(row=1, column=0)

        frame1 = tk.Frame(self.root)
        frame1.grid(row=2, column=0)

        self.listbox = tk.Listbox(frame1, bg="SystemButtonFace")
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        scrollbar = tk.Scrollbar(frame1)
        scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
        
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        self.init_list(self.task_dict)
        
        self.root.protocol("WM_DELETE_WINDOW", lambda:self.on_close())
        
        self.root.mainloop()

    def update_task(self, res, task_id):
        print(task_id)
        print(type(task_id))
        self.task_dict[int(task_id)] = res

    def delete_task(self, task_id):
        del self.task_dict[task_id]

    def get_date_tasks(self, date):
        ls = []
        for keys in self.task_dict.keys():
            if data[keys]["datetime"] == date:
                ls.append(data[keys])
        return ls

    def init_list(self, task_dict):
        self.listbox.delete(0, tk.END)
        for val in task_dict.values():
            self.listbox.insert(tk.END, val["name"])

    def update_name(self, new_name):
        self.user_name = new_name
        self.greeting_message.set(f"Good {sun} {self.user_name}!!")

    def edit_name(self):
        popup = tk.Toplevel()
        popup.wm_title("Edit Name")

        tk.Label(popup, text="Enter your name", font=('Arial', 18)).grid(row=0, column=0)

        textbox = tk.Entry(popup, font=('Arial', 16))
        textbox.grid(row=1, column=0)

        tk.Button(popup, text="Update", font=('Arial', 16), command=lambda:[self.update_name(textbox.get()), popup.destroy()]).grid(row=2, column=0)

    def save_all(self):
        data = {
            "settings": {
                "name": self.user_name,
                "task_counter": self.task_counter
            },
            "tasks": self.task_dict
        }
        with open(self.config_path, 'w') as f:
            json.dump(data, f, indent=4)

    def on_close(self):
        if messagebox.askyesno(title="Quit", message="Do you really want to quit?"):
            self.save_all()
            self.root.destroy()
        
    def edit_date(self):
        popup = tk.Toplevel()
        popup.wm_title("Edit Date")

        tk.Label(popup, text="Enter a new date (YYYY-MM-DD)", font=('Arial', 18)).grid(row=0, column=0)

        textbox = tk.Entry(popup, font=('Arial', 16))
        textbox.grid(row=1, column=0)

        tk.Button(popup, text="Update", font=('Arial', 16), command=lambda:[self.datetime_message.set(textbox.get()), popup.destroy()]).grid(row=2, column=0)

    def generate_task_id(self):
        self.task_counter += 1
        return self.task_counter
    
    def add_task(self):
        popup = tk.Toplevel()
        popup.wm_title("Add Task")

        datetime_now = datetime.now()

        tk.Label(popup, text="Task Name: ", font=('Arial', 18)).grid(row=0, column=0)

        task_name_textbox = tk.Entry(popup, font=('Arial', 16))
        
        task_name_textbox.grid(row=0, column=1)

        tk.Label(popup, text="Due by (yyyy-mm-dd hh:mm): ", font=('Arial', 18)).grid(row=1, column=0)

        due_textbox = tk.Entry(popup, font=('Arial', 16))
        due_textbox.insert(tk.END, f'{datetime_now.year}-{datetime_now.month}-{datetime_now.day} 23:59')
        due_textbox.grid(row=1, column=1)

        tk.Button(popup, text="Add", font=('Arial', 16), command=lambda:[self.update_task({"name": task_name_textbox.get(), "datetime": due_textbox.get()}, self.generate_task_id()), popup.destroy(), self.init_list(self.task_dict)]).grid(row=2, column=0)

def create_config(config_path):
    config = {
        "settings": {
            "name": "",
            "task_counter": 0
        },
        "tasks": {},
    }

    with open(config_path, 'w') as f:
        json.dump(config, f)

def load_config(config_path):
    with open(config_path, 'r') as f:
        data = json.load(f)
        
    return data

if __name__ == "__main__":

    config_path = 'config\\data.json'

    if not os.path.isfile(config_path):
        create_config(config_path)
    
    sun = get_sun()
    data = load_config(config_path)

    manager = Manager(sun, data, config_path)

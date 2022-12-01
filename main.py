import os
import json
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

def create_config(config_path):
    config = {
        "settings": {
            "name": ""
        },
        "tasks": [],
    }

    with open(config_path, 'w') as f:
        json.dump(config, f)

def load_config(config_path):
    with open(config_path, 'r') as f:
        data = json.load(f)
        
    return data

def update_name(data, name, popup, greeting_message, sun):
    greeting_message.set(f"Good {sun} {name}!!")
    data["settings"]["name"] = name
    popup.destroy()

def edit_name(data, greeting_message, sun):
    popup = tk.Toplevel()
    popup.wm_title("Edit Name")

    tk.Label(popup, text="Enter your name", font=('Arial', 18)).grid(row=0, column=0)

    textbox = tk.Entry(popup, font=('Arial', 16))
    textbox.grid(row=1, column=0)

    tk.Button(popup, text="Update", font=('Arial', 16), command=lambda:update_name(data, textbox.get(), popup, greeting_message, sun)).grid(row=2, column=0)

def save_all(data, config_path):
    with open(config_path, 'w') as f:
        json.dump(data, f)

def on_close(root, data, config_path):
    if messagebox.askyesno(title="Quit", message="Do you really want to quit?"):
        save_all(data, config_path)
        root.destroy()

def update_date(date, popup, datetime_message):
    datetime_message.set(date)
    popup.destroy()

def edit_date(datetime_message):
    popup = tk.Toplevel()
    popup.wm_title("Edit Date")

    tk.Label(popup, text="Enter a new date (YYYY-MM-DD)", font=('Arial', 18)).grid(row=0, column=0)

    textbox = tk.Entry(popup, font=('Arial', 16))
    textbox.grid(row=1, column=0)

    tk.Button(popup, text="Update", font=('Arial', 16), command=lambda:update_date(textbox.get(), popup, datetime_message)).grid(row=2, column=0)
    datetime_message.set()

if __name__ == "__main__":

    config_path = 'config\\data.json'

    if not os.path.isfile(config_path):
        create_config(config_path)
    
    datetime_now = datetime.now()
    sun = ""
    if datetime_now.hour < 12:
        sun = "Morning"
    elif datetime_now.hour < 18:
        sun = "Afternoon"
    else:
        sun = "Evening"
    data = load_config(config_path)
    name = data["settings"]["name"]

    root = tk.Tk()
    root.title("Todolist")
    root.geometry("1000x800")

    menubar = tk.Menu(root)

    greeting_message = tk.StringVar()
    greeting_message.set(f"Good {sun} {name}!!")

    datetime_message = tk.StringVar()
    datetime_message.set(datetime_now.date())

    addtaskmenu = tk.Menu(menubar, tearoff=0)
    addtaskmenu.add_command(label="Add new Task")
    addtaskmenu.add_command(label="Edit Task")
    addtaskmenu.add_command(label="Delete Task")
    menubar.add_cascade(menu=addtaskmenu, label="Tasks")

    settingsmenu = tk.Menu(menubar, tearoff=0)
    settingsmenu.add_command(label="Edit Name", command=lambda:edit_name(data, greeting_message, sun))
    menubar.add_cascade(menu=settingsmenu, label="Settings")

    root.config(menu=menubar)

    tk.Label(root, textvariable=greeting_message, font=('Arial', 18)).grid(row=0, column=0)

    tk.Button(root, textvariable=datetime_message, font=('Arial', 18), command=lambda:edit_date(datetime_message)).grid(row=0, column=1)

    tk.Label(root, text="Today's Tasks", font=('Arial', 18)).grid(row=1, column=0)

    frame1 = tk.Frame(root)
    frame1.grid(row=2, column=0)

    listbox = tk.Listbox(frame1)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH)

    scrollbar = tk.Scrollbar(listbox)
    scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
    
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    # for item in ls:
    #     listbox.insert(tk.END, item)

    root.protocol("WM_DELETE_WINDOW", lambda:on_close(root, data, config_path))
    
    root.mainloop()

import os
import json
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)


def get_sun():
    datetime_now = datetime.now()
    sun = ""
    if datetime_now.hour < 12:
        sun = "MORNING"
    elif datetime_now.hour < 18:
        sun = "AFTERNOON"
    else:
        sun = "EVENING"
    return sun

class Manager():
    def __init__(self, sun, data, config_path):

        self.user_name = data["settings"]["name"]
        self.task_counter = data["settings"]["task_counter"]
        self.completed_counter = data["settings"]["completed_counter"]
        self.task_dict = data["tasks"]
        self.config_path = config_path

        self.root = tk.Tk()
        self.root.title("My To Do List!")
        self.root.geometry("1000x600")
    
        bgimg = Image.open('assets\\background.png')
        bgimg = bgimg.resize((1000, 600))
        bg = ImageTk.PhotoImage(bgimg)
        addimg = Image.open('assets\\add.png')
        addimg = addimg.resize((20, 20))
        add = ImageTk.PhotoImage(addimg)
        # editimg = Image.open('assets\\edit.png')
        # editimg = editimg.resize((20, 20))
        # edit = ImageTk.PhotoImage(editimg)
        # deleteimg = Image.open('assets\\delete.png')
        # deleteimg = deleteimg.resize((20, 20))
        # delete = ImageTk.PhotoImage(deleteimg)

        menubar = tk.Menu(self.root)

        self.greeting_message = tk.StringVar()
        self.greeting_message.set(f"GOOD {sun} {self.user_name}!!")

        self.date_message = tk.StringVar()
        date_now = datetime.now()
        self.date_message.set(date_now.date())

        self.time_message = tk.StringVar()
        time_now = datetime.now()
        time_now = time_now.strftime("%H:%M")
        self.time_message.set(time_now)

        addtaskmenu = tk.Menu(menubar, tearoff=0)
        addtaskmenu.add_command(label="Add new Task", command=lambda:self.add_task())
        addtaskmenu.add_command(label="Edit Task")
        addtaskmenu.add_command(label="Delete Task")
        menubar.add_cascade(menu=addtaskmenu, label="Tasks")

        settingsmenu = tk.Menu(menubar, tearoff=0)
        settingsmenu.add_command(label="Edit Name", command=lambda:self.edit_name())
        settingsmenu.add_command(label="Edit Date", command=lambda:self.edit_date())
        settingsmenu.add_command(label="Edit Time", command=lambda:self.edit_time())
        menubar.add_cascade(menu=settingsmenu, label="Settings")

        self.root.config(menu=menubar)

        tk.Label(self.root, image=bg).place(x = 0,y = 0)

        tk.Label(self.root, textvariable=self.date_message, font=('Arial', 18)).grid(row=0, column=0)

        tk.Label(self.root, textvariable=self.time_message, font=('Arial', 18)).grid(row=0, column=1)

        tk.Label(self.root, textvariable=self.greeting_message, font=('Arial', 18)).grid(row=1, column=0)

        tk.Label(self.root, text="What do you want to achieve today?", font=('Arial', 18)).grid(row=2, column=0)

        tk.Button(self.root, image=add, command=lambda:self.add_task()).grid(row=2, column=1)

        tk.Button(self.root, text="Weekly Performance Report", font=('Arial', 18), command=lambda:self.task_review()).grid(row=6, column=0)
        
        frame1 = tk.Frame(self.root)
        frame1.grid(row=3, column=0)
        
        self.progressbar = ttk.Progressbar(frame1, orient='horizontal', mode='determinate', length=280)
        self.progressbar.pack(side=tk.LEFT, fill=tk.BOTH)

        self.start_button = ttk.Button(frame1, text='Refresh',command=lambda:self.progress())
        self.start_button.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.value_label = ttk.Label(self.root, text=self.update_progress_label())
        self.value_label.grid(row=4, column=0)

        frame2 = tk.Frame(self.root)
        frame2.grid(row=5, column=0)

        self.listbox = tk.Listbox(frame2, bg="SystemButtonFace")
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        scrollbar = tk.Scrollbar(frame2)
        scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

        # self.checkbox = ttk.Checkbutton(self.listbox, command=lambda:self.check_completed, onvalue='on', offvalue='off').pack()
        
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

    def update_sun(self):
        datetime_edit = self.time_message.get()
        sun = ""
        if int(datetime_edit[:2]) < 12:
            sun = "MORNING"
        elif int(datetime_edit[:2]) < 18:
            sun = "AFTERNOON"
        else:
            sun = "EVENING"
        self.greeting_message.set(f"GOOD {sun} {self.user_name}!!")
    
    def update_name(self, new_name):
        self.user_name = new_name
        self.greeting_message.set(f"GOOD {sun} {self.user_name}!!")

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
                "task_counter": self.task_counter,
                "completed_counter": self.completed_counter
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


        tk.Button(popup, text="Update", font=('Arial', 16), command=lambda:[self.date_message.set(textbox.get()), popup.destroy()]).grid(row=2, column=0)

    def is_time(self, s):
        # if len(s) == 5:
        #     return False
        # elif s[0].isnumeric() == False:
        #     return False
        pass

    def check_time(self, s):
        # if self.is_time(s) == False:
        #     print ("Invalid")
        pass

    def edit_time(self):
        popup = tk.Toplevel()
        popup.wm_title("Edit Time")

        tk.Label(popup, text="Enter a new time (HH:MM)", font=('Arial', 18)).grid(row=0, column=0)

        textbox = tk.Entry(popup, font=('Arial', 16))
        textbox.grid(row=1, column=0)

        tk.Button(popup, text="Update", font=('Arial', 16), command=lambda:[self.check_time(textbox.get()), self.time_message.set(textbox.get()), popup.destroy(), self.update_sun()]).grid(row=2, column=0)

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
        
    def task_review(self):
        popup = tk.Toplevel()
        popup.wm_title("Your Performance Report")

        fig = Figure(figsize = (5, 5), dpi = 100)
        y = [3, 2, 1, 3, 4, 2, 1]
        x = ['mon', 'tues', 'wed', 'thur', 'fri', 'sat', 'sun']
        plot1 = fig.add_subplot(111)
        plot1.plot(x, y)
        canvas = FigureCanvasTkAgg(fig, popup)  
        canvas.draw()
        canvas.get_tk_widget().pack()
    
        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(canvas, popup)
        toolbar.update()
    
        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().pack()

    def generate_completed_id(self):
        self.completed_counter += 1
        return self.completed_counter

    def check_completed(self):
        pass

    def progressvalue(self):
        completionpercent = (self.completed_counter/self.task_counter)*100
        return completionpercent
    
    def update_progress_label(self):
        return f"Current Progress: {self.progressbar['value']}%"

    def progress(self):
        if self.progressbar['value'] < 100:
            self.progressbar['value'] = self.progressvalue()
            self.value_label['text'] = self.update_progress_label()
        else:
            self.value_label['text'] = 'All Tasks completed today!'

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

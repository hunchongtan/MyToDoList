import json
import os
import tkinter as tk
import datetime
import time
from tkinter import messagebox, ttk

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.figure import Figure
from PIL import Image, ImageTk

class Manager():
    """
    Manager class manages all task and ui elements
    """
    def __init__(self, data, config_path):
        """
        Initialize main ui menu and attribute vars

        Inputs: config data (dict), config file path (str)
        """
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
        bgimg = ImageTk.PhotoImage(bgimg)
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
        self.date_message = tk.StringVar()
        self.time_message = tk.StringVar()

        addtaskmenu = tk.Menu(menubar, tearoff=0)
        addtaskmenu.add_command(label="Add new Task", command=self._add_task_popup)
        addtaskmenu.add_command(label="Edit Task", command=self._edit_task_list_popup)
        addtaskmenu.add_command(label="Delete Task", command=self._del_task_popup)
        menubar.add_cascade(menu=addtaskmenu, label="Tasks")

        settingsmenu = tk.Menu(menubar, tearoff=0)
        settingsmenu.add_command(label="Edit Name", command=self._edit_name)
        settingsmenu.add_command(label="Edit Date", command=self._edit_date)
        settingsmenu.add_command(label="Edit Time", command=self._edit_time)
        menubar.add_cascade(menu=settingsmenu, label="Settings")

        self.root.config(menu=menubar)

        tk.Label(self.root, image=bgimg).place(x = 0,y = 0)

        tk.Label(self.root,
                textvariable=self.date_message,
                font=('Arial', 18)
                ).grid(row=0, column=0)

        tk.Label(self.root,
                textvariable=self.time_message,
                font=('Arial', 18)
                ).grid(row=0, column=1)

        tk.Label(self.root, textvariable=self.greeting_message, font=('Arial', 18)).grid(row=1, column=0)

        tk.Label(self.root, text="What do you want to achieve today?", font=('Arial', 18)).grid(row=2, column=0)

        tk.Button(self.root, image=add, command=self._add_task_popup).grid(row=2, column=1)

        tk.Button(self.root, text="Weekly Performance Report", font=('Arial', 18), command=self._task_review).grid(row=6, column=0)

        frame1 = tk.Frame(self.root)
        frame1.grid(row=3, column=0)

        self.progressbar = ttk.Progressbar(frame1, orient='horizontal', mode='determinate', length=280)
        self.progressbar.pack(side=tk.LEFT, fill=tk.BOTH)

        self.start_button = ttk.Button(frame1, text='Refresh',command=self._progress)
        self.start_button.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.value_label = ttk.Label(self.root, text=self._update_progress_label())
        self.value_label.grid(row=4, column=0)

        frame2 = tk.Frame(self.root)
        frame2.grid(row=5, column=0)

        self.listbox = tk.Listbox(frame2, bg="SystemButtonFace")
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar = tk.Scrollbar(frame2)
        scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        tk.Label(self.root, text="Upcoming Tasks", font=('Arial', 18)).grid(row=0, column=3)
        frame3 = tk.Frame(self.root)
        frame3.grid(row=1, column=3)

        self.listbox_week = tk.Listbox(frame3, bg="SystemButtonFace")
        self.listbox_week.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar_week = tk.Scrollbar(frame3)
        scrollbar_week.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.listbox_week.config(yscrollcommand=scrollbar_week.set)
        scrollbar_week.config(command=self.listbox_week.yview)

        self._update_date(str(datetime.datetime.now().date()))
        self._update_time(str(datetime.datetime.now().strftime("%H:%M")))
        self._update_sun()

        self.mascot_img_ls = []
        for i in range(7):
            self.mascot_img_ls.append(ImageTk.PhotoImage(Image.open(fr'assets\\mascots\\dino\\frame-{i}.png')))
        self.mascot = tk.Label(self.root, image=self.mascot_img_ls[0])
        self.mascot.grid(row=2, column=3)
        self.mascot.bind('<Enter>', self._mascot_hover)

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        self.root.mainloop()

    def _mascot_run(self, idx):
        """
        Recursive function that changes mascot image, producing an animated effect

        Inputs: index of image (int)
        """
        if idx > 6:
            return
        frame = self.mascot_img_ls[idx]
        idx += 1
        self.mascot.configure(image=frame)
        time.sleep(0.1)
        self.root.after(5, self._mascot_run, idx)

    def _mascot_hover(self, _):
        """
        Triggers when mascot is hovered over and starts animation
        """
        self.root.after(0, self._mascot_run, 0)

    def _update_date(self, date):
        """
        Updates the apps date with input date

        Input: date (str)
        """
        self.app_date = date
        self.date_message.set(date)
        self._init_list()

    def _update_time(self, new_time):
        """
        Updates the apps time with input time

        Input: time (str)
        """
        self.app_time = new_time
        self.time_message.set(new_time)
        self._update_sun()

    def _update_task(self, res, task_id):
        """
        To add new tasks into the to-do-list

        Takes in a new task as dictionary (res) and appends it to the current dictionary (task_dict)
        Output obtained would have appended res to the end of the data

        Input: new task (dict), task_id (int)
        """
        self.task_dict[task_id] = res

    def _delete_task(self, task_id):
        del self.task_dict[task_id]

    def _get_date_tasks(self, date):
        """
        To obtain the current list of tasks available for that specified date

        Output provides the list of tasks available (in the form of a dictionary) for that specified
        date as stated in the current dictionary (self.task_dict)

        Input: date (str)
        """
        lsl = []
        for keys in self.task_dict.keys():
            if self.task_dict[keys]["datetime"][0:10] == date:
                lsl.append(self.task_dict[keys])
        return lsl

    def _get_week_tasks(self,date):
        """
        To obtain the current list of tasks available for the next 6 days, starting from the
        specified date. The list of tasks obtained will be stored in a dictionary. When the day ends,
        the system automatically appends a new list of available tasks back into the current
        dictionary (self.task_dict) so as to make up for the completed tasks from the previous day.

        Output provides the dict of tasks available for the next 6
        days, exclusive of the specified date

        Input: date (str)
        """
        #convert date from string to datetime.datetime and print date
        date = datetime.datetime.strptime(date, "%Y-%m-%d")

        #To obtain the dates for the next 6 days
        #Dates obtained will be stored as a key within the variable output (a dictionary)
        output = {}
        for idx in range(1, 7):
            next_days = date + datetime.timedelta(days=idx)
            #get dates of the next 7 consecutive days
            next_days_str = str(next_days)[0:10]
            output[next_days_str] = []

        #To obtain only the dates from the data (dictionary) through slicing
        #The dates obtained will be used to compare with the keys present in output (dictionary)
        
        #If the keys (dates) are the same:
        #Append the list of tasks (list of dictionaries) to output (dictionary)
        #Otherwise:
        #Do not append anything
        for d_keys in self.task_dict.keys():
            for o_keys in output.keys():
                if self.task_dict[d_keys]["datetime"][0:10] == o_keys:
                    output[o_keys].append(self.task_dict[d_keys])

        #To obtain the corresponding names of the days in the week with respect to the specified dates.

        #Iterates through the values in output.
        #Changes the individual keys (keys previously present in the output dictionary were a string of dates) to
        #become names of days in the week.
        new_o_keys = {}
        for index, val in enumerate(output.values()):
            #To obtain names of days in the week
            day = (date + datetime.timedelta(days=index + 1)).strftime('%A')
            new_o_keys[day] = val
        return new_o_keys

    def _date_correct(self, date):
        """
        Checks if given date string(YYYY-MM-DD) is valid

        Returns boolean

        Input: date (str)
        """
        lsl = date.split('-')

        if len(lsl) != 3:
            return False

        date_year = lsl[0]
        date_month = lsl[1]
        date_date = lsl[2]

        #Checks whether user input the date in the correct format (YYYY-MM-DD)
        if len(date_year) != 4:
            return False
        if len(date_month) != 2:
            return False
        if len(date_date) != 2:
            return False

        #Checks whether the user input a valid date
        is_valid_date = True
        try:
            datetime.datetime(int(date_year), int(date_month), int(date_date))
        except ValueError:
            is_valid_date = False
        if not is_valid_date:
            return False

        if len(lsl) == 3:
            return True
        return False


    def _time_correct(self, timestr):
        """
        Checks if given timestr string(HH:MM) is valid
        
        Returns boolean

        Input: time (str)
        """

        lsl = timestr.split(':')
        if len(lsl) != 2:
            return False
        time_hour = lsl[0]
        time_minute = lsl[1]

        #Checks whether the user input the time in the correct format (HH:MM)
        if len(time_hour) != 2:
            return False
        if len(time_minute) != 2:
            return False
        if int(time_hour) < 0 or int(time_hour) > 23:
            return False
        if int(time_minute) < 0 or int(time_minute) > 59:
            return False

        return True

    def _del_task_yesno(self, task_id):
        """
        Yes/no popup to confirm task deletion

        Input: task_id (str)
        """
        if messagebox.askyesno(title="Delete Task", message=f'Do you really want to delete task "{self.task_dict[task_id]["name"]}"?'):
            self._delete_task(task_id)
            self._init_list()

    def _del_task_popup(self):
        """
        Menu to select which task to delete
        """
        popup = tk.Toplevel()
        popup.wm_title("Delete Task")

        frame = tk.Frame(popup)
        frame.grid(row=1, column=0)

        del_listbox = tk.Listbox(frame, bg="SystemButtonFace")
        del_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
        del_listbox.config(yscrollcommand=scrollbar.set)

        scrollbar.config(command=del_listbox.yview)

        task_id_list = []
        for key, val in self.task_dict.items():
            task_id_list.append(key)
            del_listbox.insert(tk.END, val["name"])
        
        tk.Button(popup, text="Delete", font=('Arial', 16), command=lambda:[self._del_task_yesno(task_id_list[del_listbox.curselection()[0]])]).grid(row=2, column=0)

    def _edit_task_validate(self, task_dict, task_id, popup):
        """
        Validates date input for edit task submission

        Input: task (dict), task_id (str), edit task popup menu (tk.Toplevel() object)
        """
        if self._date_correct(task_dict["datetime"][0:10]) and self._time_correct(task_dict["datetime"][-5:]):
            self._update_task(task_dict, task_id)
            popup.destroy()
            self._init_list()
        else:
            messagebox.showinfo('Invalid Input', 'Error: Invalid Date/Time Input!')

    def _edit_task_edit_popup(self, task_id):
        """
        Menu to edit old task

        Input: task_id (str)
        """
        popup = tk.Toplevel()
        popup.wm_title("Edit Task")

        tk.Label(popup, text="Task Name: ", font=('Arial', 18)).grid(row=0, column=0)

        task_name_textbox = tk.Entry(popup, font=('Arial', 16))
        task_name_textbox.insert(tk.END, f'{self.task_dict[task_id]["name"]}')
        task_name_textbox.grid(row=0, column=1)

        tk.Label(popup, text="Due by (yyyy-mm-dd hh:mm): ", font=('Arial', 18)).grid(row=1, column=0)

        due_textbox = tk.Entry(popup, font=('Arial', 16))
        due_textbox.insert(tk.END, f'{self.task_dict[task_id]["datetime"]}')
        due_textbox.grid(row=1, column=1)

        tk.Button(popup, text="Update", font=('Arial', 16), command=lambda:[self._edit_task_validate({"name": task_name_textbox.get(), "datetime": due_textbox.get()}, task_id, popup)]).grid(row=2, column=0)

    def _edit_task_list_popup(self):
        """
        Menu to select which task to edit
        """
        popup = tk.Toplevel()
        popup.wm_title("Edit Task")

        frame = tk.Frame(popup)
        frame.grid(row=1, column=0)

        del_listbox = tk.Listbox(frame, bg="SystemButtonFace")
        del_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
        del_listbox.config(yscrollcommand=scrollbar.set)

        scrollbar.config(command=del_listbox.yview)
        task_id_list = []
        for key, val in self.task_dict.items():
            task_id_list.append(key)
            del_listbox.insert(tk.END, val["name"])
        
        tk.Button(popup, text="Edit Task", font=('Arial', 16), command=lambda:[self._edit_task_edit_popup(task_id_list[del_listbox.curselection()[0]])]).grid(row=2, column=0)

    def _generate_task_id(self):
        """
        Returns a task_id for a new task
        """
        self.task_counter += 1
        return str(self.task_counter)

    def _add_task_validate(self, task_dict, popup):
        """
        Validates date input for add task submission

        Input: task (dict) edit task popup menu (tk.Toplevel() object)
        """
        if self._date_correct(task_dict["datetime"][0:10]) and self._time_correct(task_dict["datetime"][-5:]):
            self._update_task(task_dict, self._generate_task_id())
            popup.destroy()
            self._init_list()
        else:
            messagebox.showinfo('Invalid Input', 'Error: Invalid Date/Time Input!')
    
    def _add_task_popup(self):
        """
        Menu to add new task
        """
        popup = tk.Toplevel()
        popup.wm_title("Add Task")

        datetime_now = datetime.datetime.now()
        datetime_now = datetime_now.strftime("%Y-%m-%d")

        tk.Label(popup, text="Task Name: ", font=('Arial', 18)).grid(row=0, column=0)

        task_name_textbox = tk.Entry(popup, font=('Arial', 16))
        
        task_name_textbox.grid(row=0, column=1)

        tk.Label(popup, text="Due by (yyyy-mm-dd hh:mm): ", font=('Arial', 18)).grid(row=1, column=0)

        due_textbox = tk.Entry(popup, font=('Arial', 16))
        due_textbox.insert(tk.END, f'{datetime_now} 23:59')
        due_textbox.grid(row=1, column=1)

        tk.Button(popup, text="Add", font=('Arial', 16), command=lambda:[self._add_task_validate({"name": task_name_textbox.get(), "datetime": due_textbox.get()}, popup)]).grid(row=2, column=0)

    def _init_list(self):
        """
        Updates daily task list and weekly task list based on app's date
        """
        self.listbox.delete(0, tk.END)
        task_list = self._get_date_tasks(self.app_date)
        for task in task_list:
            self.listbox.insert(tk.END, task["name"])

        self.listbox_week.delete(0, tk.END)
        task_dict = self._get_week_tasks(self.app_date)
        for day in task_dict.values():
            for task in day:
                self.listbox_week.insert(tk.END, task["name"])

    def _update_sun(self):
        """
        Updates greeting message based on what is the app's time
        """
        if int(self.app_time[:2]) < 12:
            self.sun = "MORNING"
        elif int(self.app_time[:2]) < 18:
            self.sun = "AFTERNOON"
        else:
            self.sun = "EVENING"
        self.greeting_message.set(f"GOOD {self.sun} {self.user_name}!!")
    
    def _update_name(self, new_name):
        """
        Updates the user's name

        Input: new user name (str)
        """
        self.user_name = new_name
        self.greeting_message.set(f"GOOD {self.sun} {self.user_name}!!")

    def _edit_name(self):
        """
        Menu to edit user's name
        """
        popup = tk.Toplevel()
        popup.wm_title("Edit Name")

        tk.Label(popup, text="Enter your name", font=('Arial', 18)).grid(row=0, column=0)
        
        textbox = tk.Entry(popup, font=('Arial', 16))
        textbox.grid(row=1, column=0)

        tk.Button(popup, text="Update", font=('Arial', 16), command=lambda:[self._update_name(textbox.get()), popup.destroy()]).grid(row=2, column=0)

    def _save_all(self):
        """
        Saves all data into json file
        """
        data = {
            "settings": {
                "name": self.user_name,
                "task_counter": self.task_counter,
                "completed_counter": self.completed_counter
            },
            "tasks": self.task_dict
        }
        with open(self.config_path, 'w') as file:
            json.dump(data, file, indent=4)

    def _on_close(self):
        """
        Quit confirmation message, also runs save all before quitting
        """
        if messagebox.askyesno(title="Quit", message="Do you really want to quit?"):
            self._save_all()
            self.root.destroy()

    def _edit_date_validate(self, date, popup):
        """
        Validates edit date date input

        Input: date (str), edit date popup (tk.Toplevel() object)
        """
        if self._date_correct(date):
            self._update_date(date)
            popup.destroy()
        else:
            messagebox.showinfo('Invalid Input', 'Error: Invalid Date Input!')
        
    def _edit_date(self):
        """
        Menu to edit app's date
        """
        popup = tk.Toplevel()
        popup.wm_title("Edit Date")

        tk.Label(popup, text="Enter a new date (YYYY-MM-DD)", font=('Arial', 18)).grid(row=0, column=0)

        textbox = tk.Entry(popup, font=('Arial', 16))
        textbox.grid(row=1, column=0)

        tk.Button(popup, text="Update", font=('Arial', 16), command=lambda:[self._edit_date_validate(textbox.get(), popup)]).grid(row=2, column=0)

    def _edit_time_validate(self, inp_time, popup):
        """
        Validates edit time input

        Input: time (str), edit date popup (tk.Toplevel() object)
        """
        if self._time_correct(inp_time):
            self._update_time(inp_time)
            popup.destroy()
        else:
            messagebox.showinfo('Invalid Input', 'Error: Invalid Time Input!')

    def _edit_time(self):
        """
        Menu to edit app's time
        """
        popup = tk.Toplevel()
        popup.wm_title("Edit Time")

        tk.Label(popup, text="Enter a new time (HH:MM)", font=('Arial', 18)).grid(row=0, column=0)

        textbox = tk.Entry(popup, font=('Arial', 16))
        textbox.grid(row=1, column=0)

        tk.Button(popup, text="Update", font=('Arial', 16), command=lambda:[self._edit_time_validate(textbox.get(), popup)]).grid(row=2, column=0)
        
    def _task_review(self):
        """
        Menu to show weekly performance report
        """
        popup = tk.Toplevel()
        popup.wm_title("Your Performance Report")

        fig = Figure(figsize = (5, 5), dpi = 100)
        y_axis_names = [3, 2, 1, 3, 4, 2, 1]
        x_axis_names = ['mon', 'tues', 'wed', 'thur', 'fri', 'sat', 'sun']
        plot1 = fig.add_subplot(111)
        plot1.plot(x_axis_names, y_axis_names)
        canvas = FigureCanvasTkAgg(fig, popup)  
        canvas.draw()
        canvas.get_tk_widget().pack()
    
        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(canvas, popup)
        toolbar.update()
    
        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().pack()

    def _generate_completed_id(self):
        self.completed_counter += 1
        return self.completed_counter

    def _check_completed(self):
        pass

    def _progressvalue(self):
        completionpercent = (self.completed_counter/self.task_counter)*100
        return completionpercent
    
    def _update_progress_label(self):
        return f"Current Progress: {self.progressbar['value']}%"

    def _progress(self):
        if self.progressbar['value'] < 100:
            self.progressbar['value'] = self._progressvalue()
            self.value_label['text'] = self._update_progress_label()
        else:
            self.value_label['text'] = 'All Tasks completed today!'

def create_config(config_path):
    """
    Create a config file in given path

    Input: config file path
    """
    config = {
        "settings": {
            "name": "",
            "task_counter": 0,
            "completed_counter": 0
        },
        "tasks": {},
    }

    with open(config_path, 'w') as file:
        json.dump(config, file)

def load_config(config_path):
    """
    Loads a config file in given path

    Input: config file path
    """
    with open(config_path, 'r') as file:
        data = json.load(file)
        
    return data

if __name__ == "__main__":

    config_path = 'config\\data.json'

    if not os.path.isfile(config_path):
        create_config(config_path)
    
    data = load_config(config_path)

    manager = Manager(data, config_path)

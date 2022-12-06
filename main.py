import datetime
import json
import os
import time
import tkinter as tk
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
        editimg = Image.open('assets\\edit.png')
        editimg = editimg.resize((20, 20))
        edit = ImageTk.PhotoImage(editimg)
        deleteimg = Image.open('assets\\delete.png')
        deleteimg = deleteimg.resize((20, 20))
        delete = ImageTk.PhotoImage(deleteimg)

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
                ).grid(row=0, column=0, padx=2, pady=2)

        """
        Uncomment this for Time Demo purposes.
        """
        # tk.Label(self.root,
        #         textvariable=self.time_message,
        #         font=('Arial', 18)
        #         ).grid(row=0, column=4, padx=2, pady=2)

        tk.Label(self.root, textvariable=self.greeting_message, font=('Arial Rounded MT Bold', 18)).grid(row=1, column=0, padx=2, pady=2)

        tk.Label(self.root, text="What do you want to achieve today?", font=('Arial', 18)).grid(row=2, column=0, padx=2, pady=2)

        ttk.Button(self.root, image=add, command=self._add_task_popup).grid(row=2, column=1, padx=2, pady=2)

        ttk.Button(self.root, image=edit, command=self._edit_task_list_popup).grid(row=2, column=2, padx=2, pady=2)

        ttk.Button(self.root, image=delete, command=self._del_task_popup).grid(row=2, column=3, padx=2, pady=2)

        ttk.Button(self.root, text="View your Weekly Performance Report", command=self._task_review).grid(row=4, column=4, padx=2, pady=2)
        
        frame1 = tk.Frame(self.root)
        frame1.grid(row=4, column=0, padx=2, pady=2)

        self.progressbar = ttk.Progressbar(frame1, orient='horizontal', mode='determinate', length=280)
        self.progressbar.pack(side=tk.LEFT, fill=tk.BOTH)

        self.value_label = ttk.Label(self.root, text=self._update_progress_label())
        self.value_label.grid(row=5, column=0, padx=2, pady=2)

        frame2 = tk.Frame(self.root)
        frame2.grid(row=3, column=0, padx=2, pady=2)

        self.listbox = tk.Listbox(frame2, bg="SystemButtonFace")
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.listbox.bind('<Double-1>', self._complete_task_popup)
        scrollbar = tk.Scrollbar(frame2)
        scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        tk.Label(self.root, text="Upcoming Weekly Tasks", font=('Arial', 18)).grid(row=2, column=4, padx=2, pady=2)
        frame3 = tk.Frame(self.root)
        frame3.grid(row=3, column=4, padx=2, pady=2)

        self.listbox_week = tk.Listbox(frame3, bg="SystemButtonFace")
        self.listbox_week.pack(side=tk.LEFT, fill=tk.BOTH)
        self.listbox_week.bind('<Double-1>', self._complete_task_week_popup)
        scrollbar_week = tk.Scrollbar(frame3)
        scrollbar_week.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.listbox_week.config(yscrollcommand=scrollbar_week.set)
        scrollbar_week.config(command=self.listbox_week.yview)

        self._update_date(str(datetime.datetime.now().date()))
        self._update_time(str(datetime.datetime.now().strftime("%H:%M")))

        self._reset_completed()
        self._progress()
        self._update_progress_label()

        self.mascot_img_ls = []
        for i in range(7):
            dinoimg = Image.open(fr'assets\\mascots\\dino\\frame-{i}.png')
            dinoimg = dinoimg.resize((160, 220))
            self.mascot_img_ls.append(ImageTk.PhotoImage(dinoimg))
        self.mascot = tk.Label(self.root, image=self.mascot_img_ls[0])
        self.mascot.grid(row=6, column=4)
        self.mascot.bind('<Enter>', self._mascot_hover)
        self.mascot.bind('<Double-1>', self._mascot_credits)

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

    def _mascot_credits(self, _):
        """
        Triggers when mascot is double clicked and a credits popup shows
        """
        popup = tk.Toplevel()
        popup.wm_title("Credits")

        tk.Label(popup, text="Brought to you by:", font=('Arial Rounded MT Bold', 18)).grid(row=0, column=0, padx=2, pady=2)
        tk.Label(popup, text="Khoo Jing Heng (1007221)", font=('Comic Sans MS', 16)).grid(row=1, column=0, padx=2, pady=2)
        tk.Label(popup, text="Tan Hun Chong (1006643)", font=('Comic Sans MS', 16)).grid(row=2, column=0, padx=2, pady=2)
        tk.Label(popup, text="Tan Yan Lin, Charlese (1007075)", font=('Comic Sans MS', 16)).grid(row=3, column=0, padx=2, pady=2)
        tk.Label(popup, text="Janessa Kwan Su Hui (1006562)", font=('Comic Sans MS', 16)).grid(row=4, column=0, padx=2, pady=2)
        tk.Label(popup, text="Foo Yu Qian, Erika (1007023)", font=('Comic Sans MS', 16)).grid(row=5, column=0, padx=2, pady=2)

        tk.Button(popup, text="Thank You!", font=('Arial', 16), command=popup.destroy).grid(row=6, column=0, padx=2, pady=2)

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

    def _reset_completed(self):
        """
        To reset completion counter everytime add, edit, delete, complete task or update time is made
        """
        self.completed_counter = 0
        for k in self.task_dict.keys():
            if self.task_dict[k]["datetime"][0:10] == self.app_date and self.task_dict[k]["complete"] == 1:
                self.completed_counter += 1

    def _update_task(self, res, task_id):
        """
        To add new tasks into the to-do-list

        Takes in a new task as dictionary (res) and appends it to the current dictionary (task_dict)
        Output obtained would have appended res to the end of the data

        Input: new task (dict), task_id (int)
        """
        self.task_dict[task_id] = res

    def _delete_task(self, task_id):
        """
        Deletes task from task_dict based on task_id given

        Input: task_id (str)
        """
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

    def _prev_week(self, date):
        """
        Returns list of dates for the previous 7 days based on date

        Input: date (str)
        """
        date = datetime.datetime.strptime(date, "%Y-%m-%d")

        output = []
        for idx in range(7):
            prev_days = date - datetime.timedelta(days=idx)
            prev_days_str = str(prev_days)[0:10]
            output.append(prev_days_str)
        output.sort()

        return output

    def _prev_week_tasks(self, date):
        """
        Returns list of tasks for the previous 7 days based on date

        Input: date (str)
        """
        date = datetime.datetime.strptime(date, "%Y-%m-%d")

        output = []
        for idx in range(7):
                prev_days = date - datetime.timedelta(days=idx)
                prev_days_str = str(prev_days)[0:10]
                output.append(prev_days_str)
        output.sort()

        task_output = []
        for element in output:
            counter = 0
            for d_keys in self.task_dict.keys():
                if self.task_dict[d_keys]["datetime"][0:10] == element:
                    counter += 1
            task_output.append(counter)

        return task_output

    def _prev_week_completed_tasks(self, date):
        """
        Returns list of completed tasks for the previous 7 days based on date

        Input: date (str)
        """
        date = datetime.datetime.strptime(date, "%Y-%m-%d")

        output = []
        for idx in range(7):
                prev_days = date - datetime.timedelta(days=idx)
                prev_days_str = str(prev_days)[0:10]
                output.append(prev_days_str)
        output.sort()

        task_output = []
        for element in output:
            counter = 0
            for d_keys in self.task_dict.keys():
                if self.task_dict[d_keys]["datetime"][0:10] == element and self.task_dict[d_keys]["complete"] == 1:
                    counter += 1
            task_output.append(counter)

        return task_output

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

    def _del_task_yesno(self, index):
        """
        Yes/no popup to confirm task deletion

        Input: index (int)
        """
        if messagebox.askyesno(title="Delete Task", message=f'Do you really want to delete task "{self.task_dict[self.task_id_list[index]]["name"]}"?'):
            self._delete_task(self.task_id_list.pop(index))
            self.del_listbox.delete(index)
            self._init_list()

    def _del_task_popup(self):
        """
        Menu to select which task to delete
        """
        popup = tk.Toplevel()
        popup.wm_title("Delete Task")

        frame = tk.Frame(popup)
        frame.grid(row=1, column=0, padx=2, pady=2)

        self.del_listbox = tk.Listbox(frame, bg="SystemButtonFace")
        self.del_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.del_listbox.config(yscrollcommand=scrollbar.set)

        scrollbar.config(command=self.del_listbox.yview)

        self.task_id_list = []
        for key, val in self.task_dict.items():
            if datetime.datetime(int(val["datetime"][:4]), int(val["datetime"][5:7]), int(val["datetime"][8:10])) >= datetime.datetime(int(self.app_date[:4]), int(self.app_date[5:7]), int(self.app_date[8:10])):
                if val["complete"] == 0:
                    self.task_id_list.append(key)
                    self.del_listbox.insert(tk.END, val["name"])
        
        tk.Button(popup, text="Delete", font=('Arial', 16), command=lambda:[self._del_task_yesno(self.del_listbox.curselection()[0]), self._reset_completed(), self._progress()]).grid(row=2, column=0, padx=2, pady=2)

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
        popup.geometry('600x110')

        tk.Label(popup, text="Task Name: ", font=('Arial', 18)).grid(row=0, column=0)

        task_name_textbox = tk.Entry(popup, font=('Arial', 16))
        task_name_textbox.insert(tk.END, f'{self.task_dict[task_id]["name"]}')
        task_name_textbox.grid(row=0, column=1)

        tk.Label(popup, text="Due by (yyyy-mm-dd hh:mm): ", font=('Arial', 18)).grid(row=1, column=0)

        due_textbox = tk.Entry(popup, font=('Arial', 16))
        due_textbox.insert(tk.END, f'{self.task_dict[task_id]["datetime"]}')
        due_textbox.grid(row=1, column=1)

        tk.Button(popup, text="Update", font=('Arial', 16), command=lambda:[self._edit_task_validate({"complete": self.task_dict[task_id]["complete"], "name": task_name_textbox.get(), "datetime": due_textbox.get()}, task_id, popup), self._reset_completed(), self._progress()]).grid(row=2, column=0)

    def _edit_task_list_popup(self):
        """
        Menu to select which task to edit
        """
        popup = tk.Toplevel()
        popup.wm_title("Edit Task")

        frame = tk.Frame(popup)
        frame.grid(row=1, column=0, padx=2, pady=2)

        edit_listbox = tk.Listbox(frame, bg="SystemButtonFace")
        edit_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
        edit_listbox.config(yscrollcommand=scrollbar.set)

        scrollbar.config(command=edit_listbox.yview)
        task_id_list = []
        for key, val in self.task_dict.items():
            if datetime.datetime(int(val["datetime"][:4]), int(val["datetime"][5:7]), int(val["datetime"][8:10])) >= datetime.datetime(int(self.app_date[:4]), int(self.app_date[5:7]), int(self.app_date[8:10])):
                if val["complete"] == 0:
                    task_id_list.append(key)
                    edit_listbox.insert(tk.END, val["name"])
        
        tk.Button(popup, text="Edit Task", font=('Arial', 16), command=lambda:[self._edit_task_edit_popup(task_id_list[edit_listbox.curselection()[0]])]).grid(row=2, column=0, padx=2, pady=2)

    def _generate_task_id(self):
        """
        Returns a task_id for a new task
        """
        self.task_counter += 1
        return str(self.task_counter)

    def _is_completed(self, task_id):
        """
        Toggles completion of task with task_id, increments/decrements completed_counter respectively (day)

        Input: task_id (str)
        """
        if self.task_dict[task_id]["complete"] == 0:
            self.task_dict[task_id]["complete"] = 1
        elif self.task_dict[task_id]["complete"] == 1:
            self.task_dict[task_id]["complete"] = 0
    
    def _is_completed_week(self, task_id):
        """
        Toggles completion of task with task_id (week)
        
        Input: task_id (str)
        """
        if self.task_dict[task_id]["complete"] == 0:
            self.task_dict[task_id]["complete"] = 1
        elif self.task_dict[task_id]["complete"] == 1:
            self.task_dict[task_id]["complete"] = 0

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
        popup.geometry('600x110')

        datetime_now = datetime.datetime.now()
        datetime_now = datetime_now.strftime("%Y-%m-%d")

        tk.Label(popup, text="Task Name: ", font=('Arial', 18)).grid(row=0, column=0)

        task_name_textbox = tk.Entry(popup, font=('Arial', 16))
        
        task_name_textbox.grid(row=0, column=1)

        tk.Label(popup, text="Due by (yyyy-mm-dd hh:mm): ", font=('Arial', 18)).grid(row=1, column=0)

        due_textbox = tk.Entry(popup, font=('Arial', 16))
        due_textbox.insert(tk.END, f'{datetime_now} 23:59')
        due_textbox.grid(row=1, column=1)

        tk.Button(popup, text="Add", font=('Arial', 16), command=lambda:[self._add_task_validate({"complete": 0, "name": task_name_textbox.get(), "datetime": due_textbox.get()}, popup), self._reset_completed(), self._progress()]).grid(row=2, column=1, padx=2, pady=2)

    def _init_list(self):
        """
        Updates daily task list and weekly task list based on app's date and task completion condition
        """
        self.listbox.delete(0, tk.END)
        task_list = self._get_date_tasks(self.app_date)
        for task in task_list:
            if task["complete"] == 1:
                self.listbox.insert(tk.END, "☒"+task["name"])
            elif task["complete"] == 0:
                self.listbox.insert(tk.END, "☐"+task["name"])

        self.listbox_week.delete(0, tk.END)
        task_dict = self._get_week_tasks(self.app_date)
        for day in task_dict.values():
            for task in day:
                if task["complete"] == 1:
                    self.listbox_week.insert(tk.END, "☒"+task["name"])
                elif task["complete"] == 0:
                    self.listbox_week.insert(tk.END, "☐"+task["name"])

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
        self.greeting_message.set(f"GOOD {self.sun} {self.user_name}!")
    
    def _update_name(self, new_name):
        """
        Updates the user's name and capitalises it

        Input: new user name (str)
        """
        self.user_name = new_name.upper()
        self.greeting_message.set(f"GOOD {self.sun} {self.user_name}!")

    def _edit_name(self):
        """
        Menu to edit user's name
        """
        popup = tk.Toplevel()
        popup.wm_title("Edit Name")

        tk.Label(popup, text="Enter your name", font=('Arial', 18)).grid(row=0, column=0, padx=2, pady=2)
        
        textbox = tk.Entry(popup, font=('Arial', 16))
        textbox.grid(row=1, column=0, padx=2, pady=2)

        tk.Button(popup, text="Update", font=('Arial', 16), command=lambda:[self._update_name(textbox.get()), popup.destroy()]).grid(row=2, column=0, padx=2, pady=2)

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

        tk.Label(popup, text="Enter a new date (YYYY-MM-DD)", font=('Arial', 18)).grid(row=0, column=0, padx=2, pady=2)

        textbox = tk.Entry(popup, font=('Arial', 16))
        textbox.grid(row=1, column=0, padx=2, pady=2)

        tk.Button(popup, text="Update", font=('Arial', 16), command=lambda:[self._edit_date_validate(textbox.get(), popup), self._reset_completed(), self._progress()]).grid(row=2, column=0, padx=2, pady=2)

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

        tk.Label(popup, text="Enter a new time (HH:MM)", font=('Arial', 18)).grid(row=0, column=0, padx=2, pady=2)

        textbox = tk.Entry(popup, font=('Arial', 16))
        textbox.grid(row=1, column=0, padx=2, pady=2)

        tk.Button(popup, text="Update", font=('Arial', 16), command=lambda:[self._edit_time_validate(textbox.get(), popup)]).grid(row=2, column=0, padx=2, pady=2)
    
    def _task_review(self):
        """
        Menu to show weekly performance report
        .
        The code for this function was modified from the code found at
        https://www.geeksforgeeks.org/how-to-embed-matplotlib-charts-in-tkinter-gui/
        """
        popup = tk.Toplevel()
        popup.wm_title("Your Performance Report")

        x_axis_names = self._prev_week(self.app_date)
        fig1 = Figure(figsize = (8, 3), dpi = 100)
        y1_axis_names = self._prev_week_tasks(self.app_date)
        plot1 = fig1.add_subplot(111)
        plot1.plot(x_axis_names, y1_axis_names, label = "Total Daily Tasks")
        plot1.set_ylim([0, 10])
        fig1.legend()
        canvas1 = FigureCanvasTkAgg(fig1, popup)  
        canvas1.draw()
        canvas1.get_tk_widget().pack()

        fig2 = Figure(figsize = (8, 3), dpi = 100)
        y2_axis_names = self._prev_week_completed_tasks(self.app_date)
        plot2 = fig2.add_subplot(111)
        plot2.plot(x_axis_names, y2_axis_names, label = "Daily Completed Tasks")
        plot2.set_ylim([0, 10])
        fig2.legend()
        canvas2 = FigureCanvasTkAgg(fig2, popup)  
        canvas2.draw()
        canvas2.get_tk_widget().pack()
    
        toolbar2 = NavigationToolbar2Tk(canvas2, popup)
        toolbar2.update()
        canvas2.get_tk_widget().pack()

        toolbar1 = NavigationToolbar2Tk(canvas1, popup)
        toolbar1.update()
        canvas1.get_tk_widget().pack()
    
    def _mark_completed(self, task_id):
        """
        Toggles completion value for the task and re inits task list for the day
        
        Input: task_id (str)
        """
        self._is_completed(task_id)
        self._init_list()
    
    def _mark_completed_week(self, task_id):
        """
        Toggles completion value for the task and re inits task list for the week

        Input: task_id (str)
        """
        self._is_completed_week(task_id)
        self._init_list()
    
    def _complete_task_popup(self, _):
        """
        Popup to check/uncheck task completion for the day listbox
        """
        popup = tk.Toplevel()
        popup.wm_title("Complete Task")

        task_id_dd = {}
        for k, v in self.task_dict.items():
            task_id_dd.update({k: v["name"]})
            
        task_name = (self.listbox.get(self.listbox.curselection()))[1:]
        for k, v in task_id_dd.items():
             if v == task_name:
                 task_id = k

        if self.task_dict[task_id]["complete"] == 0:
            tk.Label(popup, text="Mark Task as Completed?", font=('Arial', 18)).grid(row=0, column=0)
        elif self.task_dict[task_id]["complete"] == 1:
            tk.Label(popup, text="Undo Completed Task?", font=('Arial', 18)).grid(row=0, column=0)

        tk.Button(popup, text="Yes", font=('Arial', 16), command=lambda:[self._mark_completed(task_id), popup.destroy(), self._reset_completed(), self._progress()]).grid(row=1, column=0, padx=2, pady=2)
        tk.Button(popup, text="No", font=('Arial', 16), command=lambda:[popup.destroy()]).grid(row=2, column=0, padx=2, pady=2)

    def _complete_task_week_popup(self, _):
        """
        Popup to check/uncheck task completion for the week listbox
        """
        popup = tk.Toplevel()
        popup.wm_title("Complete Task")

        task_id_dd = {}
        for k, v in self.task_dict.items():
            task_id_dd.update({k: v["name"]})
            
        task_name = (self.listbox_week.get(self.listbox_week.curselection()))[1:]
        for k, v in task_id_dd.items():
            if v == task_name:
                task_id = k

        if self.task_dict[task_id]["complete"] == 0:
            tk.Label(popup, text="Mark Task as Completed?", font=('Arial', 18)).grid(row=0, column=0)
        elif self.task_dict[task_id]["complete"] == 1:
            tk.Label(popup, text="Undo Completed Task?", font=('Arial', 18)).grid(row=0, column=0)

        tk.Button(popup, text="Yes", font=('Arial', 16), command=lambda:[self._mark_completed_week(task_id), popup.destroy()]).grid(row=1, column=0, padx=2, pady=2)
        tk.Button(popup, text="No", font=('Arial', 16), command=lambda:[popup.destroy()]).grid(row=2, column=0, padx=2, pady=2)

    def _progressvalue(self):
        """
        Returns the current completion % value
        """
        if len(self._get_date_tasks(self.app_date)):
            completionpercent = round((self.completed_counter/len(self._get_date_tasks(self.app_date)))*100, 2)
        else:
            completionpercent = 0.0
        return completionpercent
    
    def _update_progress_label(self):
        """
        Updates and returns the text string for the progress bar
        """
        return f"Current Progress: {self.progressbar['value']}%"

    def _progress(self):
        """
        Updates the values for the progress bar and the progress label
        """
        self.progressbar['value'] = self._progressvalue()
        self.value_label['text'] = self._update_progress_label()
        if self.progressbar['value'] == 100:
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

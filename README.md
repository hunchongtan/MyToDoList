# My To Do List

## Acknowledgements

This project is an undertaking of SUTD's Computational Thinking and Design (10.014) 1D Project. \
This project is done by: \
Khoo Jing Heng \
Tan Hun Chong \
Tan Yan Lin, Charlese \
Janessa Kwan Su Hui \
Foo Yu Qian, Erika

## About:

https://user-images.githubusercontent.com/87000020/216804640-c3d9c70b-882c-434f-96d5-705bb5448340.mp4

## Usage:

```
pip install -r requirements.txt
python3 main.py
```

## Description

Our software is targeted towards **mild level dementia patients**. Understanding that they have the tendency to forget about the tasks of which they are supposed to complete or whether they have consumed their medications, this remarkable innovation of our own allows users to record and complete their daily and weekly tasks through a to-do-list. Our software reflects their daily completion progress accurately and even a weekly performance report with graphs for them to track. While the ultimate goal is to improve the lives of dementia patients, this software can also sub as a normal to-do-list for other users on a daily basis. 

## Documentation

For this software, we used the following libraries: json, os, tkinter, datetime, time, matplotlib and PIL. 

**class Manager():** Manager class manages all tasks and UI elements
    
**def __init__(self, data, config_path):** This function initializes the main UI menu and attributes vars. It also takes in config_data (dict) and returns config_file_path (string)
        
**def _mascot_run(self, idx):** This recursive function takes in idx, the index of image (int) to change the mascot sprite image, producing an animated effect

**def _mascot_hover(self, _):** This function is triggered when the cursor is hovered over the mascot. The mascot will begin its animation

**def _mascot_credits(self, _):** This function is triggered when the user double clicks on the mascot and a credits popup with all members’ names will appear
        
**def _update_date(self, date):** This function takes in a date (str) and updates the app’s date based on the user’s input
      
**def _update_time(self, new_time):** This function takes in a new_time (str) and updates the app’s time based on the user’s input

**def _reset_completed(self):** This function resets the completed counter to 0 and recomputes the completed counter again through a for loop that checks for completed tasks that match the current app date (so that progress bar can be reset properly when date changed)

**def _update_task(self, res, task_id):** This function allows users to add new tasks into their to-do-list. It takes in res, a dictionary of a new task, and appends it to task_dict (int) , the current dictionary. The output obtained would have appended res to the end of the data
       
**def _delete_task(self, task_id):** This function takes in the task_id (int) based on the user’s input, allowing users to delete a specific task of their choice from the to-do-list

**def _get_date_tasks(self, date):** This function obtains the current list of tasks available for that specified date. This function takes in a date (str) based on the user’s input and returns the list of task available (in the form of a dictionary) for that specified date as stated in the current dictionary (self.task_dict) 

        lsl = []
        for keys in self.task_dict.keys():
            if self.task_dict[keys]["datetime"][0:10] == date:
                lsl.append(self.task_dict[keys])
        return lsl

**def _get_week_tasks(self,date):** This function obtains the current list of tasks available for the next 6 days, starting from the specified date. The list of tasks obtained will be stored in a dictionary. When the day ends, the system automatically appends a new list of available tasks back into the current dictionary (self.task_dict) so as to make up for the completed tasks from the previous day. This function takes in date (str) and returns a dictionary of tasks available for the next 6 days, exclusive of the specified date

**def _prev_week(self, date):** This function takes in date (str) and returns a list of dates for the previous 7 days, inclusive of the specified date, based on the user’s date input

**def _prev_week_tasks(self, date):** This function takes in date (str) and returns a list of total input tasks for the previous 7 days, inclusive of the specified date, based on the user’s date input

**def _prev_week_completed_tasks(self, date):** This function takes in date (str) and returns a list of completed tasks for the previous 7 days, inclusive of the specified date, based on the user’s date input

**def _date_correct(self, date):** This function checks if the user has managed to input a valid date string in the correct format (YYYY-MM-DD). It takes in a date (str) and returns a boolean
  
**def _time_correct(self, timestr):** This function checks if the user has managed to input a valid timestr string in the correct format (HH:MM). It takes in a timestr (str) and returns a boolean 

**def _del_task_yesno(self, index):** This function displays a yes/no popup to seek confirmation from the user for task deletion. It takes in index (int) and returns an updated dictionary of tasks 

**def _del_task_popup(self):** This function displays a popup that shows a listbox menu which allows users to select which task they wish to be deleted
        
**def _edit_task_validate(self, task_dict, task_id, popup):** This function takes in task_dict (dict), task_id (str) and popup (edit task popup menu (tk.Toplevel() object)) so as to validate the inputs given for edit task submission. If the inputs are invalid, an error message will be raised to the user

**def _edit_task_list_popup(self):** This function displays a popup that shows a listbox menu for the user to select which task they would wish to be edited
       
**def _edit_task_edit_popup(self, task_id):** This function takes in task_id (str) so as to display a menu which allows the users to edit their old tasks 

**def _generate_task_id(self):** This function returns the task_id (str) for a new task
       
**def _is_completed(self, task_id):** This function toggles the “complete” or “undo complete” flags of the daily task given by task_id and also increases or decreases _completed_counter based on its complete condition 

**def _is_completed_week(self, task_id):** This function toggles the “complete” or “undo complete” flags of the weekly task given by task_id based on its complete condition

**def _add_task_validate(self, task_dict, popup):** This function validates the date in the task_dict to be correct, destroys the popup if the time is correct. If the date in the task_dict is not valid, an error message will be raised to the user
            
**def _add_task_popup(self):** This function invokes the popup to allow the user to add a new task to the listboxes
        
**def _init_list(self):** This function updates the daily and weekly task lists based on the app’s date and task completion condition
        
**def _update_sun(self):** This function updates the greeting message in the app based on the app’s time
         
**def _update_name(self, new_name):** This function updates the relevant labels and current user’s name with a capitalised version of the string new_name
        
**def _edit_name(self):** This function invokes the popup to allow the user to edit their name on the app
        
**def _save_all(self):** This function saves all important user data into the data.json file; this data includes the tasks the user has created, the user’s name and some data counters used in the app

**def _on_close(self):** This function runs when the user exits the app and invokes a popup asking the user if they are sure. Once the user confirms that they want to close the app, the _save_all function will be called before closing to save the user’s data.
       
**def _edit_date_validate(self, date, popup):** This function validates the date given in date to be correct, destroys the date if the time is correct. If the date is not valid, an error message will be raised to the user
               
**def _edit_date(self):** This function invokes the popup to allow the user to edit the current date

**def _edit_time_validate(self, inp_time, popup):** This function validates the time given in inp_time to be correct, destroys the popup if the time is correct. If the inp_time is not valid, an error message will be raised to the user

**def _edit_time(self):** This function invokes the popup to allow the user to edit the current time
           
**def _task_review(self):** This function invokes the popup which shows 2 Matplotlib graphs detailing the total daily tasks for the week and the tasks the user completed for that week. Both graphs come with a Matplotlib toolbar for users to configure the graphs
    
**def _mark_completed(self, task_id):** This function toggles the complete flag of the day’s task given by the task_id and re inits task list for the day
    
**def _mark_completed_week(self, task_id):** This function toggles the complete flag of the week’s task given by the task_id and re inits task list for the week

**def _complete_task_popup(self, _):** This function invokes the popup menu to confirm whether the user wants to check/uncheck a given task in the “Daily Tasks” list

**def _complete_task_week_popup(self, _):** This function invokes the popup menu to confirm whether the user wants to check/uncheck a given task in the “Upcoming Weekly Tasks” list

**def _progressvalue(self):** This function calculates the daily completion % and returns the % value for the progress bar

**def _update_progress_label(self):** This function updates and returns the correct string to be used for the progress bar text label

**def _progress(self):** This function calls for both _progressvalue function and _update_progress_label functions and updates the values of the progress bar and the text label. It also accounts for the condition when the progress value hits 100 to show a “All Tasks completed today” text label below the progress bar

**def create_config(config_path):** This function will be run the first time the user opens the app, as the user does not have any previous saved data, this function will be called to generate a blank json template for the app to use later on. This function takes config_path as a string to decide where to save the json file to

**def load_config(config_path):** This function takes the location of the json data file (config_path) as a string and loads the data from that file, it then returns the loaded data as a dictionary


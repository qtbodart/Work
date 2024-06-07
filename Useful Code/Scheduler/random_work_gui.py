import random as rd
import datetime as dt
import time as t
import tkinter as tk
from tkinter import ttk

# functions
def switch_to_main():
    try:
        cur_end_time = end_time_strvar.get()
        end_time_s_intvar.set(int(cur_end_time[0:2])*3600+int(cur_end_time[3:5])*60)

        for widget in window.grid_slaves():
            widget.grid_forget()
        CS_label.grid(row=0, column=0, sticky=tk.W)
        CS_var_label.grid(row=0, column=1, sticky=tk.E)
        TL_label.grid(row=1,column=0, sticky=tk.W)
        TL_var_label.grid(row=1,column=1, sticky=tk.E)
        pause_button.grid(row=2, sticky=tk.W)

        mainLoop()
    except:
        error_strvar.set("Wrong input, try again.")

def end_loop(hours_worked):
    pass

def time():
    cur_time = str(dt.datetime.now()).split(" ")[1]
    cur_time_s_intvar.set(int(cur_time[0:2])*3600+int(cur_time[3:5])*60+int(cur_time[6:8]))
    CS_label.after(1000,time)

def get_cur_t():
    return cur_time_s_intvar.get()

def sec_to_string(secs):
    hours = secs//3600
    mins = secs//60 - hours*60
    sec = secs - hours*3600 - mins*60
    output = ""

    if hours < 10:
        output += "0"
    output += str(hours)+":"
    if mins < 10:
        output += "0"
    output += str(mins)+":"
    if sec < 10:
        output += "0"
    output += str(sec)
    
    return output

def pause_function():
    pause = pause_boolvar.get()

    if pause:
        pause_boolvar.set(False)
    else:
        pause_boolvar.set(True)

def mainLoop():
    end_time = end_time_s_intvar.get()
    cur_time = get_cur_t()
    session_end_time = CS_end_time_s_intvar.get()
    session_bool = session_boolvar.get()
    pause = pause_boolvar.get()

    # print(f"Current time : {sec_to_string(cur_time)} \tEnd time : {sec_to_string(end_time)}\tSession end time : {sec_to_string(session_end_time)}\tSession : {current_session_strvar.get()}")
    if not pause:
        if not session_bool:
            work_boolvar.set(not work_boolvar.get())
            if work_boolvar.get():
                current_session_strvar.set("work")
                duration = 1800
                while rd.choice([True,False,True]) and cur_time+duration+1800 < end_time and duration < 7200:
                    duration+=1800
                CS_end_time_s_intvar.set(cur_time+duration)
            
            else:
                current_session_strvar.set("rest")
                duration = 1800
                while not rd.choice([True,False,True]) and cur_time+duration+1800 < end_time and duration < 7200:
                    duration+=1800
                CS_end_time_s_intvar.set(cur_time+duration)
            
            session_boolvar.set(True)
        
        else:
            if session_end_time-cur_time <= 0:
                session_boolvar.set(False)
            else:
                time_left_strvar.set(sec_to_string(session_end_time-cur_time))
    else:
        CS_end_time_s_intvar.set(CS_end_time_s_intvar.get()+(get_cur_t()-cur_time)+1)
    CS_label.after(1000,mainLoop)
    

# main window
window = tk.Tk()
window.title("Schedule")

##### variables #####
## integers
cur_time_s_intvar = tk.IntVar()    # current time in seconds, updated by @time()
end_time_s_intvar = tk.IntVar()    # end of schedule in seconds
CS_end_time_s_intvar = tk.IntVar() # end of session in seconds
# time_worked_s_intvar = tk.IntVar() # time worked in seconds

## strings
end_time_strvar = tk.StringVar()                      # user input
error_strvar = tk.StringVar()                         # error string, given "Wrong input, try again." if an error is encountered
current_session_strvar = tk.StringVar(value="pause")  # string representing current user state, second window
time_left_strvar = tk.StringVar()                     # session time left, second window
time_worked_strvar = tk.StringVar()                   # time worked

## booleans
session_boolvar = tk.BooleanVar(value=True)  # Represents if the user is currently in session
pause_boolvar = tk.BooleanVar(value=False)
work_boolvar = tk.BooleanVar(value=rd.choice([True,False,True]))
#####################

###### widgets ######
# first widgets
label = ttk.Label(window, text="End of session (hh:mm) : ").grid(row=0, column=0)
error_label = ttk.Label(window, textvariable=error_strvar).grid(row=1, column=1)
entry = ttk.Entry(window,textvariable=end_time_strvar).grid(row=0,column=1)
entry_button = ttk.Button(window, text="validate", command=switch_to_main).grid(row=0,column=2) # switches to the second window after retrieving @end_time_strvar

# second widgets (CS = Current Session, TL = Time Left)
CS_label = ttk.Label(window, text="Current session : ")
CS_var_label = ttk.Label(window, textvariable=current_session_strvar)
TL_label = ttk.Label(window, text="Time left : ")
TL_var_label = ttk.Label(window, textvariable=time_left_strvar)
pause_button = ttk.Button(window, text="Pause", command=pause_function)

# last widgets

#####################

time()
CS_end_time_s_intvar.set(get_cur_t()+10)
window.mainloop()

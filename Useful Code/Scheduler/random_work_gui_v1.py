import numpy.random as rd
import datetime as dt
import tkinter as tk
from tkinter import ttk
import winsound
import time as t
import scipy.stats as stats

################  USER-DEFINED VARIABLES (modify as seen fit)  ##################
#                                                                               #
# DURATIONS                                                                     #
min_work_duration = 60   # Minimum amount of time per work session (in minutes) #
max_work_duration = 120  # Maximum amount of time per work session (in minutes) #
min_rest_duration = 30   # Minimum amount of time per rest session (in minutes) #
max_rest_duration = 60   # Maximum amount of time per rest session (in minutes) #
#                                                                               #
#                                                                               #
# PROBABILITES                                                                  #
# The amount of time spent working or resting is determined randomly,           #
# through the two variables below.                                              #
work_probability = 0.5                                                          #
rest_probability = 0.4                                                          #
# For example :                                                                 #
# work_probability = 0   -> work time likely from min to (min + max)/2          #
# work_probability = 0.5 -> work time equally distributed from min to max       #
# work_probability = 1   -> work time likely from (min + max)/2 to max          #
#                                                                               #
#                                                                               #
# CHUNKS                                                                        #
# The amount of minutes into which the work and rest intervals are sliced.      #
chunk = 5                                                                       #
# For example:                                                                  #
# min_work_duration = 60                                                        #
# max_work_duration = 120                                                       #
# chunk = 30                                                                    #
# Every work session, the code will choose a duration between : [60,90,120]     #
#                                                                               #
# OTHERS                                                                        #
#                                                                               #
# "work" and "rest" begins the schedule with this session, and "random" chooses #
begin_with = "random"                                                           #
# DEBUG                                                                         #
# prints some info on the command panel if True                                 #
debug = True                                                                    #
#################################################################################

# functions
def get_work():
    choices = [(min_work_duration+i*chunk)*60 for i in range((max_work_duration-min_work_duration)//chunk)]
    #          |____________________________|                 |__________________________________________|
    #            explained in CHUNKS above                  number of chunk that fit the interval [min,max]

    mu = (min_work_duration+work_probability*(max_work_duration-min_work_duration))*60
    sigma = 12*(max_work_duration-min_work_duration)
    print(f"mu : {mu} , sigma : {sigma}\n")
    probabilities = stats.norm.pdf(choices,mu,sigma)
    print(f"Not normalized probabilities : {probabilities}\n")
    probabilities = probabilities/(sum(probabilities))
    print(f"Choices : {choices}\nProbs : {probabilities}\n")
    return rd.choice(choices, 1, p=probabilities)[0]

def get_rest():
    choices = [(min_rest_duration+i*chunk)*60 for i in range((max_rest_duration-min_rest_duration)//chunk)]
    #          |____________________________|                 |__________________________________________|
    #            explained in CHUNKS above                  number of chunk that fit the interval [min,max]
    
    mu = (min_rest_duration+rest_probability*(max_rest_duration-min_rest_duration))*60
    sigma = 12*(max_rest_duration-min_rest_duration)
    print(f"mu : {mu} , sigma : {sigma}\n")
    probabilities = stats.norm.pdf(choices,mu,sigma)
    print(f"\nNot normalized probabilities : {probabilities}\n")
    probabilities = probabilities/(sum(probabilities))
    print(f"Choices : {choices}\nProbs : {probabilities}\n")
    return rd.choice(choices, 1, p=probabilities)[0]

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

def end_loop():
    CS_label_strvar.set("Time worked : ")
    TL_label_strvar.set("Time rested : ")
    current_session_strvar.set(sec_to_string(time_worked_ns_intvar.get()*1e-9))
    time_left_strvar.set(sec_to_string(time_played_ns_intvar.get()*1e-9))
    pause_button.grid_forget()

def time():
    cur_time = str(dt.datetime.now()).split(" ")[1]
    cur_time_s_intvar.set(int(cur_time[0:2])*3600+int(cur_time[3:5])*60+int(cur_time[6:8]))
    CS_label.after(1000,time)

def get_cur_t():
    return cur_time_s_intvar.get()

def sec_to_string(secs):
    secs = int(secs)
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
        pause_button_strvar.set("Pause")
    else:
        pause_boolvar.set(True)
        pause_button_strvar.set("Resume")

def mainLoop():
    loop_init = t.monotonic_ns()                  # Allows to tell how much time is spent in the loop
    end_time = end_time_s_intvar.get()            # End of schedule, in seconds
    cur_time = get_cur_t()                        # Current time, in seconds
    session_end_time = CS_end_time_s_intvar.get() # End of session, in seconds
    session_bool = session_boolvar.get()          # Represents current state, True means the user's currently in session
    pause = pause_boolvar.get()                   # Represents if the user's currently on pause

    # print(f"Current time : {sec_to_string(cur_time)} \tEnd time : {sec_to_string(end_time)}\tSession end time : {sec_to_string(session_end_time)}\tSession : {current_session_strvar.get()}")
    if cur_time < end_time:
        if not pause:
            if not session_bool:
                # if we're not in pause and not in session, we need to choose the next session
                work_boolvar.set(not work_boolvar.get()) # current session is set to the opposite of the last ("rest", "work")
                if work_boolvar.get():
                    # if current session is "work", we set it so and choose the time to be worked
                    current_session_strvar.set("work")
                    duration = get_work()
                    if end_time-(cur_time+duration) <= 1800: # if there's less than 30 minutes between the chosen work time and the schedule's end time,
                        CS_end_time_s_intvar.set(end_time)   # set the session's end time to the schedule's end time
                    else:
                        CS_end_time_s_intvar.set(cur_time+duration)
                
                else:
                    # if current session is "rest", we set it so and choose the time to be rested
                    current_session_strvar.set("rest")
                    duration = get_rest()
                    if end_time-(cur_time+duration) <= 1800: # if there's less than 30 minutes between the chosen rest time and the schedule's end time,
                        CS_end_time_s_intvar.set(end_time)   # set the session's end time to the schedule's end time
                    else:
                        CS_end_time_s_intvar.set(cur_time+duration)
                
                session_boolvar.set(True)
                winsound.PlaySound("pingsound",winsound.SND_FILENAME)
            
            else:
                if session_end_time-cur_time <= 0:
                    session_boolvar.set(False)
                else:
                    time_left_strvar.set(sec_to_string(session_end_time-cur_time))
                    if work_boolvar.get():
                        time_worked_ns_intvar.set(time_worked_ns_intvar.get()+(t.monotonic_ns()-loop_init)+1e9)
                    else:
                        time_played_ns_intvar.set(time_played_ns_intvar.get()+(t.monotonic_ns()-loop_init)+1e9)
        else:
            CS_end_time_s_intvar.set(CS_end_time_s_intvar.get()+(get_cur_t()-cur_time)+1)
        CS_label.after(1000,mainLoop)
    else:
        end_loop()

# main window
window = tk.Tk()
window.title("Schedule")

##### variables #####
## integers
cur_time_s_intvar = tk.IntVar()    # current time in seconds, updated by @time()
end_time_s_intvar = tk.IntVar()    # end of schedule in seconds
CS_end_time_s_intvar = tk.IntVar() # end of session in seconds
time_worked_ns_intvar = tk.IntVar() # Keeps track of the amount of time spent
time_played_ns_intvar = tk.IntVar() # working or playing, in nanoseconds

## strings
end_time_strvar = tk.StringVar()                      # user input
error_strvar = tk.StringVar()                         # error string, given "Wrong input, try again." if an error is encountered
current_session_strvar = tk.StringVar(value="pause")  # string representing current user state, second window
time_left_strvar = tk.StringVar()                     # session time left, second window
time_worked_strvar = tk.StringVar()                   # time worked
CS_label_strvar = tk.StringVar(value="Current session : ")
TL_label_strvar = tk.StringVar(value="Time left : ")
pause_button_strvar = tk.StringVar(value="Pause")

## booleans
session_boolvar = tk.BooleanVar(value=True)  # Represents if the user is currently in session
pause_boolvar = tk.BooleanVar(value=False)
work_boolvar = tk.BooleanVar(value=[True if begin_with=="work" else [False if begin_with=="pause" else bool(rd.choice([True, False]))][0]][0])
#####################

###### widgets ######
# first widgets
label = ttk.Label(window, text="End of session (hh:mm) : ").grid(row=0, column=0)
error_label = ttk.Label(window, textvariable=error_strvar).grid(row=1, column=1)
entry = ttk.Entry(window,textvariable=end_time_strvar).grid(row=0,column=1)
entry_button = ttk.Button(window, text="validate", command=switch_to_main).grid(row=0,column=2) # switches to the second window after retrieving @end_time_strvar

# second widgets (CS = Current Session, TL = Time Left)
CS_label = ttk.Label(window, textvariable=CS_label_strvar)
CS_var_label = ttk.Label(window, textvariable=current_session_strvar)
TL_label = ttk.Label(window, textvariable=TL_label_strvar)
TL_var_label = ttk.Label(window, textvariable=time_left_strvar)
pause_button = ttk.Button(window, textvariable=pause_button_strvar, command=pause_function)

# last widgets

#####################

time()
CS_end_time_s_intvar.set(get_cur_t()+10)
window.mainloop()
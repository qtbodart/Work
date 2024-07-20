import numpy.random as rd
import datetime as dt
import tkinter as tk
from tkinter import ttk
import winsound
import time as t
import scipy.stats as stats
import json

# getting scheduler settings from .json file
with open("settings.json","r") as file:
    settings = json.load(file)
settings_keys = (list)(settings.keys())

class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Schedule")

        #### Settings variables ####
        self.min_work_duration = settings["min_work_duration"]  
        self.max_work_duration = settings["max_work_duration"]  
        self.min_rest_duration = settings["min_rest_duration"]  
        self.max_rest_duration = settings["max_rest_duration"]   

        self.work_probability = settings["work_probability"]
        self.rest_probability = settings["rest_probability"]

        self.chunk = settings["chunk"]

        self.begin_with = settings["begin_with"]

        self.debug = settings["debug"]

        ####### TK variables #######
        ## integers
        self.cur_time_s_intvar = tk.IntVar()    # current time in seconds, updated by @time()
        self.end_time_s_intvar = tk.IntVar()    # end of schedule in seconds
        self.CS_end_time_s_intvar = tk.IntVar() # end of session in seconds
        self.time_worked_ns_intvar = tk.IntVar(value=0) # Keeps track of the amount of time spent
        self.time_played_ns_intvar = tk.IntVar(value=0) # working or playing, in nanoseconds

        ## strings
        self.end_time_strvar = tk.StringVar()                      # user input
        self.error_strvar = tk.StringVar()                         # error string, given "Wrong input, try again." if an error is encountered
        self.current_session_strvar = tk.StringVar(value="pause")  # string representing current user state, second window
        self.time_left_strvar = tk.StringVar()                     # session time left, second window
        self.time_worked_strvar = tk.StringVar()                   # time worked
        self.CS_label_strvar = tk.StringVar(value="   Current session : ")
        self.TL_label_strvar = tk.StringVar(value="   Time left : ")
        self.pause_button_strvar = tk.StringVar(value="Pause")

        ## booleans
        self.session_boolvar = tk.BooleanVar(value=True)  # Represents if the user is currently in session
        self.pause_boolvar = tk.BooleanVar(value=False)
        self.work_boolvar = tk.BooleanVar(value=[True if self.begin_with=="work" else [False if self.begin_with=="pause" else bool(rd.choice([True, False]))][0]][0])
        self.stop_boolvar = tk.BooleanVar(value=False)

        ########## widgets #########
        # first widgets
        self.menu_bar = tk.Menu(self.window)
        self.menu_settings = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_timing = tk.Menu(self.menu_bar, tearoff=0)
        self.label = ttk.Label(self.window, text="  End of session (hh:mm) : ").grid(row=0, column=0)
        self.error_label = ttk.Label(self.window, textvariable=self.error_strvar).grid(row=1, column=1)
        self.entry = ttk.Entry(self.window,textvariable=self.end_time_strvar).grid(row=0,column=1)
        self.entry_button = ttk.Button(self.window, text="validate", command=self.switch_to_main).grid(row=0,column=2) # switches to the second window after retrieving @end_time_strvar

        # second widgets (CS = Current Session, TL = Time Left)
        self.CS_label = ttk.Label(self.window, textvariable=self.CS_label_strvar)
        self.CS_var_label = ttk.Label(self.window, textvariable=self.current_session_strvar)
        self.TL_label = ttk.Label(self.window, textvariable=self.TL_label_strvar)
        self.TL_var_label = ttk.Label(self.window, textvariable=self.time_left_strvar)
        self.pause_button = ttk.Button(self.window, textvariable=self.pause_button_strvar, command=self.pause_function)
        self.stop_button = ttk.Button(self.window, text="Stop", command=self.stop_function)

        self.window.config(menu=self.menu_bar)
        self.menu_bar.add_cascade(label="Settings",menu=self.menu_settings)
        self.menu_bar.add_cascade(label="Timing",menu=self.menu_timing)
        self.menu_settings.add_command(label="Begin session with ...")
        self.menu_timing.add_command(label="Min. time worked")
        self.menu_timing.add_command(label="Max. time worked")
        self.menu_timing.add_command(label="Min. time rested")
        self.menu_timing.add_command(label="Max. time rested")

        self.time()
        self.CS_end_time_s_intvar.set(self.get_cur_t()+1)
        self.window.mainloop()
    

    def get_work(self):
        choices = [(self.min_work_duration+i*self.chunk)*60 for i in range((self.max_work_duration-self.min_work_duration)//self.chunk+1)]
        #          |____________________________|                 |__________________________________________|
        #            explained in CHUNKS above                  number of chunk that fit the interval [min,max]

        mu = (self.min_work_duration+self.work_probability*(self.max_work_duration-self.min_work_duration))*60
        sigma = 12*(self.max_work_duration-self.min_work_duration)
        probabilities = stats.norm.pdf(choices,mu,sigma)
        probabilities = probabilities/(sum(probabilities))
        if self.debug:
            print(f"mu : {mu} , sigma : {sigma}")
            print(f"Choices : {[i//60 for i in choices]}\nProbs : {probabilities*100}\n")
        return rd.choice(choices, 1, p=probabilities)[0]

    def get_rest(self):
        choices = [(self.min_rest_duration+i*self.chunk)*60 for i in range((self.max_rest_duration-self.min_rest_duration)//self.chunk+1)]
        #          |____________________________|                 |__________________________________________|
        #            explained in CHUNKS above                  number of chunk that fit the interval [min,max]
        
        mu = (self.min_rest_duration+self.rest_probability*(self.max_rest_duration-self.min_rest_duration))*60
        sigma = 12*(self.max_rest_duration-self.min_rest_duration)
        probabilities = stats.norm.pdf(choices,mu,sigma)
        probabilities = probabilities/(sum(probabilities))
        if self.debug:
            print(f"mu : {mu} , sigma : {sigma}")
            print(f"Choices : {[i//60 for i in choices]}\nProbs : {probabilities}\n")
        return rd.choice(choices, 1, p=probabilities)[0]

    def switch_to_main(self):
        try:
            cur_end_time = self.end_time_strvar.get()
            self.end_time_s_intvar.set(int(cur_end_time[0:2])*3600+int(cur_end_time[3:5])*60)

            for widget in self.window.grid_slaves():
                widget.grid_forget()
            self.CS_label.grid(row=0, column=0, sticky=tk.W)
            self.CS_var_label.grid(row=0, column=1, sticky=tk.E)
            self.TL_label.grid(row=1,column=0, sticky=tk.W)
            self.TL_var_label.grid(row=1,column=1, sticky=tk.E)
            self.pause_button.grid(row=2, column=0, sticky=tk.W)
            self.stop_button.grid(row=2, column=1, sticky=tk.E)

            self.mainLoop()
        except:
            
            self.error_strvar.set("Wrong input, try again.")

    def end_loop(self):
        self.CS_label_strvar.set("Time worked : ")
        self.TL_label_strvar.set("Time rested : ")
        self.current_session_strvar.set(self.sec_to_string(self.time_worked_ns_intvar.get()*1e-9))
        self.time_left_strvar.set(self.sec_to_string(self.time_played_ns_intvar.get()*1e-9))
        self.pause_button.grid_forget()
        self.stop_button.grid_forget()

    def time(self):
        cur_time = str(dt.datetime.now()).split(" ")[1]
        self.cur_time_s_intvar.set(int(cur_time[0:2])*3600+int(cur_time[3:5])*60+int(cur_time[6:8]))
        self.CS_label.after(1000,self.time)

    def get_cur_t(self):
        return self.cur_time_s_intvar.get()

    def sec_to_string(self, secs):
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

    def pause_function(self):
        pause = self.pause_boolvar.get()

        if pause:
            self.pause_boolvar.set(False)
            self.pause_button_strvar.set("Pause")
        else:
            self.pause_boolvar.set(True)
            self.pause_button_strvar.set("Resume")

    def stop_function(self):
        self.stop_boolvar.set(True)

    def mainLoop(self):
        loop_init = t.monotonic_ns()                  # Allows to tell how much time is spent in the loop
        end_time = self.end_time_s_intvar.get()            # End of schedule, in seconds
        cur_time = self.get_cur_t()                        # Current time, in seconds
        session_end_time = self.CS_end_time_s_intvar.get() # End of session, in seconds
        session_bool = self.session_boolvar.get()          # Represents current state, True means the user's currently in session
        pause = self.pause_boolvar.get()                   # Represents if the user's currently on pause
        stopped = self.stop_boolvar.get()

        # print(f"Current time : {sec_to_string(cur_time)} \tEnd time : {sec_to_string(end_time)}\tSession end time : {sec_to_string(session_end_time)}\tSession : {current_session_strvar.get()}")
        if cur_time < end_time and not stopped:
            if not pause:
                if not session_bool:
                    # if we're not in pause and not in session, we need to choose the next session
                    self.work_boolvar.set(not self.work_boolvar.get()) # current session is set to the opposite of the last ("rest", "work")
                    if self.work_boolvar.get():
                        # if current session is "work", we set it so and choose the time to be worked
                        self.current_session_strvar.set("work")
                        duration = self.get_work()
                        if end_time-(cur_time+duration) <= 1800: # if there's less than 30 minutes between the chosen work time and the schedule's end time,
                            self.CS_end_time_s_intvar.set(end_time)   # set the session's end time to the schedule's end time
                        else:
                            self.CS_end_time_s_intvar.set(cur_time+duration)
                    
                    else:
                        # if current session is "rest", we set it so and choose the time to be rested
                        self.current_session_strvar.set("rest")
                        duration = self.get_rest()
                        if end_time-(cur_time+duration) <= 1800: # if there's less than 30 minutes between the chosen rest time and the schedule's end time,
                            self.CS_end_time_s_intvar.set(end_time)   # set the session's end time to the schedule's end time
                        else:
                            self.CS_end_time_s_intvar.set(cur_time+duration)
                    
                    self.session_boolvar.set(True)
                    winsound.PlaySound("pingsound",winsound.SND_FILENAME)
                
                else:
                    if session_end_time-cur_time <= 0:
                        self.session_boolvar.set(False)
                    else:
                        if self.debug:
                            print(f"Time worked : {self.sec_to_string(self.time_worked_ns_intvar.get()*1e-9)}   Time rested : {self.sec_to_string(self.time_played_ns_intvar.get()*1e-9)}", end="\r")
                        self.time_left_strvar.set(self.sec_to_string(session_end_time-cur_time))
                        if self.work_boolvar.get():
                            self.time_worked_ns_intvar.set(self.time_worked_ns_intvar.get()+(t.monotonic_ns()-loop_init)+1e9)
                        else:
                            self.time_played_ns_intvar.set(self.time_played_ns_intvar.get()+(t.monotonic_ns()-loop_init)+1e9)
            else:
                self.CS_end_time_s_intvar.set(self.CS_end_time_s_intvar.get()+(self.get_cur_t()-cur_time)+1)
            self.CS_label.after(1000,self.mainLoop)
        else:
            self.end_loop()
    

if __name__ == "__main__":
    GUI()
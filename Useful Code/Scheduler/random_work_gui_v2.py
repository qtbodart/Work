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
print(settings_keys)
setting_description = {
    "min_work_duration" : "Minimum amount of time per work session (in minutes)",
    "max_work_duration" : "Maximum amount of time per work session (in minutes)",
    "min_rest_duration" : "Minimum amount of time per rest session (in minutes)",
    "max_rest_duration" : "Maximum amount of time per rest session (in minutes)",
    "work_probability"  : "Value between 0 and 1. Shifts the time probabilities of a work session. \nFor example, if close to 0, work sessions will likely last \"min_work_duration\" minutes",
    "rest_probability"  : "Value between 0 and 1. Shifts the time probabilities of a rest session. \nFor example, if close to 1, rest sessions will likely last \"max_rest_duration\" minutes",
    "chunk"             : "Work and rest session durations will be multiples of this value",
    "begin_with"        : "Either \"work\", \"rest\" or \"random\". \nThe schedule will begin with the selected type of session",
    "debug"             : "Prints data about the probabilities on the console"
}   

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
        self.label = ttk.Label(self.window, text="  End of session (hh:mm) : ").grid(row=0, column=0)
        self.error_label = ttk.Label(self.window, textvariable=self.error_strvar).grid(row=1, column=1)
        self.entry = ttk.Entry(self.window,textvariable=self.end_time_strvar).grid(row=0,column=1)
        self.entry_button = ttk.Button(self.window, text="validate", command=self.switch_to_main).grid(row=0,column=2) # switches to the second window after retrieving @end_time_strvar

        # second widgets (CS = Current Session, TL = Time Left)
        self.content = ttk.Frame(self.window, border=2, relief='groove')
        self.CS_label = ttk.Label(self.content, textvariable=self.CS_label_strvar)
        self.CS_var_label = ttk.Label(self.content, textvariable=self.current_session_strvar)
        self.TL_label = ttk.Label(self.content, textvariable=self.TL_label_strvar)
        self.TL_var_label = ttk.Label(self.content, textvariable=self.time_left_strvar)
        self.pause_button = ttk.Button(self.content, textvariable=self.pause_button_strvar, command=self.pause_function)
        self.stop_button = ttk.Button(self.content, text="Stop", command=self.stop_function)

        ### Menu config ###
        self.menu_bar = tk.Menu(self.window,bg='blue',fg='white')
        self.menu_settings = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_timing = tk.Menu(self.menu_bar, tearoff=0)

        self.window.config(menu=self.menu_bar)
        self.menu_bar.add_cascade(label="Settings",menu=self.menu_settings)
        self.menu_settings.add_command(label="Set settings", command=self.set_settings)

        ### Initialization ###
        self.time()
        self.CS_end_time_s_intvar.set(self.get_cur_t()+1)
        self.window.mainloop()

    def set_settings(self):
        # initializing new window
        self.new_window = tk.Toplevel()
        self.new_window.title("Settings")

        ##### SETTINGS WIDGETS/VARIABLES #####
        # min_work_duration
        minwd_frame = ttk.Frame(self.new_window)
        self.minwd_entry_strvar = tk.StringVar(self.new_window, value=self.min_work_duration)
        minwd_entry = ttk.Entry(minwd_frame, textvariable=self.minwd_entry_strvar)
        minwd_label = ttk.Label(minwd_frame, text="min_work_duration")
        minwd_description = ttk.Label(minwd_frame, text=setting_description["min_work_duration"])
        minwd_label.grid(row=0, column=0, sticky=tk.W)
        minwd_entry.grid(row=0, column=1, sticky=tk.E)
        minwd_description.grid(row = 1, columnspan=2, sticky=tk.W)

        # max_work_duration
        maxwd_frame = ttk.Frame(self.new_window)
        self.maxwd_entry_strvar = tk.StringVar(self.new_window, value=self.max_work_duration)
        maxwd_entry = ttk.Entry(maxwd_frame, textvariable=self.maxwd_entry_strvar)
        maxwd_label = ttk.Label(maxwd_frame, text="max_work_duration")
        maxwd_description = ttk.Label(maxwd_frame, text=setting_description["max_work_duration"])
        maxwd_label.grid(row=0, column=0, sticky=tk.W)
        maxwd_entry.grid(row=0, column=1, sticky=tk.E)
        maxwd_description.grid(row = 1, columnspan=2, sticky=tk.W)

        # min_rest_duration
        minrd_frame = ttk.Frame(self.new_window)
        self.minrd_entry_strvar = tk.StringVar(self.new_window, value=self.min_rest_duration)
        minrd_entry = ttk.Entry(minrd_frame, textvariable=self.minrd_entry_strvar)
        minrd_label = ttk.Label(minrd_frame, text="min_rest_duration")
        minrd_description = ttk.Label(minrd_frame, text=setting_description["min_rest_duration"])
        minrd_label.grid(row=0, column=0, sticky=tk.W)
        minrd_entry.grid(row=0, column=1, sticky=tk.E)
        minrd_description.grid(row = 1, columnspan=2, sticky=tk.W)

        # max_rest_duration
        maxrd_frame = ttk.Frame(self.new_window)
        self.maxrd_entry_strvar = tk.StringVar(self.new_window, value=self.max_rest_duration)
        maxrd_entry = ttk.Entry(maxrd_frame, textvariable=self.maxrd_entry_strvar)
        maxrd_label = ttk.Label(maxrd_frame, text="max_rest_duration")
        maxrd_description = ttk.Label(maxrd_frame, text=setting_description["max_rest_duration"])
        maxrd_label.grid(row=0, column=0, sticky=tk.W)
        maxrd_entry.grid(row=0, column=1, sticky=tk.E)
        maxrd_description.grid(row = 1, columnspan=2, sticky=tk.W)

        # work_probability
        wp_frame = ttk.Frame(self.new_window)
        self.wp_entry_strvar = tk.StringVar(self.new_window, value=self.work_probability)
        wp_entry = ttk.Entry(wp_frame, textvariable=self.wp_entry_strvar)
        wp_label = ttk.Label(wp_frame, text="work_probability")
        wp_description = ttk.Label(wp_frame, text=setting_description["work_probability"])
        wp_label.grid(row=0, column=0, sticky=tk.W)
        wp_entry.grid(row=0, column=1, sticky=tk.E)
        wp_description.grid(columnspan=2, rowspan=2, sticky=tk.NSEW)

        # rest_probability
        rp_frame = ttk.Frame(self.new_window)
        self.rp_entry_strvar = tk.StringVar(self.new_window, value=self.rest_probability)
        rp_entry = ttk.Entry(rp_frame, textvariable=self.rp_entry_strvar)
        rp_label = ttk.Label(rp_frame, text="rest_probability")
        rp_description = ttk.Label(rp_frame, text=setting_description["rest_probability"])
        rp_label.grid(row=0, column=0, sticky=tk.W)
        rp_entry.grid(row=0, column=1, sticky=tk.E)
        rp_description.grid(columnspan=2, rowspan=2, sticky=tk.NSEW)

        # chunk
        chunk_frame = ttk.Frame(self.new_window)
        self.chunk_entry_strvar = tk.StringVar(self.new_window, value=self.chunk)
        chunk_entry = ttk.Entry(chunk_frame, textvariable=self.chunk_entry_strvar)
        chunk_label = ttk.Label(chunk_frame, text="chunk")
        chunk_description = ttk.Label(chunk_frame, text=setting_description["chunk"])
        chunk_label.grid(row=0, column=0, sticky=tk.W)
        chunk_entry.grid(row=0, column=1, sticky=tk.E)
        chunk_description.grid(columnspan=2, rowspan=2, sticky=tk.NSEW)

        # begin_with
        bw_frame = ttk.Frame(self.new_window)
        self.bw_entry_strvar = tk.StringVar(self.new_window, value=self.begin_with)
        bw_entry = ttk.Entry(bw_frame, textvariable=self.bw_entry_strvar)
        bw_label = ttk.Label(bw_frame, text="begin_with")
        bw_description = ttk.Label(bw_frame, text=setting_description["begin_with"])
        bw_label.grid(row=0, column=0, sticky=tk.W)
        bw_entry.grid(row=0, column=1, sticky=tk.E)
        bw_description.grid(columnspan=2, rowspan=2, sticky=tk.NSEW)

        # debug
        debug_frame = ttk.Frame(self.new_window)
        self.debug_entry_strvar = tk.StringVar(self.new_window, value=self.debug)
        debug_entry = ttk.Entry(debug_frame, textvariable=self.debug_entry_strvar)
        debug_label = ttk.Label(debug_frame, text="debug")
        debug_description = ttk.Label(debug_frame, text=setting_description["debug"])
        debug_label.grid(row=0, column=0, sticky=tk.W)
        debug_entry.grid(row=0, column=1, sticky=tk.E)
        debug_description.grid(columnspan=2, rowspan=2, sticky=tk.NSEW)

        # save button
        save_button = ttk.Button(self.new_window, text="Save", command=self.save_settings)

        # grid manager
        minwd_frame.grid(pady=10, sticky=tk.W)
        maxwd_frame.grid(pady=10, sticky=tk.W)
        minrd_frame.grid(pady=10, sticky=tk.W)
        maxrd_frame.grid(pady=10, sticky=tk.W)
        wp_frame.grid(pady=10, sticky=tk.W)
        rp_frame.grid(pady=10, sticky=tk.W)
        chunk_frame.grid(pady=10, sticky=tk.W)
        bw_frame.grid(pady=10, sticky=tk.W)
        debug_frame.grid(pady=10, sticky=tk.W)
        save_button.grid(pady=10, sticky=tk.W)

        # putting new window on top
        self.new_window.attributes('-topmost', True)
        self.new_window.update()
        self.new_window.attributes('-topmost', False)

    def save_settings(self):
        # min_work_duration
        self.min_work_duration = int(self.minwd_entry_strvar.get())
        settings["min_work_duration"] = self.min_work_duration

        # max_work_duration
        self.max_work_duration = int(self.maxwd_entry_strvar.get())
        settings["max_work_duration"] = self.max_work_duration

        # min_rest_duration
        self.min_rest_duration = int(self.minrd_entry_strvar.get())
        settings["min_rest_duration"] = self.min_rest_duration

        # max_work_duration
        self.max_rest_duration = int(self.maxrd_entry_strvar.get())
        settings["max_rest_duration"] = self.max_work_duration

        # work_probability
        self.work_probability = float(self.wp_entry_strvar.get())
        settings["work_probability"] = self.work_probability

        # rest_probability
        self.rest_probability = float(self.rp_entry_strvar.get())
        settings["rest_probability"] = self.rest_probability

        # chunk
        self.chunk = int(self.chunk_entry_strvar.get())
        settings["chunk"] = self.chunk

        # begin_with
        self.begin_with = self.bw_entry_strvar.get()
        settings["begin_with"] = self.begin_with

        # debug
        self.debug = int(self.debug_entry_strvar.get())
        settings["debug"] = self.debug

        with open("settings.json", "w") as file:
            newData = json.dumps(settings, indent=4)
            print(newData)
            file.write(newData)


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
            print(f"Choices : {[i//60 for i in choices]}\nProbs : {[probability*100 for probability in probabilities]}\n")
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
            print(f"Choices : {[i//60 for i in choices]}\nProbs : {[probability*100 for probability in probabilities]}\n")
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
            self.content.pack()
            self.window.config(bg='grey')
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
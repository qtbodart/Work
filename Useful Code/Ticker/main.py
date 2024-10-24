from datetime import datetime
import time as t
import numpy as np 
import sounddevice as sd 

time_interval = 5
check_frequency = 2

def bip(freq, dur, a=0, d=0, s=1, r=0):
    t=np.arange(0,dur,1/44100)
    env=np.interp(t, [0, a, (a+d), dur-r, dur], [0, 1, s, s, 0])
    sound=np.sin(2*np.pi*freq*t)*env
    sd.play(sound, samplerate=44100)

while True:
    time = str(datetime.now())
    hours, minutes, seconds = [int(hms) for hms in time[11:19].split(":")]
    if (minutes%time_interval == 0 and seconds<check_frequency):
        bip(1000, .5)
    print(f"{"0" if hours<10 else ""}{hours}:{"0" if minutes<10 else ""}{minutes}", end='\r')
    t.sleep(check_frequency)
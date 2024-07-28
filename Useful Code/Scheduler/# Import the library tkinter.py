from tkinter import *
root = Tk()
root.title("hello")
top = Toplevel()
top.title("Python")
top.attributes('-topmost', True)
top.update()
top.attributes('-topmost', False)
top.mainloop()
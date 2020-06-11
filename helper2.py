import tkinter as tk
from consts import *
root = tk.Tk()
T = tk.Text(root)
T.pack()
T.insert(tk.END, WELCOME_MESSAGE)
T.config(state=tk.DISABLED)
tk.mainloop()
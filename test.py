from tkinter import *

root = Tk()
canvas = Canvas(root, bg="white")
canvas.grid(row=0, column=0)
canvas.create_rectangle(0, 0, 50, 50)
canvas.create_rectangle(50, 0, 50, 50)
canvas.create_rectangle(100, 0, 50, 50)
canvas.create_rectangle(150, 0, 50, 50)
canvas.create_rectangle(200, 0, 50, 50)
button_start = Button(root, text="Play")
button_start.grid(row=0, column=1)
root.mainloop()

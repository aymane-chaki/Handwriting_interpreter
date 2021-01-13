from tkinter import *

canvas_width = 600
canvas_height = 450

def paint (event):
    color = 'black'
    x1,y1 = (event.x-1),(event.y-1)
    x2,y2 = (event.x+1),(event.y+1)
    c.create_oval(x1, y1, x2, y2, fill=color, outline=color)

master = Tk()
master.title('Whiteboard')

c = Canvas(master, width=canvas_width, height=canvas_height, bg='white')
c.pack(expand=YES, fill=BOTH)
c.bind('<B1-Motion>', paint)

message = Label(master,text='Draw to your heart\'s content!')
message.pack(side=BOTTOM)
master.mainloop()
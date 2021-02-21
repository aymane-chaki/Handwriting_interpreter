#from tkinter import Tk,Canvas,BOTH,Label,BOTTOM,YES
from tkinter import *
from functools import partial

canvas_width = 600
canvas_height = 450
color = 'black'
diameter = 10

def eraser (event):
    global color
    color = 'white'
    print(color)

def pen (event):
    global color
    color = 'black'
    print(color)

def paint (event):
    global color
    global diameter
    x1,y1 = (event.x-diameter/2),(event.y-diameter/2)
    x2,y2 = (event.x+diameter/2),(event.y+diameter/2)
    c.create_oval(x1, y1, x2, y2, fill=color, outline=color)


master = Tk()
master.title('Whiteboard')



eraser_button = Button(master,text='eraser')
eraser_button.bind('<Button-1>',func=eraser)
pen_button = Button(master,text='pen')
pen_button.bind('<Button-1>',func=pen)

c = Canvas(master, width=canvas_width, height=canvas_height, bg='white')
c.pack(expand=YES, fill=BOTH)
c.bind('<B1-Motion>', func=paint)
#message = Label(master,text='Draw to your heart\'s content!')
#message.pack(side=BOTTOM)
eraser_button.pack()
pen_button.pack()
print(color)
master.mainloop()